from fastapi import APIRouter, Depends
from redis import Redis
from src.configs.redis_config import get_redis_client
from src.services.redis_service import RedisBaseService
from src.schemas.redis_schema import RedisKeyCreateRequest, RedisKeyUpdateRequest
from src.schemas.response_schema import SuccessResponse, ErrorResponse
from src.exceptions.redis_exceptions import RedisException, RedisErrorCode

router = APIRouter(
    prefix="/redis",
    tags=["Redis CRUD"],
    responses={
        400: {"description": "请求参数格式错误", "model": ErrorResponse},
        404: {"description": "资源未找到", "model": ErrorResponse},
        500: {"description": "Redis服务不可用或操作失败", "model": ErrorResponse}
    }
)

@router.post("/create", 
             summary="创建Redis键值对", 
             response_model=SuccessResponse,
             description="通过指定键（key）和值（value）在Redis中创建键值对。若键已存在，将覆盖旧值。",
             responses={
                 502: {"description": "键创建失败", "model": ErrorResponse}
             })
async def create_redis_key(
    request: RedisKeyCreateRequest,  # 使用Pydantic自动校验请求体
    redis_client: Redis = Depends(get_redis_client)
):
    RedisBaseService.create_key(redis_client, request.key, request.value)
    return SuccessResponse(data={"key": request.key, "value": request.value})

@router.get("/get/{key}", 
            summary="获取Redis键值", 
            response_model=SuccessResponse,
            description="根据指定键（key）获取Redis中的值。若键不存在返回空字符串并抛出异常。",
            responses={
                404: {"description": "键不存在（key未找到）", "model": ErrorResponse}
            })
async def get_redis_key(
    key: str, 
    redis_client: Redis = Depends(get_redis_client)
):
    value = RedisBaseService.get_key(redis_client, key)
    return SuccessResponse(data={"key": key, "value": value})

@router.put("/update/{key}", 
            summary="更新Redis键值", 
            response_model=SuccessResponse,
            description="根据指定键（key）更新Redis中的值。若键不存在则更新失败并抛出异常。",
            responses={
                503: {"description": "键更新失败", "model": ErrorResponse}
            })  # 移除重复的400定义
async def update_redis_key(
    key: str, 
    request: RedisKeyUpdateRequest,  # 使用Pydantic请求体自动校验
    redis_client: Redis = Depends(get_redis_client)
):
    RedisBaseService.update_key(redis_client, key, request.new_value)
    return SuccessResponse(data={"key": key, "new_value": request.new_value})

@router.delete("/delete/{key}", 
               summary="删除Redis键", 
               response_model=SuccessResponse,
               description="根据指定键（key）删除Redis中的键。若键不存在则删除失败并抛出异常。",
               responses={
                   504: {"description": "键删除失败", "model": ErrorResponse}
               })
async def delete_redis_key(
    key: str, 
    redis_client: Redis = Depends(get_redis_client)
):
    RedisBaseService.delete_key(redis_client, key)
    return SuccessResponse(data={"message": f"键 {key} 已删除"})