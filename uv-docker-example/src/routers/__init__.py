# 导出物品管理路由
from .items import router as items_router
# 导出用户管理路由（示例其他路由）
from .user import router as user_router
# 新增：导出Redis CRUD路由
from .redis_crud import router as redis_crud_router