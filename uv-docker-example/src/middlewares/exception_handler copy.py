from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging
from typing import Dict, Any, Optional

from src.exceptions.user_exceptions import UserException
from src.exceptions.redis_exceptions import RedisException
from src.schemas.response_schema import ErrorResponse

logger = logging.getLogger(__name__)

def add_exception_handlers(app: FastAPI) -> None:
    """添加全局异常处理器"""
    
    # 处理自定义业务异常
    @app.exception_handler(UserException)
    async def user_exception_handler(request: Request, exc: UserException):
        logger.error(f"用户业务异常: {exc.message}", exc_info=True)
        return JSONResponse(
            content=ErrorResponse(
                code=exc.code,
                message=exc.message,
                details=exc.details,
                status_code=exc.status_code
            ).dict(),
            status_code=exc.status_code
        )

    # 处理Redis业务异常
    @app.exception_handler(RedisException)
    async def redis_exception_handler(request: Request, exc: RedisException):
        logger.error(f"Redis业务异常: {exc.message}", exc_info=True)
        return JSONResponse(
            content=ErrorResponse(
                code=exc.code,
                message=exc.message,
                details=exc.details,
                status_code=exc.status_code
            ).dict(),
            status_code=exc.status_code
        )
    
    # 处理请求验证错误
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"请求验证错误: {exc}", exc_info=True)
        # 提取验证错误详情
        errors = []
        for error in exc.errors():
            errors.append({
                "loc": error["loc"],
                "msg": error["msg"],
                "type": error["type"]
            })
        
        return JSONResponse(
            content=ErrorResponse(
                code=40000,  # 通用验证错误码
                message="请求参数验证失败",
                details={"errors": errors},
                status_code=status.HTTP_400_BAD_REQUEST
            ).dict(),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # 处理Pydantic验证错误
    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        logger.error(f"Pydantic验证错误: {exc}", exc_info=True)
        return JSONResponse(
            content=ErrorResponse(
                code=40000,
                message="数据验证失败",
                details={"errors": exc.errors()},
                status_code=status.HTTP_400_BAD_REQUEST
            ).dict(),
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # 处理未捕获的异常
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error(f"未捕获的异常: {str(exc)}", exc_info=True)
        return JSONResponse(
            content=ErrorResponse(
                code=50000,  # 通用服务器错误码
                message="服务器内部错误，请稍后重试",
                details=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).dict(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
