import logging
from fastapi import FastAPI
from src.configs.logging_config import (
    LogConfig,
    setup_logging,
)
# 导入路由模块（统一管理各功能路由）
from src.routers import user_router, items_router

# 创建模块级别的 logger（名称为当前模块名）
logger = logging.getLogger(__name__)

app = FastAPI(title="My FastAPI Service")

# 注册路由（将用户管理、物品管理路由挂载到主应用）
app.include_router(user_router)
app.include_router(items_router)

# 配置日志（初始化根 logger 和模块 logger 的处理器）
config = LogConfig(LOGGING_LEVEL=logging.INFO)
setup_logging(app)

@app.get("/")
async def root():
    logger.info("访问根路径 /")
    return "Hello world"


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
