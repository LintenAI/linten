"""
``RouterCore``: the interface ``linten.Router`` delegates to, and ``make_core``, which builds it.

The core is ``RustCore`` (``linten/router_rust/core.py`` over linten-rust/crates/router-core),
which reaches outside itself only through its host.
"""

from collections.abc import Mapping
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from linten.router_config import RouterConfig

if TYPE_CHECKING:
    from linten.router_api import (
        ApplyResult,
        ChangeSet,
        RouterHealth,
        RouterRegistry,
        RouterSettings,
        RoutingObservers,
    )
    from linten.router_python_host import PythonHost
    from linten.types.router import CustomRoutingStrategyBase


@runtime_checkable
class RouterCore(Protocol):
    async def call(self, op: str, request: Mapping[str, object]) -> object: ...

    def registry(self) -> "RouterRegistry": ...

    def settings(self) -> "RouterSettings": ...

    def health(self) -> "RouterHealth": ...

    async def select(
        self,
        model: str,
        request_kwargs: dict[str, object] | None = None,  # mutable-ok: the selection cores take a dict
    ) -> object: ...

    def apply(self, changes: "ChangeSet") -> "ApplyResult": ...

    def observe(self) -> "RoutingObservers": ...

    def register_plugin(self, plugin: "CustomRoutingStrategyBase") -> None: ...

    def retire(self) -> None: ...


def make_core(config: RouterConfig, host: "PythonHost") -> RouterCore:
    """The router's core: the Rust core, built once for the router's life from its config."""
    from linten.router_rust.core import RustCore

    return RustCore.build(config, host)  # pyright: ignore[reportReturnType]  # RustCore serves the RouterCore entry points; other members raise RustCoreUnsupported
