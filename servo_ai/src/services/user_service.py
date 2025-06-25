from sqlalchemy.orm import Session
from src.models.user import User
from src.exceptions.user_exceptions import UserException, UserErrorCode
from src.exceptions.common_exceptions import CommonErrorCode
from fastapi import status


class UserService:
    @staticmethod
    def create_user(db: Session, username: str, email: str) -> User:
        """创建用户（检查用户名/邮箱唯一）"""
        if db.query(User).filter(User.username == username).first():
            raise UserException(
                code=UserErrorCode.USERNAME_EXIST,
                message="用户名已存在",
                details={"username": username}
            )
        if db.query(User).filter(User.email == email).first():
            raise UserException(
                code=UserErrorCode.EMAIL_EXIST,
                message="邮箱已注册",
                details={"email": email}
            )
        new_user = User(username=username, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """根据ID获取用户（不存在则抛异常）"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserException(
                code=UserErrorCode.USER_NOT_EXIST,
                message="用户不存在",
                details={"user_id": user_id}
            )
        return user

    @staticmethod
    def update_user(db: Session, user_id: int, new_email: str) -> User:
        """更新用户邮箱（检查邮箱唯一）"""
        user = UserService.get_user(db, user_id)  # 复用获取逻辑，不存在则抛异常
        if db.query(User).filter(User.email == new_email).first():
            raise UserException(
                code=UserErrorCode.EMAIL_EXIST,
                message="邮箱已注册",
                details={"email": new_email}
            )
        user.email = new_email
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        """删除用户（不存在则抛异常）"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserException(
                code=CommonErrorCode.UNKNOWN_ERROR,
                message="用户不存在",
                details={"user_id": user_id}
            )
        try:
            db.delete(user)
            db.commit()
        except Exception as e:
            db.rollback()
            raise UserException(
                code=CommonErrorCode.UNKNOWN_ERROR,
                message="用户删除失败（数据库错误）",
                details={"user_id": user_id, "error": str(e)}
            )
