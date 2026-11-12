"""
Passthrough table repositories.

Each repository centralizes access to a single Prisma table behind a ``table``
property, making the repository the one place that names the underlying table.
These are thin wrappers for tables that do not (yet) need domain-specific query
methods; richer repositories live in their own modules.
"""

from collections.abc import Mapping, Sequence
from datetime import timedelta
from itertools import groupby
from typing import TYPE_CHECKING, Any, Final, Generic, Protocol

from pydantic import TypeAdapter

from linten.linten_core_utils.core_helpers import require_attributes
from linten.linten_core_utils.safe_json_dumps import safe_dumps
from linten.models.access_group import Linten_AccessGroupTable
from linten.repositories.accounting_delivery_repository import LedgerDatabase, LedgerTransaction
from linten.repositories.prisma_protocols import RowT_co, TableActions

if TYPE_CHECKING:
    from prisma import models as prisma_models  # noqa: F401  # used by quoted base-class subscripts


class _PrismaReaderClientView(Protocol):
    @property
    def db(self) -> object: ...


class _PrismaWriterClientView(Protocol):
    @property
    def writer_db(self) -> object: ...


class PrismaTableRepository(Generic[RowT_co]):
    """Base for repositories that expose a single Prisma table."""

    table_name: str

    def __init__(self, prisma_client: object, *, use_writer: bool = False) -> None:
        self._prisma_client = prisma_client
        self._use_writer = use_writer

    def _connected_client(self) -> object:
        if self._prisma_client is None:
            raise RuntimeError("No DB Connected. See - https://docs.linten.ai/docs/proxy/virtual_keys")
        return self._prisma_client

    @property
    def prisma_client(self) -> Any:
        return self._connected_client()

    def _selected_database(self) -> object:
        client: Final = self._connected_client()
        if self._use_writer:
            return require_attributes(client, _PrismaWriterClientView, "writer_db").writer_db
        return require_attributes(client, _PrismaReaderClientView, "db").db

    @property
    def table(self) -> TableActions[RowT_co]:
        from linten.proxy.common_utils.config_sync_pubsub import wrap_table_actions_for_config_sync

        actions: Final[TableActions[RowT_co]] = getattr(self._selected_database(), self.table_name)
        return wrap_table_actions_for_config_sync(actions=actions, table_name=self.table_name)


class PolicyRepository(PrismaTableRepository["prisma_models.Linten_PolicyTable"]):
    table_name = "linten_policytable"


class AgentsRepository(PrismaTableRepository["prisma_models.Linten_AgentsTable"]):
    table_name = "linten_agentstable"


class AgentIdentityRepository(PrismaTableRepository["prisma_models.Linten_AgentIdentity"]):
    table_name = "linten_agentidentity"


class RetiredAgentIdentityRepository(PrismaTableRepository["prisma_models.Linten_RetiredAgentIdentity"]):
    table_name = "linten_retiredagentidentity"


class VerifiedSubjectRepository(PrismaTableRepository["prisma_models.Linten_VerifiedSubject"]):
    table_name = "linten_verifiedsubject"


class ObjectPermissionRepository(PrismaTableRepository["prisma_models.Linten_ObjectPermissionTable"]):
    table_name = "linten_objectpermissiontable"


class GuardrailsRepository(PrismaTableRepository["prisma_models.Linten_GuardrailsTable"]):
    table_name = "linten_guardrailstable"


class MCPServerRepository(PrismaTableRepository["prisma_models.Linten_MCPServerTable"]):
    table_name = "linten_mcpservertable"


class ManagedObjectRepository(PrismaTableRepository["prisma_models.Linten_ManagedObjectTable"]):
    table_name = "linten_managedobjecttable"


class OrganizationMembershipRepository(PrismaTableRepository["prisma_models.Linten_OrganizationMembership"]):
    table_name = "linten_organizationmembership"


_SPEND_LOG_FIELDS: Final = TypeAdapter(dict[str, object])


def _accounting_payload(value: object) -> Mapping[str, object]:
    return (
        _SPEND_LOG_FIELDS.validate_json(value) if isinstance(value, str) else _SPEND_LOG_FIELDS.validate_python(value)
    )


_ACCOUNTING_ONLY_FIELDS: Final = frozenset({"accounting_payload", "accounting_log_disabled", "accounting_delivery_id"})


