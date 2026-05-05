"""
API路由模块
"""

from fastapi import APIRouter

from .auth import router as auth_router
from .projects import router as projects_router
from .measurements import router as measurements_router
from .drawings import router as drawings_router
from .models import router as models_router
from .offline import router as offline_router

# 创建主路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(projects_router, prefix="/projects", tags=["项目管理"])
api_router.include_router(measurements_router, prefix="/measurements", tags=["测量记录"])
api_router.include_router(drawings_router, prefix="/drawings", tags=["图纸管理"])
api_router.include_router(models_router, prefix="/models", tags=["3D模型"])
api_router.include_router(offline_router, prefix="/offline", tags=["离线管理"])
