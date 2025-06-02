from fastapi import APIRouter
from pydantic import BaseModel

# 定义路由实例（设置前缀和标签）
router = APIRouter(
    prefix="/users", tags=["用户管理1"], responses={404: {"description": "未找到用户"}}
)


# 定义请求数据模型
class UserCreate(BaseModel):
    username: str
    email: str


# 示例路由：创建用户
@router.post("/", response_description="创建新用户")
async def create_user(user: UserCreate):
    return {"message": f"用户 {user.username} 创建成功", "data": user.dict()}


# 示例路由：获取用户详情
@router.get("/{user_id}", response_description="获取用户详情")
async def read_user(user_id: int):
    return {"user_id": user_id, "username": "示例用户"}
