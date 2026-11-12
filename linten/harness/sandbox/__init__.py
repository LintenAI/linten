"""Sandboxes for linten.harness: where the runtime runs and which files it can touch."""

from linten.harness.sandbox.base import CompletedRun, Process, Sandbox
from linten.harness.sandbox.docker import DockerSandbox, docker
from linten.harness.sandbox.local import LocalSandbox, local
from linten.harness.sandbox.snapshot import (
    build_file_changes,
    capture_text_contents,
    diff_snapshots,
    snapshot_local,
)

__all__ = (
    "CompletedRun",
    "DockerSandbox",
    "LocalSandbox",
    "Process",
    "Sandbox",
    "build_file_changes",
    "capture_text_contents",
    "diff_snapshots",
    "docker",
    "local",
    "snapshot_local",
)
