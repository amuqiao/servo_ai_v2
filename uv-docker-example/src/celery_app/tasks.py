import logging
from datetime import datetime
from src.celery_app import app  # 导入Celery应用实例

# 新增：每分钟执行的定时任务（打印当前时间）
@app.task(name="celery_app.tasks.log_current_time")  # 显式命名任务（与BEAT_SCHEDULE路径一致）
def log_current_time():
    logger = logging.getLogger("celery.task")  # 使用Celery任务专用日志器
    current_time = datetime.now().isoformat()  # 获取当前时间的ISO格式字符串
    logger.info(f"定时任务执行，当前时间：{current_time}")  # 打印时间到日志
    return {"status": "success", "message": f"时间已记录：{current_time}"}