from pydantic import BaseModel, Field
from typing import List

class DemoTaskRequest(BaseModel):
    task_data: dict = Field(
        ...,
        example={"task_id": "123", "content": "需要处理的内容"},
        description="单个任务数据（直接接收 Python 字典，长度通过序列化后字符串控制在 1-1024 字符）"
    )  # 直接接受 Python 字典输入

class BatchDemoTaskRequest(BaseModel):
    task_data_list: List[dict] = Field(
        ...,
        min_items=1,
        max_items=100,
        example=[
            {"task_id": "1", "content": "批量内容1"},
            {"task_id": "2", "content": "批量内容2"}
        ],
        description="批量任务数据列表（每个元素为 Python 字典，最多 100 个）"
    )  # 每个元素为 Python 字典