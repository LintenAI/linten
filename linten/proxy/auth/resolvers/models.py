from __future__ import annotations

from enum import Enum

from pydantic import ConfigDict, Field

from linten.proxy._types import UserAPIKeyAuth
from linten.proxy.auth.auth_method import AuthMethod
from linten.proxy.auth.network import NetworkContext
from linten.proxy.auth.roles import Role, TeamRole
from linten.types.llms.base import LintenBaseModel


class PrincipalType(str, Enum):
    HUMAN = "human"
    SERVICE_ACCOUNT = "service_account"


class UserIdentity(LintenBaseModel):
    id: str
    external_id: str | None = None
    user_name: str | None = None
    email: str | None = None
    display_name: str | None = None


class OrganizationIdentity(LintenBaseModel):
    id: str
    name: str | None = None


class TeamIdentity(LintenBaseModel):
    id: str
    name: str | None = None
    role: TeamRole = TeamRole.MEMBER


class ProjectIdentity(LintenBaseModel):
    id: str
    name: str | None = None


class EndUserIdentity(LintenBaseModel):
    id: str


class CredentialRef(LintenBaseModel):
    key_id: str | None = None
    token_id: str | None = None


class Principal(LintenBaseModel):
    """Normalized caller identity, resolved once per request at the auth seam.

    Frozen and constructed fresh per request, never cached or shared. The identity
    fields carry no policy, budget, or rate-limit state. ``source_key`` is a
    transitional carrier for the resolved key object so ``key_from_principal`` can
    hand it to the request flow that still consumes ``UserAPIKeyAuth``; it is
    excluded from serialization and repr and goes away once those consumers read
    identity off the Principal directly.
    """

    model_config = ConfigDict(frozen=True)

    principal_type: PrincipalType
    subject: str
    issuer: str | None = None
    audience: list[str] = Field(default_factory=list)

    user: UserIdentity | None = None
    organization: OrganizationIdentity | None = None
    teams: list[TeamIdentity] = Field(default_factory=list)
    project: ProjectIdentity | None = None
    end_user: EndUserIdentity | None = None

    roles: list[Role] = Field(default_factory=list)
    scopes: list[str] = Field(default_factory=list)

    auth_method: AuthMethod
    credential_ref: CredentialRef = Field(default_factory=CredentialRef)
    network: NetworkContext = Field(default_factory=NetworkContext)

    source_key: UserAPIKeyAuth | None = Field(default=None, exclude=True, repr=False)