def _settles_once(row: Mapping[str, object]) -> bool:
    """A batch or video cost row: update_database gives every other ledger row its own delivery id."""
    return "accounting_delivery_id" not in row


def _delivery_id(row: Mapping[str, object]) -> str:
    return str(row["accounting_delivery_id"]) if not _settles_once(row) else str(row["request_id"])


class SpendLogsRepository(PrismaTableRepository["prisma_models.Linten_SpendLogs"]):
    table_name = "linten_spendlogs"

    async def insert_with_deliveries(
        self, rows: Sequence[Mapping[str, object]], *, write_spend_logs: bool = True
    ) -> int:
        legacy: Final = tuple(row for row in rows if "accounting_payload" not in row)
        legacy_count: Final = await self.table.create_many(data=legacy, skip_duplicates=True) if legacy else 0
        ledger: Final = tuple(
            sorted(
                {_delivery_id(row): row for row in reversed(rows) if "accounting_payload" in row}.values(),
                key=_delivery_id,
            )
        )
        if not ledger:
            return legacy_count
        database: Final[LedgerDatabase] = self.prisma_client.writer_db
        async with database.tx(timeout=timedelta(seconds=60)) as transaction:
            accepted: Final = await self._insert_ledger(transaction, ledger, write_spend_logs=write_spend_logs)
        return legacy_count + accepted

    @staticmethod
    async def _insert_ledger(
        transaction: LedgerTransaction, rows: Sequence[Mapping[str, object]], *, write_spend_logs: bool
    ) -> int:
        from linten.proxy.db.db_span import db_span
        from linten.repositories.spend_log_insert import spend_log_insert_statement

        payloads: Final = tuple(
            {
                "delivery_id": _delivery_id(row),
                "request_id": row["request_id"],
                "accounting_payload": _accounting_payload(row["accounting_payload"]),
                "is_batch": _settles_once(row),
            }
            for row in rows
        )
        inserted_deliveries: Final = await transaction.query_raw(
            'INSERT INTO "Linten_SpendLogDelivery" (delivery_id, request_id, accounting_payload, is_batch) '
            "SELECT delivery_id, request_id, accounting_payload, is_batch FROM jsonb_to_recordset($1::jsonb) "
            "AS inputs(delivery_id text, request_id text, accounting_payload jsonb, is_batch boolean) "
            "ON CONFLICT (delivery_id) DO NOTHING RETURNING delivery_id",
            safe_dumps(payloads, non_finite_as_null=True),
        )
        accepted_ids: Final = frozenset(str(row["delivery_id"]) for row in inserted_deliveries)
        charged_by_legacy: Final = await SpendLogsRepository._jobs_charged_by_legacy(
            transaction,
            tuple(_delivery_id(row) for row in rows if _settles_once(row) and _delivery_id(row) in accepted_ids),
        )
        if charged_by_legacy:
            await transaction.execute_raw(
                'DELETE FROM "Linten_SpendLogDelivery" WHERE delivery_id = ANY($1::text[])', list(charged_by_legacy)
            )
        accepted: Final = accepted_ids - charged_by_legacy
        local_rows: Final = tuple(
            {key: value for key, value in row.items() if key not in _ACCOUNTING_ONLY_FIELDS}
            for row in rows
            if _delivery_id(row) in accepted and row.get("accounting_log_disabled") is not True
        )
        if write_spend_logs and local_rows:
            groups: Final = tuple(
                tuple(group)
                for _, group in groupby(
                    sorted(local_rows, key=lambda row: tuple(sorted(row))), key=lambda row: tuple(sorted(row))
                )
            )
            async with db_span("insert_spend_logs", "Linten_SpendLogs"):
                for group in groups:
                    await transaction.query_raw(*spend_log_insert_statement(group))
        return len(accepted)

    @staticmethod
    async def _jobs_charged_by_legacy(transaction: LedgerTransaction, cost_row_ids: Sequence[str]) -> frozenset[str]:
        """Batches and videos a pre-ledger poll already charged through their SpendLogs cost row."""
        if not cost_row_ids:
            return frozenset()
        rows: Final = await transaction.query_raw(
            'SELECT DISTINCT request_id FROM "Linten_SpendLogs" WHERE request_id = ANY($1::text[]) '
            "AND status = 'success' AND spend > 0",
            list(cost_row_ids),
        )
        return frozenset(str(row["request_id"]) for row in rows)

    async def has_delivery(self, delivery_id: str) -> bool:
        database: Final[LedgerTransaction] = self.prisma_client.writer_db
        rows: Final = await database.query_raw(
            'SELECT 1 FROM "Linten_SpendLogDelivery" WHERE delivery_id = $1', delivery_id
        )
        return bool(rows)


