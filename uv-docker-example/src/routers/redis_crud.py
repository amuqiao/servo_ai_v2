from fastapi import APIRouter, Depends, HTTPException
from redis import Redis
from src.configs.redis_config import get_redis_client  # 已有依赖注入生成器
from src.services.redis_service import RedisCRUDService  # 新增服务类

router = APIRouter(
    prefix="/redis",
    tags=["Redis CRUD"],
    responses={404: {"description": "资源未找到"}}
)



@router.post("/create", summary="创建键值对")
async def create_redis_key(
    key: str, 
    value: str, 
    redis_client: Redis = Depends(get_redis_client)  # 依赖注入Redis客户端
):
    try:
        success = RedisCRUDService.create_key(redis_client, key, value)
        if not success:
            raise HTTPException(status_code=500, detail="键创建失败")
        return {"status": "success", "key": key, "value": value}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/{key}", summary="获取键值")
async def get_redis_key(
    key: str, 
    redis_client: Redis = Depends(get_redis_client)
):
    try:
        value = RedisCRUDService.get_key(redis_client, key)
        if not value:
            raise HTTPException(status_code=404, detail="键不存在")
        return {"status": "success", "key": key, "value": value}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{key}", summary="更新键值")
async def update_redis_key(
    key: str, 
    new_value: str, 
    redis_client: Redis = Depends(get_redis_client)
):
    try:
        success = RedisCRUDService.update_key(redis_client, key, new_value)
        if not success:
            raise HTTPException(status_code=500, detail="键更新失败")
        return {"status": "success", "key": key, "new_value": new_value}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{key}", summary="删除键")
async def delete_redis_key(
    key: str, 
    redis_client: Redis = Depends(get_redis_client)
):
    try:
        deleted = RedisCRUDService.delete_key(redis_client, key)
        if deleted == 0:
            raise HTTPException(status_code=404, detail="键不存在")
        return {"status": "success", "message": f"键 {key} 已删除"}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))