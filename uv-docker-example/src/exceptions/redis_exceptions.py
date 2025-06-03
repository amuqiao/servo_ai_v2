from fastapi import HTTPException
from enum import Enum


class RedisErrorCode(Enum):
    KEY_NOT_EXIST = 40001  # 业务错误码（HTTP状态码=400）
    OPERATION_FAILED = 50001  # 业务错误码（HTTP状态码=500）


class RedisException(HTTPException):
    def __init__(self, code: RedisErrorCode, detail: str):
        status_code = code.value // 100  # 从业务错误码中提取HTTP状态码（如40001→400）
        super().__init__(status_code=status_code, detail=detail)
        self.code = code.value  # 业务错误码
        self.message = detail
