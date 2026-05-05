"""
图纸相关Pydantic模型
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class DrawingType(str, Enum):
    """图纸类型枚举"""
    PLAN = "plan"
    ELEVATION = "elevation"
    SECTION = "section"
    DETAIL = "detail"
    OTHER = "other"


class DrawingStatus(str, Enum):
    """图纸状态枚举"""
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


class DrawingBase(BaseModel):
    """图纸基础模型"""
    name: str = Field(..., min_length=1, max_length=200, description="图纸名称")
    code: Optional[str] = Field(None, max_length=50, description="图纸编码")
    description: Optional[str] = Field(None, description="图纸描述")
    drawing_type: DrawingType = Field(DrawingType.PLAN, description="图纸类型")
    file_name: str = Field(..., max_length=255, description="文件名")
    file_path: str = Field(..., max_length=500, description="文件路径")
    file_size: Optional[float] = Field(None, ge=0, description="文件大小（字节）")
    file_format: Optional[str] = Field(None, max_length=20, description="文件格式")
    origin_x: Optional[float] = Field(None, description="原点X坐标")
    origin_y: Optional[float] = Field(None, description="原点Y坐标")
    scale: float = Field(1.0, gt=0, description="图纸比例")
    rotation: float = Field(0.0, description="旋转角度（度）")
    is_ar_enabled: bool = Field(True, description="是否启用AR")
    ar_opacity: float = Field(0.7, ge=0, le=1, description="AR透明度")


class DrawingCreate(DrawingBase):
    """图纸创建模型"""
    project_id: int = Field(..., gt=0, description="项目ID")


class DrawingUpdate(BaseModel):
    """图纸更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    drawing_type: Optional[DrawingType] = None
    origin_x: Optional[float] = None
    origin_y: Optional[float] = None
    scale: Optional[float] = Field(None, gt=0)
    rotation: Optional[float] = None
    is_ar_enabled: Optional[bool] = None
    ar_opacity: Optional[float] = Field(None, ge=0, le=1)


class DrawingResponse(DrawingBase):
    """图纸响应模型"""
    id: int
    status: DrawingStatus
    project_id: int
    uploaded_by: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DrawingListResponse(BaseModel):
    """图纸列表响应模型"""
    total: int
    drawings: list[DrawingResponse]
    skip: int
    limit: int
