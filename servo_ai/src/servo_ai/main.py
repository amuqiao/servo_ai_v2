import logging
from fastapi import FastAPI, Depends
from src.configs.config import ApiConfig, get_config
from fastapi.middleware.cors import CORSMiddleware
from src.configs.logging_config import setup_logging
from src.middlewares.exception_handler import add_exception_handlers

# 导入路由模块（统一管理各功能路由）
from src.routers import user_router, items_router, redis_crud_router, celery_demo_router

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

# 添加异常处理器
add_exception_handlers(app)

# 注册路由（将用户管理、物品管理路由挂载到主应用）
app.include_router(user_router)
app.include_router(items_router)
app.include_router(redis_crud_router)
app.include_router(celery_demo_router)

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
    
    
import sys
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from threading import Thread
import asyncio
from uvicorn import Server, Config

async def start_fastapi():
    config = Config(app=app, host="0.0.0.0", port=8000)
    server = Server(config)
    await server.serve()

def start_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()  # 移除sys.exit，避免提前终止主线程

if __name__ == "__main__":
    if "--gui" in sys.argv:
        # 使用asyncio.run启动协程（替代get_event_loop）
        # 启动FastAPI服务在子线程中
        fastapi_thread = Thread(target=lambda: asyncio.run(start_fastapi(), debug=True))
        fastapi_thread.daemon = True  # 设置为守护线程，随主线程退出
        fastapi_thread.start()
        # 启动GUI（主线程）
        start_gui()
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
