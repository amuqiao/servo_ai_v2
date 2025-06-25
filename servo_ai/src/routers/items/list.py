from fastapi import APIRouter, Query
from typing import Optional

# 版本控制：在 prefix 中添加版本号 v1
router = APIRouter(
    prefix="/v1/items",
    tags=["物品管理"],
    dependencies=[],
    responses={404: {"description": "未找到物品"}}
)

# 示例路由：查询物品列表（保持原功能）
@router.get("/", response_description="获取物品列表")
async def read_items(
    q: Optional[str] = Query(None, max_length=50, description="搜索关键词")
):
    return [{"item_id": 1, "name": "示例物品"}, {"item_id": 2, "name": q or "无关键词"}]