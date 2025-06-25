import logging
import time
import uuid
import json  # 新增JSON模块导入
from src.celery_app import app
from celery import shared_task
from src.services.redis_service import RedisBaseService  # 替换为核心服务层
from src.configs.redis_config import get_redis_client  # 新增：用于获取Redis连接生成器

# 配置Celery任务专用日志记录器（调整为更细粒度的 "celery.task"）
logger = logging.getLogger("celery.task")


@shared_task(name="celery_app.demo_tasks.process_demo_task", bind=True, max_retries=3)
def process_demo_task(self, task_key: str) -> dict:  # 返回值类型调整为字典
    """
    模拟任务处理：使用RedisBaseService完成数据操作
    """
    logger.info(f"开始处理模拟任务，任务键：{task_key}")
    redis_generator = get_redis_client()  # 获取连接生成器
    redis_client = next(redis_generator)  # 获取客户端实例
    try:
        # 1. 使用核心服务层获取并删除任务数据（原子操作）
        data_str = RedisBaseService.get_and_delete_key(redis_client, task_key)  # 获取字符串数据
        if not data_str:
            logger.error(f"任务数据为空，任务键：{task_key}")
            return {"status": False, "message": f"任务数据为空，任务键：{task_key}"}  # 结构化返回

        # 修改：将JSON字符串解析为对象
        data = json.loads(data_str)

        # 2. 模拟耗时操作（如OCR识别）
        logger.info(f"开始模拟耗时处理，任务数据：{data}")
        time.sleep(3)  # 模拟3秒耗时操作

        # 3. 无需额外删除（已通过get_and_delete_key原子删除）
        logger.info(f"模拟任务处理完成并清理，任务键：{task_key}")
        return {"status": True, "message": f"模拟任务处理完成，任务键：{task_key}"}  # 结构化返回

    except Exception as e:
        logger.error(
            f"任务处理失败，任务键：{task_key}，错误详情：{str(e)}", exc_info=True
        )
        self.retry(countdown=2**self.request.retries)
        return {"status": False, "message": f"任务处理失败，错误详情：{str(e)}"}  # 结构化返回
    finally:
        next(redis_generator, None)  # 归还连接（重要：避免连接泄漏）


@shared_task(name="celery_app.demo_tasks.scan_demo_tasks")
def scan_demo_tasks() -> int:
    """
    定时扫描：使用RedisBaseService的通用扫描方法，返回扫描到的任务个数
    """
    redis_generator = get_redis_client()
    redis_client = next(redis_generator)
    task_count = 0
    try:
        logger.debug("开始扫描Redis中的模拟待处理任务")  # 保持与 tasks.py 一致的 debug 日志
        # 使用核心服务层的scan_keys方法（模式：demo_task_*）
        tasks = RedisBaseService.scan_keys(redis_client, match_pattern="demo_task_*")
        task_count = len(tasks)
        if tasks:
            logger.info(f"扫描到{task_count}个待处理模拟任务键")
            for key in tasks:
                logger.debug(f"分发任务键：{key} 到模拟处理任务")
                process_demo_task.apply_async(args=(key,))  # 异步执行处理任务
        else:
            logger.debug("未扫描到待处理的模拟任务键")  # 无任务时记录 debug 日志
        return task_count
    except Exception as e:
        logger.error(f"任务扫描异常，错误详情：{str(e)}", exc_info=True)
        return task_count  # 异常时返回已统计的任务数（可能为0）
    finally:
        next(redis_generator, None)



