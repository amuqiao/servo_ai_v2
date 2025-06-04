from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func  # 导入时间函数
from src.configs.database import Base  # 共享数据库基类（来自postgres_config.py的依赖）

class User(Base):
    __tablename__ = "users"  # 数据库表名

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 新增：创建时间
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # 新增：更新时间（插入时默认当前时间，更新时自动刷新）

    def to_dict(self):
        """转换为字典格式（用于响应）"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),  # 新增：时间格式化为ISO字符串
            "updated_at": self.updated_at.isoformat()  # 新增：更新时间格式化为ISO字符串
        }