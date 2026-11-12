"""
The router and its cores never read or write ``linten.*``.

Process settings reach the router through ``RouterDynamicConfig`` (linten/router_config.py) and
everything else outside it (inference calls, callbacks, the global cache) through ``PythonHost``
(linten/router_python_host.py). Those two modules are the only router code allowed to touch the
``linten`` package namespace. This check fails on ``import linten`` (or ``import linten.<x>``,
which binds the same name) and on any ``linten.<attr>`` access in the files below.

Run: python tests/code_coverage_tests/router_linten_globals_check.py
"""

import ast
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CHECKED = (
    "linten/router.py",
    "linten/router_api.py",
    "linten/router_core.py",
    "linten/router_deprecated.py",
    "linten/router_rust/core.py",
)


def violations(rel: str) -> list[str]:
    tree = ast.parse(open(os.path.join(ROOT, rel)).read(), rel)
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(
                f"{rel}:{node.lineno}: import {alias.name}"
                for alias in node.names
                if alias.asname is None and (alias.name == "linten" or alias.name.startswith("linten."))
            )
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "linten":
            found.append(f"{rel}:{node.lineno}: linten.{node.attr}")
    return found


def main() -> int:
    found = [line for rel in CHECKED for line in violations(rel)]
    for line in found:
        print(line)
    if found:
        print(f"{len(found)} linten.* uses in router modules; read settings from RouterDynamicConfig and use PythonHost")
        return 1
    print("router modules use no linten.* globals")
    return 0


if __name__ == "__main__":
    sys.exit(main())
