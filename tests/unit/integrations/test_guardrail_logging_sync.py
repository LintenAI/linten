"""
Regression test for _sync_guardrail_info_to_logging_obj.

Ensures that when the @log_guardrail_information decorator writes guardrail info
to request_data["linten_metadata"] (as it does for /v1/messages passthrough
routes that have no "metadata" key), the helper propagates it into
logging_obj.linten_params["metadata"] so merge_linten_metadata surfaces it in
spend logs.
"""

import pytest
from linten.integrations.custom_guardrail import _sync_guardrail_info_to_logging_obj


def _make_slg_entry(name: str = "headroom-test") -> dict:
    return {
        "guardrail_name": name,
        "guardrail_response": "mask",
        "guardrail_status": "success",
        "duration": 0.1,
    }


class _FakeLogging:
    """Minimal stand-in for linten.linten_core_utils.linten_logging.Logging."""

    def __init__(self, lp_metadata: dict | None = None):
        self.linten_params: dict = {"metadata": lp_metadata or {}}
        self.model_call_details: dict = {"linten_params": self.linten_params}


def test_syncs_from_linten_metadata_key():
    """When guardrail info is in request_data["linten_metadata"], it is copied."""
    entry = _make_slg_entry()
    request_data = {
        "linten_metadata": {"standard_logging_guardrail_information": [entry]}
    }
    logging_obj = _FakeLogging()

    _sync_guardrail_info_to_logging_obj(request_data, logging_obj)

    result = logging_obj.linten_params["metadata"].get(
        "standard_logging_guardrail_information"
    )
    assert result == [entry]


def test_syncs_from_metadata_key():
    """When guardrail info is in request_data["metadata"], it is also copied."""
    entry = _make_slg_entry()
    request_data = {"metadata": {"standard_logging_guardrail_information": [entry]}}
    logging_obj = _FakeLogging()

    _sync_guardrail_info_to_logging_obj(request_data, logging_obj)

    result = logging_obj.linten_params["metadata"].get(
        "standard_logging_guardrail_information"
    )
    assert result == [entry]


def test_linten_metadata_wins_over_caller_metadata():
    """When both keys are present the helper must read the bucket the writer used,
    which get_or_create_metadata_bucket resolves to linten_metadata. Reading the
    caller's metadata instead is how a guardrail entry went missing from spend logs
    on the routes that seed linten_metadata."""
    entry_meta = _make_slg_entry("from-metadata")
    entry_lm = _make_slg_entry("from-linten_metadata")
    request_data = {
        "metadata": {"standard_logging_guardrail_information": [entry_meta]},
        "linten_metadata": {"standard_logging_guardrail_information": [entry_lm]},
    }
    logging_obj = _FakeLogging()

    _sync_guardrail_info_to_logging_obj(request_data, logging_obj)

    result = logging_obj.linten_params["metadata"].get(
        "standard_logging_guardrail_information"
    )
    assert result == [entry_lm]


def test_syncs_when_caller_sends_its_own_metadata():
    """The Claude Code shape: caller metadata present, guardrail entry in the seeded
    linten_metadata bucket. The entry must still reach the spend-log payload."""
    entry = _make_slg_entry()
    request_data = {
        "metadata": {"user_id": "device-account-session"},
        "linten_metadata": {"standard_logging_guardrail_information": [entry]},
    }
    logging_obj = _FakeLogging()

    _sync_guardrail_info_to_logging_obj(request_data, logging_obj)

    result = logging_obj.linten_params["metadata"].get(
        "standard_logging_guardrail_information"
    )
    assert result == [entry]


def test_noop_when_no_guardrail_info():
    """Does nothing when standard_logging_guardrail_information is absent."""
    request_data = {"linten_metadata": {"other_key": "value"}}
    logging_obj = _FakeLogging()

    _sync_guardrail_info_to_logging_obj(request_data, logging_obj)

    assert (
        logging_obj.linten_params["metadata"].get(
            "standard_logging_guardrail_information"
        )
        is None
    )


def test_noop_when_logging_obj_is_none():
    """Does nothing when logging_obj is None."""
    entry = _make_slg_entry()
    request_data = {
        "linten_metadata": {"standard_logging_guardrail_information": [entry]}
    }
    _sync_guardrail_info_to_logging_obj(request_data, None)


def test_writes_to_model_call_details_too():
    """Also writes into model_call_details["linten_params"]["metadata"]."""
    entry = _make_slg_entry()
    request_data = {
        "linten_metadata": {"standard_logging_guardrail_information": [entry]}
    }

    logging_obj = _FakeLogging()
    # Simulate linten_params reassignment (creating a new dict) — model_call_details
    # then points to the OLD dict while linten_params points to the new one.
    old_lp = logging_obj.linten_params
    logging_obj.linten_params = {**old_lp, "extra": "added"}
    logging_obj.model_call_details["linten_params"] = old_lp  # diverged

    _sync_guardrail_info_to_logging_obj(request_data, logging_obj)

    # Both dicts should have the info.
    assert logging_obj.linten_params["metadata"].get(
        "standard_logging_guardrail_information"
    ) == [entry]
    assert old_lp["metadata"].get("standard_logging_guardrail_information") == [entry]
