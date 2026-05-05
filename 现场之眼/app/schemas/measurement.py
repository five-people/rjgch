"""
测量记录相关Pydantic模型
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MeasurementStatus(str, Enum):
    """测量状态枚举"""
    NORMAL = "normal"
    WARNING = "warning"
    ERROR = "error"


class MeasurementBase(BaseModel):
    """测量记录基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="测量点名称")
    measured_latitude: float = Field(..., ge=-90, le=90, description="实测纬度")
    measured_longitude: float = Field(..., ge=-180, le=180, description="实测经度")
    measured_elevation: Optional[float] = Field(None, description="实测高程")
    converted_x: Optional[float] = Field(None, description="转换后X坐标")
    converted_y: Optional[float] = Field(None, description="转换后Y坐标")
    converted_z: Optional[float] = Field(None, description="转换后Z坐标")
    design_x: Optional[float] = Field(None, description="设计X坐标")
    design_y: Optional[float] = Field(None, description="设计Y坐标")
    design_z: Optional[float] = Field(None, description="设计Z坐标")
    deviation_x: Optional[float] = Field(None, description="X方向偏差")
    deviation_y: Optional[float] = Field(None, description="Y方向偏差")
    deviation_z: Optional[float] = Field(None, description="Z方向偏差")
    total_deviation: Optional[float] = Field(None, ge=0, description="总偏差")
    gps_accuracy: Optional[float] = Field(None, ge=0, description="GPS精度（米）")
    device_id: Optional[str] = Field(None, max_length=100, description="设备ID")
    notes: Optional[str] = Field(None, description="备注")


class MeasurementCreate(MeasurementBase):
    """测量记录创建模型"""
    project_id: int = Field(..., gt=0, description="项目ID")
    status: MeasurementStatus = Field(MeasurementStatus.NORMAL, description="测量状态")
    is_offline: bool = Field(False, description="是否离线记录")


class MeasurementResponse(MeasurementBase):
    """测量记录响应模型"""
    id: int
    project_id: int
    user_id: int
    status: MeasurementStatus
    is_offline: bool
    measured_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MeasurementListResponse(BaseModel):
    """测量记录列表响应模型"""
    total: int
    measurements: list[MeasurementResponse]
    skip: int
    limit: int
