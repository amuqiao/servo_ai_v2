from fastapi import APIRouter, Depends, status, Query
from redis import Redis
from src.configs.redis_config import get_redis_client
from src.celery_app.app import CeleryConfig
from src.services.redis_service import RedisBaseService
from src.schemas.response_schema import BaseResponse
from src.schemas.celery_schema import DemoTaskRequest, BatchDemoTaskRequest,GenerateTasksRequest  # 新增Pydantic模型
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

@router.post("/trigger_subscribe",  # 新增订阅触发接口 
             summary="触发单个模拟订阅任务", 
             response_model=BaseResponse,
             description="向Redis插入单个模拟任务数据，由Celery订阅触发处理")
async def trigger_subscribe_demo_task(
    request: DemoTaskRequest,  # 改为Pydantic模型验证
    redis_client: Redis = Depends(get_redis_client)
):
    task_key = _generate_task_key()
    
    success = RedisBaseService.create_key(redis_client, task_key, json.dumps(request.task_data))
    if not success:
        return BaseResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="任务触发失败")
    
    # 新增：发布任务键到Redis频道
    redis_client.publish("demo_task_channel", task_key)  # 发布到固定频道
    return BaseResponse(message=f"任务已触发并发布，键：{task_key}")


@router.post("/publish_queue",
             summary="发布任务到订阅队列",
             response_model=BaseResponse)
async def publish_to_queue(
    request: DemoTaskRequest,
    redis_client: Redis = Depends(get_redis_client)
):
    config = CeleryConfig()  # 加载Celery配置
    if not redis_client.ping():
        raise HTTPException(status_code=500, detail="Redis连接失败")
    # 发布任务数据到TASK_QUEUE_CHANNEL
    redis_client.publish(
        config.CELERY_TASK_QUEUE_CHANNEL,
        json.dumps(request.task_data)
    )
    return BaseResponse(message="任务已发布到订阅队列")


@router.post("/generate-random-tasks",
             summary="生成并发布随机任务",
             response_model=BaseResponse)
async def generate_random_tasks(
    request: GenerateTasksRequest,
    redis_client: Redis = Depends(get_redis_client)
):
    config = CeleryConfig()  # 加载Celery配置
    if not redis_client.ping():
        raise HTTPException(status_code=500, detail="Redis连接失败")
    
    # 生成随机任务数据
    generated_tasks = []
    for i in range(request.count):
        task_data = {
            "task_type": request.task_type,
            "task_id": str(uuid.uuid4()),
            "content": f"随机内容_{i+1}"
        }
        generated_tasks.append(task_data)
        redis_client.publish(
            config.CELERY_TASK_QUEUE_CHANNEL,
            json.dumps(task_data)
        )
    
    return BaseResponse(message=f"成功生成并发布'{request.count}'个{request.task_type}类型的随机任务")


@router.post("/publish-batch-queue",
             summary="批量发布任务到订阅队列",
             response_model=BaseResponse)
async def publish_batch_to_queue(
    request: BatchDemoTaskRequest,
    redis_client: Redis = Depends(get_redis_client)
):
    if len(request.task_data_list) < 1:
        raise HTTPException(status_code=400, detail="任务数据列表不能为空")
    config = CeleryConfig()  # 加载Celery配置
    if not redis_client.ping():
        raise HTTPException(status_code=500, detail="Redis连接失败")
    # 循环发布task_data_list中的每个任务数据
    for task_data in request.task_data_list:
        redis_client.publish(
            config.CELERY_TASK_QUEUE_CHANNEL,
            json.dumps(task_data)
        )
    return BaseResponse(message=f"{len(request.task_data_list)}个任务已批量发布到订阅队列")