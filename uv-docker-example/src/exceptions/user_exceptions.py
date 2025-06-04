from enum import Enum
from fastapi import HTTPException


class UserErrorCode(Enum):
    USER_NOT_EXIST = 40401  # HTTP 404 + 业务子码
    USERNAME_EXIST = 40001  # HTTP 400 + 业务子码
    EMAIL_EXIST = 40002


class UserException(HTTPException):
    def __init__(self, code: UserErrorCode, detail: str):
        # 从业务错误码中提取HTTP状态码（前两位），如40401→404
        status_code = code.value // 100
        super().__init__(status_code=status_code, detail=detail)
        self.code = code.value  # 保留完整业务错误码
        self.message = detail  # 兼容前端获取消息


class UserNotFoundException(UserException):
    def __init__(self, user_id: int):
        super().__init__(
            code=UserErrorCode.USER_NOT_EXIST,
            detail=f"用户ID {user_id} 不存在"
        )
