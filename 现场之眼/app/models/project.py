"""
项目模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from ..database import Base


class ProjectStatus(str, enum.Enum):
    """项目状态枚举"""
    DRAFT = "draft"  # 草稿
    ACTIVE = "active"  # 进行中
    COMPLETED = "completed"  # 已完成
    ARCHIVED = "archived"  # 已归档


class CoordinateSystem(str, enum.Enum):
    """坐标系类型枚举"""
    WGS84 = "wgs84"  # 世界大地坐标系
    GCJ02 = "gcj02"  # 火星坐标系
    BD09 = "bd09"  # 百度坐标系
    LOCAL = "local"  # 局部坐标系


class Project(Base):
    """项目表"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True, comment="项目ID")
    name = Column(String(200), nullable=False, index=True, comment="项目名称")
    code = Column(String(50), unique=True, index=True, comment="项目编码")
    description = Column(Text, comment="项目描述")
    
    # 坐标系信息
    coordinate_system = Column(Enum(CoordinateSystem), default=CoordinateSystem.WGS84, comment="坐标系类型")
    reference_latitude = Column(Float, comment="基准纬度")
    reference_longitude = Column(Float, comment="基准经度")
    reference_elevation = Column(Float, comment="基准高程")
    
    # 项目状态
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DRAFT, comment="项目状态")
    
    # 偏差阈值设置
    deviation_threshold_x = Column(Float, default=0.05, comment="X方向偏差阈值（米）")
    deviation_threshold_y = Column(Float, default=0.05, comment="Y方向偏差阈值（米）")
    deviation_threshold_z = Column(Float, default=0.05, comment="Z方向偏差阈值（米）")
    
    # 项目信息
    location = Column(String(200), comment="项目地点")
    start_date = Column(DateTime(timezone=True), comment="开始日期")
    end_date = Column(DateTime(timezone=True), comment="结束日期")
    
    # 外键
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="负责人ID")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关系
    owner = relationship("User", back_populates="projects")
    control_points = relationship("ControlPoint", back_populates="project", cascade="all, delete-orphan")
    design_coordinates = relationship("DesignCoordinate", back_populates="project", cascade="all, delete-orphan")
    drawings = relationship("Drawing", back_populates="project", cascade="all, delete-orphan")
    models_3d = relationship("Model3D", back_populates="project", cascade="all, delete-orphan")
    measurement_records = relationship("MeasurementRecord", back_populates="project", cascade="all, delete-orphan")
    deviation_records = relationship("DeviationRecord", back_populates="project", cascade="all, delete-orphan")
    offline_caches = relationship("OfflineCache", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, code={self.code})>"
