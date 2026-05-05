"""
离线缓存模型
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from ..database import Base


class CacheType(str, enum.Enum):
    """缓存类型枚举"""
    DRAWING = "drawing"  # 图纸
    MODEL_3D = "model_3d"  # 3D模型
    CONTROL_POINT = "control_point"  # 控制点
    DESIGN_COORDINATE = "design_coordinate"  # 设计坐标
    PROJECT_DATA = "project_data"  # 项目数据


class CacheStatus(str, enum.Enum):
    """缓存状态枚举"""
    SYNCING = "syncing"  # 同步中
    SYNCED = "synced"  # 已同步
    OUTDATED = "outdated"  # 已过期
    ERROR = "error"  # 错误


class OfflineCache(Base):
    """离线缓存表"""
    __tablename__ = "offline_caches"
    
    id = Column(Integer, primary_key=True, index=True, comment="缓存ID")
    name = Column(String(200), nullable=False, index=True, comment="缓存名称")
    
    # 缓存信息
    cache_type = Column(Enum(CacheType), nullable=False, comment="缓存类型")
    cache_key = Column(String(255), unique=True, index=True, comment="缓存键")
    cache_data = Column(JSON, comment="缓存数据")
    
    # 文件信息
    file_path = Column(String(500), comment="文件路径")
    file_size = Column(Float, comment="文件大小（字节）")
    file_hash = Column(String(64), comment="文件哈希值")
    
    # 缓存控制
    is_active = Column(Boolean, default=True, comment="是否激活")
    last_accessed = Column(DateTime(timezone=True), comment="最后访问时间")
    expires_at = Column(DateTime(timezone=True), comment="过期时间")
    
    # 同步信息
    synced_at = Column(DateTime(timezone=True), comment="同步时间")
    sync_version = Column(String(50), comment="同步版本")
    
    # 外键
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="项目ID")
    user_id = Column(Integer, ForeignKey("users.id"), comment="用户ID")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关系
    project = relationship("Project", back_populates="offline_caches")
    
    def __repr__(self):
        return f"<OfflineCache(id={self.id}, name={self.name}, type={self.cache_type})>"
