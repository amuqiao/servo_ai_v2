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
from src.schemas.response_schema import BaseResponse

router = APIRouter(
    prefix="/users",
    tags=["用户管理"],
    responses={
        # 明确错误响应模型包含业务错误码和消息
        404: {"description": "用户未找到", "model": BaseResponse},
        400: {"description": "参数错误", "model": BaseResponse}
    }
)

# 创建用户（使用UserDetailResponse，明确data是UserResponse）
@router.post("/", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_postgres_db)
):
    created_user = UserService.create_user(db, user.username, user.email)
    return UserDetailResponse(
        data=created_user.to_dict(),  # 确保to_dict()与UserResponse结构一致
        message="用户创建成功"
    )

# 获取单个用户（删除冗余检查）
@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_postgres_db)
):
    user = UserService.get_user(db, user_id)  # 服务层已抛异常，无需检查
    return UserDetailResponse(data=user.to_dict())

# 获取所有用户（验证data类型为 list[UserResponse]）
@router.get("/", response_model=UserListResponse)
async def get_all_users(
    db: Session = Depends(get_postgres_db)
):
    users = db.query(User).all()
    return UserListResponse(
        data=[user.to_dict() for user in users],  # 确保每个user.to_dict()包含updated_at
        message="用户列表获取成功"
    )

# 更新用户（使用UserDetailResponse）
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

# 删除用户（处理用户不存在异常）
@router.delete("/{user_id}", response_model=BaseResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_postgres_db)
):
    UserService.delete_user(db, user_id)
    return BaseResponse(
        status_code=status.HTTP_200_OK,
        message=f"用户ID {user_id} 删除成功"
    )
