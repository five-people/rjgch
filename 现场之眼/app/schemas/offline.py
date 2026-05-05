"""
离线缓存相关Pydantic模型
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from enum import Enum


class CacheType(str, Enum):
    """缓存类型枚举"""
    DRAWING = "drawing"
    MODEL_3D = "model_3d"
    CONTROL_POINT = "control_point"
    DESIGN_COORDINATE = "design_coordinate"
    PROJECT_DATA = "project_data"


class CacheStatus(str, Enum):
    """缓存状态枚举"""
    SYNCING = "syncing"
    SYNCED = "synced"
    OUTDATED = "outdated"
    ERROR = "error"


class OfflineCacheBase(BaseModel):
    """离线缓存基础模型"""
    name: str = Field(..., min_length=1, max_length=200, description="缓存名称")
    cache_type: CacheType = Field(..., description="缓存类型")
    cache_key: str = Field(..., max_length=255, description="缓存键")
    cache_data: Optional[Any] = Field(None, description="缓存数据")
    file_path: Optional[str] = Field(None, max_length=500, description="文件路径")
    file_size: Optional[float] = Field(None, ge=0, description="文件大小（字节）")
    file_hash: Optional[str] = Field(None, max_length=64, description="文件哈希值")
    is_active: bool = Field(True, description="是否激活")
    expires_at: Optional[datetime] = Field(None, description="过期时间")
    synced_at: Optional[datetime] = Field(None, description="同步时间")
    sync_version: Optional[str] = Field(None, max_length=50, description="同步版本")


class OfflineCacheCreate(OfflineCacheBase):
    """离线缓存创建模型"""
    project_id: int = Field(..., gt=0, description="项目ID")
    user_id: int = Field(..., gt=0, description="用户ID")


class OfflineCacheUpdate(BaseModel):
    """离线缓存更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    cache_data: Optional[Any] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None


class OfflineCacheResponse(OfflineCacheBase):
    """离线缓存响应模型"""
    id: int
    status: CacheStatus
    error_message: Optional[str] = None
    last_accessed: Optional[datetime] = None
    project_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class OfflineCacheListResponse(BaseModel):
    """离线缓存列表响应模型"""
    total: int
    caches: list[OfflineCacheResponse]
    skip: int
    limit: int
