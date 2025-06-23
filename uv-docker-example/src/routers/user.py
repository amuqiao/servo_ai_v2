from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.schemas.user_schema import (
    UserCreate, 
    UserUpdate, 
    UserResponse, 
    UserListResponse,
    UserDetailResponse
)
from src.services.user_service import UserService
from src.configs.postgres_config import get_postgres_db
from src.models.user import User
from src.exceptions.user_exceptions import UserException
from src.schemas.response_schema import BaseResponse, ErrorResponse
from src.schemas.response_schema import SuccessResponse  # 新增导入

router = APIRouter(
    prefix="/users",
    tags=["用户管理"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "未认证", "model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "服务器错误", "model": ErrorResponse}
    }
)

# 创建用户（保持使用 UserDetailResponse）
@router.post("/", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_postgres_db)
):
    created_user = UserService.create_user(db, user.username, user.email)
    return UserDetailResponse(data=created_user.to_dict(), message="用户创建成功")

# 获取单个用户（保持使用 UserDetailResponse）
@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_postgres_db)
):
    user = UserService.get_user(db, user_id)  # 服务层已抛异常，无需检查
    return UserDetailResponse(data=user.to_dict())

# 获取所有用户（保持使用 UserListResponse）
@router.get("/", response_model=UserListResponse)
async def get_all_users(
    db: Session = Depends(get_postgres_db)
):
    users = db.query(User).all()
    return UserListResponse(data=[user.to_dict() for user in users], message="用户列表获取成功")

# 更新用户（保持使用 UserDetailResponse）
@router.put("/{user_id}", response_model=UserDetailResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_postgres_db)
):
    updated_user = UserService.update_user(db, user_id, user_update.email)  # 服务层已抛异常
    return UserDetailResponse(
        data=updated_user.to_dict(),
        message="用户信息更新成功"
    )

# 删除用户（改为使用 SuccessResponse，明确成功响应结构）
@router.delete("/{user_id}", response_model=SuccessResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_postgres_db)
):
    UserService.delete_user(db, user_id)
    return SuccessResponse(  # 使用 SuccessResponse 替代 BaseResponse
        message=f"用户ID {user_id} 删除成功",
        data=None  # 可选：若需返回额外信息（如删除的用户ID），可填充到 data
    )
