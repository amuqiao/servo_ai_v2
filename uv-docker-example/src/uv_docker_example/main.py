import logging
from fastapi import FastAPI, Depends
from src.configs.config import ApiConfig, get_config
from fastapi.middleware.cors import CORSMiddleware
from src.configs.logging_config import setup_logging


# 导入路由模块（统一管理各功能路由）
from src.routers import user_router, items_router, redis_crud_router

# 创建模块级别的 logger（名称为当前模块名）
logger = logging.getLogger(__name__)

app = FastAPI(title="My FastAPI Service")

# CORS中间件（生产环境需限制具体源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源（开发用）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 注册路由（将用户管理、物品管理路由挂载到主应用）
app.include_router(user_router)
app.include_router(items_router)
app.include_router(redis_crud_router)

# 配置日志（初始化根 logger 和模块 logger 的处理器）
setup_logging(app)


@app.get("/config")
async def get_app_config(config: ApiConfig = Depends(get_config)):
    """示例接口：返回日志配置"""
    return {
        "project_name": config.project_name,
        "database": config.database,
        "redis": config.redis,
    }


@app.get("/")
async def root():
    logger.info("访问根路径 /")
    return "Hello world1"


@app.get("/hello")
async def hello_luffy():
    logger.debug("访问路径 /hello")
    return "Hello Luffy"


def hello():
    print("Hello world")
    logger.debug("调用了 hello 函数")


if __name__ == "__main__":
    import os
    import sys
    import uvicorn

    print(f"当前工作目录: {os.getcwd()}")
    print("Python路径列表:")
    for path in sys.path:
        print(f"- {path}")
    logger.info("应用启动，开始监听端口 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
