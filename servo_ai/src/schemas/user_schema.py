from pydantic import BaseModel, EmailStr, Field
from datetime import datetime  # 新增：时间类型
from src.schemas.response_schema import BaseResponse, SuccessResponse, ErrorResponse

# 请求模型：创建用户
class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50, example="alice")
    email: EmailStr = Field(..., example="alice@example.com")

# 请求模型：更新用户
class UserUpdate(BaseModel):
    email: EmailStr | None = Field(example="new_alice@example.com")  # 允许不修改邮箱
    username: str | None = Field(None, min_length=2, max_length=50, example="张三")  # 明确允许None值，仅当提供时验证长度

# 响应模型：用户详情（补充 updated_at 字段）
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime  # 与模型层对齐
    updated_at: datetime  # 新增：补充更新时间

    class Config:
        orm_mode = True  # 支持从ORM对象转换

# 响应模型：用户列表（继承BaseResponse，明确data类型）
# 原 UserListResponse 和 UserDetailResponse 调整
class UserListResponse(SuccessResponse):  # 继承 SuccessResponse（含 data 字段）
    data: list[UserResponse] | None = None

class UserDetailResponse(SuccessResponse):  # 继承 SuccessResponse（含 data 字段）
    data: UserResponse | None = None