class BudgetWindowSpendRepository(PrismaTableRepository["prisma_models.Linten_BudgetWindowSpend"]):
    table_name = "linten_budgetwindowspend"


class ClaudeCodePluginRepository(PrismaTableRepository["prisma_models.Linten_ClaudeCodePluginTable"]):
    table_name = "linten_claudecodeplugintable"


class TeamMembershipRepository(PrismaTableRepository["prisma_models.Linten_TeamMembership"]):
    table_name = "linten_teammembership"


class EndUserRepository(PrismaTableRepository["prisma_models.Linten_EndUserTable"]):
    table_name = "linten_endusertable"


class ManagedVectorStoresRepository(PrismaTableRepository["prisma_models.Linten_ManagedVectorStoresTable"]):
    table_name = "linten_managedvectorstorestable"


class MCPUserCredentialsRepository(PrismaTableRepository["prisma_models.Linten_MCPUserCredentials"]):
    table_name = "linten_mcpusercredentials"


class MCPServerOAuthClientRepository(PrismaTableRepository["prisma_models.Linten_MCPServerOAuthClient"]):
    table_name = "linten_mcpserveroauthclient"


class PromptRepository(PrismaTableRepository["prisma_models.Linten_PromptTable"]):
    table_name = "linten_prompttable"


class TagRepository(PrismaTableRepository["prisma_models.Linten_TagTable"]):
    table_name = "linten_tagtable"


class ModelAccessGroupBudgetRepository(PrismaTableRepository["prisma_models.Linten_ModelAccessGroupBudgetTable"]):
    table_name = "linten_modelaccessgroupbudgettable"


class InvitationLinkRepository(PrismaTableRepository["prisma_models.Linten_InvitationLink"]):
    table_name = "linten_invitationlink"


class JWTKeyMappingRepository(PrismaTableRepository["prisma_models.Linten_JWTKeyMapping"]):
    table_name = "linten_jwtkeymapping"


class MemoryRepository(PrismaTableRepository["prisma_models.Linten_MemoryTable"]):
    table_name = "linten_memorytable"


class SearchToolsRepository(PrismaTableRepository["prisma_models.Linten_SearchToolsTable"]):
    table_name = "linten_searchtoolstable"


class ConfigOverridesRepository(PrismaTableRepository["prisma_models.Linten_ConfigOverrides"]):
    table_name = "linten_configoverrides"


class MCPToolsetRepository(PrismaTableRepository["prisma_models.Linten_MCPToolsetTable"]):
    table_name = "linten_mcptoolsettable"


class ToolRepository(PrismaTableRepository["prisma_models.Linten_ToolTable"]):
    table_name = "linten_tooltable"


class DeletedVerificationTokenRepository(PrismaTableRepository["prisma_models.Linten_DeletedVerificationToken"]):
    table_name = "linten_deletedverificationtoken"


class WorkflowRunRepository(PrismaTableRepository["prisma_models.Linten_WorkflowRun"]):
    table_name = "linten_workflowrun"


class ModelTableRepository(PrismaTableRepository["prisma_models.Linten_ModelTable"]):
    table_name = "linten_modeltable"


class AccessGroupRepository(PrismaTableRepository["prisma_models.Linten_AccessGroupTable"]):
    table_name = "linten_accessgrouptable"

    async def find_by_name(self, name: str) -> Linten_AccessGroupTable | None:
        row: Final = await self.table.find_unique(where={"access_group_name": name})
        return Linten_AccessGroupTable.model_validate(row, from_attributes=True) if row is not None else None


class SSOConfigRepository(PrismaTableRepository["prisma_models.Linten_SSOConfig"]):
    table_name = "linten_ssoconfig"


class UISettingsRepository(PrismaTableRepository["prisma_models.Linten_UISettings"]):
    table_name = "linten_uisettings"


