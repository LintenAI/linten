from collections.abc import Mapping
from typing import Final

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import TypeAdapter

import linten
from linten._logging import verbose_proxy_logger
from linten.caching.caching import RedisCache
from linten.linten_core_utils.core_helpers import decoded_json_object
from linten.linten_core_utils.safe_json_dumps import safe_dumps
from linten.linten_core_utils.sensitive_data_masker import SensitiveDataMasker
from linten.proxy._types import ProxyErrorTypes, ProxyException
from linten.proxy.auth.user_api_key_auth import user_api_key_auth
from linten.types.caching import CachePingResponse, HealthCheckCacheParams

masker: Final = SensitiveDataMasker()
_DECODED_JSON: Final = TypeAdapter(object)

router: Final = APIRouter(
    prefix="/cache",
    tags=["caching"],
)


def _copy_cache_params(cache_params: Mapping[str, object]) -> Mapping[str, object]:
    return dict(**cache_params)


def _extract_cache_params() -> dict[str, object]:
    """
    Safely extracts and cleans cache parameters.

    The health check UI needs to display specific cache parameters, to show users how they set up their cache.

    eg.
        {
            "host": "localhost",
            "port": 6379,
            "redis_kwargs": {"db": 0},
            "namespace": "test",
        }

    Returns:
        Dict containing cleaned and masked cache parameters
    """
    if linten.cache is None:
        return {}
    try:
        cache_params: Final = vars(linten.cache.cache)
        cleaned_params: Final = (
            HealthCheckCacheParams.model_validate(_copy_cache_params(cache_params)).model_dump() if cache_params else {}
        )
        return masker.mask_dict(cleaned_params)
    except (AttributeError, TypeError) as e:
        verbose_proxy_logger.debug("Error extracting cache params: %s", e)
        return {}


@router.get(
    "/ping",
    response_model=CachePingResponse,
    dependencies=[Depends(user_api_key_auth)],
)
async def cache_ping():
    """
    Endpoint for checking if cache can be pinged
    """
    linten_cache_params: dict[str, object] = {}
    cleaned_cache_params: dict[str, object] = {}
    if linten.cache is None:
        raise ProxyException(
            message=safe_dumps(
                {
                    "message": "Cache not initialized. linten.cache is None",
                    "linten_cache_params": "{}",
                    "health_check_cache_params": "{}",
                }
            ),
            type=ProxyErrorTypes.cache_ping_error,
            param="cache_ping",
            code=503,
        )
    try:
        linten_cache_params = masker.mask_dict(vars(linten.cache))
        # remove field that might reference itself
        linten_cache_params.pop("cache", None)
        cleaned_cache_params = _extract_cache_params()

        if linten.cache.type == "redis":
            ping_response: Final = await linten.cache.ping()
            verbose_proxy_logger.debug("/cache/ping: ping_response: " + str(ping_response))
            # add cache does not return anything
            await linten.cache.async_add_cache(
                result="test_key",
                model="test-model",
                messages=[{"role": "user", "content": "test from linten"}],
            )
            verbose_proxy_logger.debug("/cache/ping: done with set_cache()")

            return CachePingResponse(
                status="healthy",
                cache_type=str(linten.cache.type),
                ping_response=True,
                set_cache_response="success",
                linten_cache_params=safe_dumps(linten_cache_params),
                health_check_cache_params=cleaned_cache_params,
            )
        else:
            return CachePingResponse(
                status="healthy",
                cache_type=str(linten.cache.type),
                linten_cache_params=safe_dumps(linten_cache_params),
            )
    except HTTPException:
        raise
    except Exception:
        verbose_proxy_logger.exception("Cache health check failed")
        error_message: Final = {
            "message": "Service Unhealthy",
            "linten_cache_params": safe_dumps(linten_cache_params),
            "health_check_cache_params": safe_dumps(cleaned_cache_params),
        }
        raise ProxyException(
            message=safe_dumps(error_message),
            type=ProxyErrorTypes.cache_ping_error,
            param="cache_ping",
            code=503,
        )


@router.post(
    "/delete",
    tags=["caching"],
    dependencies=[Depends(user_api_key_auth)],
)
async def cache_delete(request: Request):
    """
    Endpoint for deleting a key from the cache. All responses from linten proxy have `x-linten-cache-key` in the headers

    Parameters:
    - **keys**: *Optional[List[str]]* - A list of keys to delete from the cache. Example {"keys": ["key1", "key2"]}

    ```shell
    curl -X POST "http://0.0.0.0:4000/cache/delete" \
    -H "Authorization: Bearer $LINTEN_MASTER_KEY" \
    -d '{"keys": ["key1", "key2"]}'
    ```

    """
    try:
        if linten.cache is None:
            raise HTTPException(status_code=503, detail="Cache not initialized. linten.cache is None")

        request_data: Final = decoded_json_object(_DECODED_JSON.validate_python(await request.json()))
        keys: Final = request_data.get("keys", None)

        if linten.cache.type == "redis":
            await linten.cache.delete_cache_keys(keys=keys)
            return {
                "status": "success",
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Cache type {linten.cache.type} does not support deleting a key. only `redis` is supported",
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Cache Delete Failed({e})",
        )


def _get_redis_client_info(cache_instance: RedisCache) -> tuple[list[object], int]:
    """
    Helper function to safely get Redis client list information.

    Returns:
        tuple: (client_list, num_clients) where num_clients is -1 if CLIENT LIST is unavailable
    """
    try:
        client_list: Final = cache_instance.client_list()
        return client_list, len(client_list)
    except Exception as e:
        verbose_proxy_logger.warning("CLIENT LIST command failed (likely restricted on managed Redis): %s", e)
        return ["CLIENT LIST command not available on this Redis instance"], -1


@router.get(
    "/redis/info",
    dependencies=[Depends(user_api_key_auth)],
)
async def cache_redis_info():
    """
    Endpoint for getting /redis/info
    """
    try:
        if linten.cache is None:
            raise HTTPException(status_code=503, detail="Cache not initialized. linten.cache is None")

        if not (linten.cache.type == "redis" and isinstance(linten.cache.cache, RedisCache)):
            raise HTTPException(
                status_code=500,
                detail=f"Cache type {linten.cache.type} does not support redis info",
            )

        # Get client information (handles CLIENT LIST restrictions gracefully)
        client_list, num_clients = _get_redis_client_info(linten.cache.cache)

        # Get Redis server information
        redis_info: Final = linten.cache.cache.info()

        return {
            "num_clients": num_clients,
            "clients": client_list,
            "info": redis_info,
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service Unhealthy ({e})",
        )


@router.post(
    "/flushall",
    tags=["caching"],
    dependencies=[Depends(user_api_key_auth)],
)
async def cache_flushall():
    """
    A function to flush all items from the cache. (All items will be deleted from the cache with this)
    Raises HTTPException if the cache is not initialized or if the cache type does not support flushing.
    Returns a dictionary with the status of the operation.

    Usage:
    ```
    curl -X POST http://0.0.0.0:4000/cache/flushall -H "Authorization: Bearer $LINTEN_MASTER_KEY"
    ```
    """
    try:
        if linten.cache is None:
            raise HTTPException(status_code=503, detail="Cache not initialized. linten.cache is None")
        if linten.cache.type == "redis" and isinstance(linten.cache.cache, RedisCache):
            linten.cache.cache.flushall()
            return {
                "status": "success",
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Cache type {linten.cache.type} does not support flushing",
            )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service Unhealthy ({e})",
        )
