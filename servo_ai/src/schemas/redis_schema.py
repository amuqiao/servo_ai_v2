from pydantic import BaseModel, Field
from typing import List
from src.schemas.response_schema import SuccessResponse


class RedisKeyDetailResponse(SuccessResponse):
    data: dict = Field(
        ..., 
        description="单个Redis键值对详情", 
        example={"key": "test_key", "value": "test_value"}
    )


class RedisKeyListResponse(SuccessResponse):
    data: List[dict] = Field(
        ..., 
        description="Redis键值对列表", 
        example=[{"key": "key1", "value": "value1"}, {"key": "key2", "value": "value2"}]
    )


class RedisKeyCreateRequest(BaseModel):
    key: str = Field(
        ..., 
        min_length=1, 
        max_length=255, 
        example="user:1001", 
        description="Redis键（唯一标识，长度1-255字符）"
    )
    value: str = Field(
        ..., 
        min_length=1, 
        max_length=1024, 
        example="{'username': 'alice'}", 
        description="Redis值（字符串格式，长度1-1024字符）"
    )


class RedisKeyUpdateRequest(BaseModel):
    key: str = Field(
        ..., 
        min_length=1, 
        max_length=255, 
        example="user:1001", 
        description="待更新的Redis键（需已存在）"
    )
    new_value: str = Field(
        ..., 
        min_length=1, 
        max_length=1024, 
        example="{'username': 'alice_updated'}", 
        description="新值（字符串格式，长度1-1024字符）"
    )
