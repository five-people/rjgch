"""
3D模型相关Pydantic模型
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class Model3DType(str, Enum):
    """3D模型类型枚举"""
    BUILDING = "building"
    STRUCTURE = "structure"
    EQUIPMENT = "equipment"
    OTHER = "other"


class Model3DStatus(str, Enum):
    """3D模型状态枚举"""
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


class Model3DBase(BaseModel):
    """3D模型基础模型"""
    name: str = Field(..., min_length=1, max_length=200, description="模型名称")
    code: Optional[str] = Field(None, max_length=50, description="模型编码")
    description: Optional[str] = Field(None, description="模型描述")
    model_type: Model3DType = Field(Model3DType.BUILDING, description="模型类型")
    file_name: str = Field(..., max_length=255, description="文件名")
    file_path: str = Field(..., max_length=500, description="文件路径")
    file_size: Optional[float] = Field(None, ge=0, description="文件大小（字节）")
    file_format: Optional[str] = Field(None, max_length=20, description="文件格式")
    origin_x: Optional[float] = Field(None, description="原点X坐标")
    origin_y: Optional[float] = Field(None, description="原点Y坐标")
    origin_z: Optional[float] = Field(None, description="原点Z坐标")
    scale: float = Field(1.0, gt=0, description="模型比例")
    rotation_x: float = Field(0.0, description="X轴旋转角度（度）")
    rotation_y: float = Field(0.0, description="Y轴旋转角度（度）")
    rotation_z: float = Field(0.0, description="Z轴旋转角度（度）")
    is_ar_enabled: bool = Field(True, description="是否启用AR")
    ar_opacity: float = Field(0.8, ge=0, le=1, description="AR透明度")


class Model3DCreate(Model3DBase):
    """3D模型创建模型"""
    project_id: int = Field(..., gt=0, description="项目ID")


class Model3DUpdate(BaseModel):
    """3D模型更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    code: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    model_type: Optional[Model3DType] = None
    origin_x: Optional[float] = None
    origin_y: Optional[float] = None
    origin_z: Optional[float] = None
    scale: Optional[float] = Field(None, gt=0)
    rotation_x: Optional[float] = None
    rotation_y: Optional[float] = None
    rotation_z: Optional[float] = None
    is_ar_enabled: Optional[bool] = None
    ar_opacity: Optional[float] = Field(None, ge=0, le=1)


class Model3DResponse(Model3DBase):
    """3D模型响应模型"""
    id: int
    status: Model3DStatus
    project_id: int
    uploaded_by: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Model3DListResponse(BaseModel):
    """3D模型列表响应模型"""
    total: int
    models_3d: list[Model3DResponse]
    skip: int
    limit: int