class DailyGuardrailMetricsRepository(PrismaTableRepository["prisma_models.Linten_DailyGuardrailMetrics"]):
    table_name = "linten_dailyguardrailmetrics"


class DailyGuardrailUsageUnitsRepository(PrismaTableRepository["prisma_models.Linten_DailyGuardrailUsageUnits"]):
    table_name = "linten_dailyguardrailusageunits"


class PolicyAttachmentRepository(PrismaTableRepository["prisma_models.Linten_PolicyAttachmentTable"]):
    table_name = "linten_policyattachmenttable"


class TeamRepository(PrismaTableRepository["prisma_models.Linten_TeamTable"]):
    table_name = "linten_teamtable"


class DeletedTeamRepository(PrismaTableRepository["prisma_models.Linten_DeletedTeamTable"]):
    table_name = "linten_deletedteamtable"


class SkillsRepository(PrismaTableRepository["prisma_models.Linten_SkillsTable"]):
    table_name = "linten_skillstable"


class CacheConfigRepository(PrismaTableRepository["prisma_models.Linten_CacheConfig"]):
    table_name = "linten_cacheconfig"


class ManagedVectorStoreIndexRepository(PrismaTableRepository["prisma_models.Linten_ManagedVectorStoreIndexTable"]):
    table_name = "linten_managedvectorstoreindextable"


class WorkflowMessageRepository(PrismaTableRepository["prisma_models.Linten_WorkflowMessage"]):
    table_name = "linten_workflowmessage"


class DailyTagSpendRepository(PrismaTableRepository["prisma_models.Linten_DailyTagSpend"]):
    table_name = "linten_dailytagspend"


class SpendLogToolIndexRepository(PrismaTableRepository["prisma_models.Linten_SpendLogToolIndex"]):
    table_name = "linten_spendlogtoolindex"


class DailyToolSpendRepository(PrismaTableRepository["prisma_models.Linten_DailyToolSpend"]):
    table_name = "linten_dailytoolspend"


class DailyModelUsageRepository(PrismaTableRepository["prisma_models.Linten_DailyModelUsage"]):
    table_name = "linten_dailymodelusage"


class SpendLogGuardrailIndexRepository(PrismaTableRepository["prisma_models.Linten_SpendLogGuardrailIndex"]):
    table_name = "linten_spendlogguardrailindex"


class UserNotificationsRepository(PrismaTableRepository["prisma_models.Linten_UserNotifications"]):
    table_name = "linten_usernotifications"


class HealthCheckRepository(PrismaTableRepository["prisma_models.Linten_HealthCheckTable"]):
    table_name = "linten_healthchecktable"


class DeprecatedVerificationTokenRepository(PrismaTableRepository["prisma_models.Linten_DeprecatedVerificationToken"]):
    table_name = "linten_deprecatedverificationtoken"


class WorkflowEventRepository(PrismaTableRepository["prisma_models.Linten_WorkflowEvent"]):
    table_name = "linten_workflowevent"


class DailyPolicyMetricsRepository(PrismaTableRepository["prisma_models.Linten_DailyPolicyMetrics"]):
    table_name = "linten_dailypolicymetrics"


class AdaptiveRouterStateRepository(PrismaTableRepository["prisma_models.Linten_AdaptiveRouterState"]):
    table_name = "linten_adaptiverouterstate"


class AuditLogRepository(PrismaTableRepository["prisma_models.Linten_AuditLog"]):
    table_name = "linten_auditlog"


class AdaptiveRouterSessionRepository(PrismaTableRepository["prisma_models.Linten_AdaptiveRouterSession"]):
    table_name = "linten_adaptiveroutersession"


class BackgroundInteractionSettlementRepository(
    PrismaTableRepository["prisma_models.Linten_BackgroundInteractionSettlement"]
):
    table_name = "linten_backgroundinteractionsettlement"


class BackgroundResponseSettlementRepository(
    PrismaTableRepository["prisma_models.Linten_BackgroundResponseSettlement"]
):
    table_name = "linten_backgroundresponsesettlement"


class RetiredAgentRepository(PrismaTableRepository["prisma_models.Linten_RetiredAgent"]):
    table_name = "linten_retiredagent"


class DailyUserSpendRepository(PrismaTableRepository["prisma_models.Linten_DailyUserSpend"]):
    table_name = "linten_dailyuserspend"
