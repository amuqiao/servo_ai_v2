from pydantic import BaseModel


class RedisKeyCreateRequest(BaseModel):
    key: str
    value: str


class RedisKeyUpdateRequest(BaseModel):
    key: str
    new_value: str
