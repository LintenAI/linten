from typing import Final

from fastapi import Request


def get_linten_virtual_key(request: Request) -> str:
    """
    Extract and format API key from request headers.
    Prioritizes x-linten-api-key over Authorization header.


    Vertex JS SDK uses `Authorization` header, we use `x-linten-api-key` to pass linten virtual key

    """
    linten_api_key: Final = request.headers.get("x-linten-api-key")
    if linten_api_key:
        return f"Bearer {linten_api_key}"
    return request.headers.get("Authorization", "")
