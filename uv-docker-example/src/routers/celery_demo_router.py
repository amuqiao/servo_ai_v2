from fastapi import APIRouter, Depends, status, Query
from redis import Redis
from src.configs.redis_config import get_redis_client
from src.services.redis_service import RedisBaseService
from src.schemas.response_schema import BaseResponse
from src.schemas.celery_schema import DemoTaskRequest, BatchDemoTaskRequest  # 新增Pydantic模型
import uuid
import json  # 新增JSON模块导入

router = APIRouter(
    prefix="/demo-tasks",
    tags=["Celery 模拟任务"],
    responses={404: {"description": "资源未找到"}}
)

def _generate_task_key() -> str:
    """公共方法：生成符合扫描规则的任务键"""
    return f"demo_task_{str(uuid.uuid4())}"

@router.post("/trigger", 
             summary="触发单个模拟任务", 
             response_model=BaseResponse,
             description="向Redis插入单个模拟任务数据，由Celery定时扫描处理")
async def trigger_demo_task(
    request: DemoTaskRequest,  # 改为Pydantic模型验证
    redis_client: Redis = Depends(get_redis_client)
):
    task_key = _generate_task_key()
    
    success = RedisBaseService.create_key(redis_client, task_key, json.dumps(request.task_data))
    if not success:
        return BaseResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="任务触发失败")
    return BaseResponse(message=f"任务已触发，键：{task_key}")

# @router.post("/trigger_subscribe",  # 新增订阅触发接口 
#              summary="触发单个模拟订阅任务", 
#              response_model=BaseResponse,
#              description="向Redis插入单个模拟任务数据，由Celery订阅触发处理")
# async def trigger_subscribe_demo_task(
#     request: DemoTaskRequest,  # 改为Pydantic模型验证
#     redis_client: Redis = Depends(get_redis_client)
# ):
#     task_key = _generate_task_key()
    
#     success = RedisBaseService.create_key(redis_client, task_key, json.dumps(request.task_data))
#     if not success:
#         return BaseResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="任务触发失败")
    
#     # 新增：发布任务键到Redis频道
#     redis_client.publish("demo_task_channel", task_key)  # 发布到固定频道
#     return BaseResponse(message=f"任务已触发并发布，键：{task_key}")