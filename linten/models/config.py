"""
Config table model.

Canonical definition for ``linten_config``. Re-exported from
``linten.proxy._types`` for backwards compatibility.
"""

from linten.types.llms.base import LintenPydanticObjectBase


class Linten_Config(LintenPydanticObjectBase):
    param_name: str
    param_value: dict
