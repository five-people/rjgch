"""
项目相关Pydantic模型
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum


class ProjectStatus(str, Enum):
    """项目状态枚举"""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CoordinateSystem(str, Enum):
    """坐标系类型枚举"""
    WGS84 = "wgs84"
    GCJ02 = "gcj02"
    BD09 = "bd09"
    LOCAL = "local"


class ProjectBase(BaseModel):
    """项目基础模型"""
    name: str = Field(..., min_length=1, max_length=200, description="项目名称")
    code: str = Field(..., min_length=1, max_length=50, description="项目编码")
    description: Optional[str] = Field(None, description="项目描述")
    coordinate_system: CoordinateSystem = Field(CoordinateSystem.WGS84, description="坐标系类型")
    reference_latitude: Optional[float] = Field(None, ge=-90, le=90, description="基准纬度")
    reference_longitude: Optional[float] = Field(None, ge=-180, le=180, description="基准经度")
    reference_elevation: Optional[float] = Field(None, description="基准高程")
    deviation_threshold_x: float = Field(0.05, ge=0, description="X方向偏差阈值（米）")
    deviation_threshold_y: float = Field(0.05, ge=0, description="Y方向偏差阈值（米）")
    deviation_threshold_z: float = Field(0.05, ge=0, description="Z方向偏差阈值（米）")
    location: Optional[str] = Field(None, max_length=200, description="项目地点")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")


class ProjectCreate(ProjectBase):
    """项目创建模型"""
    status: ProjectStatus = Field(ProjectStatus.DRAFT, description="项目状态")


class ProjectUpdate(BaseModel):
    """项目更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    coordinate_system: Optional[CoordinateSystem] = None
    reference_latitude: Optional[float] = Field(None, ge=-90, le=90)
    reference_longitude: Optional[float] = Field(None, ge=-180, le=180)
    reference_elevation: Optional[float] = None
    deviation_threshold_x: Optional[float] = Field(None, ge=0)
    deviation_threshold_y: Optional[float] = Field(None, ge=0)
    deviation_threshold_z: Optional[float] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=200)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[ProjectStatus] = None


class ProjectResponse(ProjectBase):
    """项目响应模型"""
    id: int
    status: ProjectStatus
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """项目列表响应模型"""
    total: int
    projects: list[ProjectResponse]
    skip: int
    limit: int
