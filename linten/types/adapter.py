from typing import TYPE_CHECKING

from typing_extensions import TypedDict

if TYPE_CHECKING:
    from linten.integrations.custom_logger import CustomLogger


class AdapterItem(TypedDict):
    id: str
    adapter: "CustomLogger"
