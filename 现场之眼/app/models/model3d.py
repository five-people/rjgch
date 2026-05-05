"""
3D模型模型
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from ..database import Base


class Model3DType(str, enum.Enum):
    """3D模型类型枚举"""
    BUILDING = "building"  # 建筑物
    STRUCTURE = "structure"  # 结构
    EQUIPMENT = "equipment"  # 设备
    OTHER = "other"  # 其他


class Model3DStatus(str, enum.Enum):
    """3D模型状态枚举"""
    UPLOADING = "uploading"  # 上传中
    PROCESSING = "processing"  # 处理中
    READY = "ready"  # 就绪
    ERROR = "error"  # 错误


class Model3D(Base):
    """3D模型表"""
    __tablename__ = "models_3d"
    
    id = Column(Integer, primary_key=True, index=True, comment="3D模型ID")
    name = Column(String(200), nullable=False, index=True, comment="模型名称")
    code = Column(String(50), comment="模型编码")
    description = Column(Text, comment="模型描述")
    
    # 模型信息
    model_type = Column(Enum(Model3DType), default=Model3DType.BUILDING, comment="模型类型")
    file_name = Column(String(255), nullable=False, comment="文件名")
    file_path = Column(String(500), nullable=False, comment="文件路径")
    file_size = Column(Float, comment="文件大小（字节）")
    file_format = Column(String(20), comment="文件格式")
    
    # 模型坐标信息
    origin_x = Column(Float, comment="原点X坐标")
    origin_y = Column(Float, comment="原点Y坐标")
    origin_z = Column(Float, comment="原点Z坐标")
    scale = Column(Float, default=1.0, comment="模型比例")
    rotation_x = Column(Float, default=0.0, comment="X轴旋转角度（度）")
    rotation_y = Column(Float, default=0.0, comment="Y轴旋转角度（度）")
    rotation_z = Column(Float, default=0.0, comment="Z轴旋转角度（度）")
    
    # 处理状态
    status = Column(Enum(Model3DStatus), default=Model3DStatus.UPLOADING, comment="处理状态")
    error_message = Column(Text, comment="错误消息")
    
    # AR相关
    is_ar_enabled = Column(Boolean, default=True, comment="是否启用AR")
    ar_opacity = Column(Float, default=0.8, comment="AR透明度")
    
    # 外键
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="项目ID")
    uploaded_by = Column(Integer, ForeignKey("users.id"), comment="上传人ID")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关系
    project = relationship("Project", back_populates="models_3d")
    
    def __repr__(self):
        return f"<Model3D(id={self.id}, name={self.name}, type={self.model_type})>"
