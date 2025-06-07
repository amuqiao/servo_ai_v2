from fastapi import APIRouter, Depends
from redis import Redis
from src.configs.redis_config import get_redis_client
from src.services.redis_service import RedisBaseService
from src.schemas.redis_schema import RedisKeyCreateRequest, RedisKeyUpdateRequest
from src.schemas.response_schema import BaseResponse
from src.exceptions.redis_exceptions import RedisException, RedisErrorCode

router = APIRouter(
    prefix="/redis",
    tags=["Redis CRUD"],
    responses={404: {"description": "资源未找到"}}
)

@router.post("/create", 
             summary="创建Redis键值对", 
             response_model=BaseResponse,
             description="通过指定键（key）和值（value）在Redis中创建键值对。若键已存在，将覆盖旧值。",
             responses={
                 400: {"description": "请求参数格式错误（如key/value为空）"},
                 500: {"description": "Redis服务不可用或操作失败"}
             })
async def create_redis_key(
    request: RedisKeyCreateRequest,  # 使用Pydantic自动校验请求体
    redis_client: Redis = Depends(get_redis_client)
):
    success = RedisBaseService.create_key(redis_client, request.key, request.value)
    if not success:
        raise RedisException(RedisErrorCode.OPERATION_FAILED, "键创建失败")
    return BaseResponse(data={"key": request.key, "value": request.value})

@router.get("/get/{key}", 
            summary="获取Redis键值", 
            response_model=BaseResponse,
            description="根据指定键（key）获取Redis中的值。若键不存在返回空字符串并抛出异常。",
            responses={
                404: {"description": "键不存在（key未找到）"},
                500: {"description": "Redis服务不可用或操作失败"}
            })
async def get_redis_key(
    key: str, 
    redis_client: Redis = Depends(get_redis_client)
):
    value = RedisBaseService.get_key(redis_client, key)
    if not value:
        raise RedisException(RedisErrorCode.KEY_NOT_EXIST, "键不存在")
    return BaseResponse(data={"key": key, "value": value})

@router.put("/update/{key}", 
            summary="更新Redis键值", 
            response_model=BaseResponse,
            description="根据指定键（key）更新Redis中的值。若键不存在则更新失败并抛出异常。",
            responses={
                400: {"description": "请求参数格式错误（如new_value为空）"},
                404: {"description": "键不存在（key未找到）"},
                500: {"description": "Redis服务不可用或操作失败"}
            })
async def update_redis_key(
    key: str, 
    request: RedisKeyUpdateRequest,  # 使用Pydantic请求体自动校验
    redis_client: Redis = Depends(get_redis_client)
):
    success = RedisBaseService.update_key(redis_client, key, request.new_value)
    if not success:
        raise RedisException(RedisErrorCode.OPERATION_FAILED, "键更新失败")
    return BaseResponse(data={"key": key, "new_value": request.new_value})

@router.delete("/delete/{key}", 
               summary="删除Redis键", 
               response_model=BaseResponse,
               description="根据指定键（key）删除Redis中的键。若键不存在则删除失败并抛出异常。",
               responses={
                   404: {"description": "键不存在（key未找到）"},
                   500: {"description": "Redis服务不可用或操作失败"}
               })
async def delete_redis_key(
    key: str, 
    redis_client: Redis = Depends(get_redis_client)
):
    deleted = RedisBaseService.delete_key(redis_client, key)
    if deleted == 0:
        raise RedisException(RedisErrorCode.KEY_NOT_EXIST, "键不存在")
    return BaseResponse(data={"message": f"键 {key} 已删除"})