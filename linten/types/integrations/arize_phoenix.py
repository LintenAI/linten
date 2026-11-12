from linten.types.llms.base import LintenBaseModel

from .arize import Protocol


class ArizePhoenixConfig(LintenBaseModel):
    otlp_auth_headers: str | None = None
    protocol: Protocol
    endpoint: str
    project_name: str | None = None
