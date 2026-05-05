"""
图纸模型
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from ..database import Base


class DrawingType(str, enum.Enum):
    """图纸类型枚举"""
    PLAN = "plan"  # 平面图
    ELEVATION = "elevation"  # 立面图
    SECTION = "section"  # 剖面图
    DETAIL = "detail"  # 详图
    OTHER = "other"  # 其他


class DrawingStatus(str, enum.Enum):
    """图纸状态枚举"""
    UPLOADING = "uploading"  # 上传中
    PROCESSING = "processing"  # 处理中
    READY = "ready"  # 就绪
    ERROR = "error"  # 错误


class Drawing(Base):
    """图纸表"""
    __tablename__ = "drawings"
    
    id = Column(Integer, primary_key=True, index=True, comment="图纸ID")
    name = Column(String(200), nullable=False, index=True, comment="图纸名称")
    code = Column(String(50), comment="图纸编码")
    description = Column(Text, comment="图纸描述")
    
    # 图纸信息
    drawing_type = Column(Enum(DrawingType), default=DrawingType.PLAN, comment="图纸类型")
    file_name = Column(String(255), nullable=False, comment="文件名")
    file_path = Column(String(500), nullable=False, comment="文件路径")
    file_size = Column(Float, comment="文件大小（字节）")
    file_format = Column(String(20), comment="文件格式")
    
    # 图纸坐标信息
    origin_x = Column(Float, comment="原点X坐标")
    origin_y = Column(Float, comment="原点Y坐标")
    scale = Column(Float, default=1.0, comment="图纸比例")
    rotation = Column(Float, default=0.0, comment="旋转角度（度）")
    
    # 处理状态
    status = Column(Enum(DrawingStatus), default=DrawingStatus.UPLOADING, comment="处理状态")
    error_message = Column(Text, comment="错误消息")
    
    # AR相关
    is_ar_enabled = Column(Boolean, default=True, comment="是否启用AR")
    ar_opacity = Column(Float, default=0.7, comment="AR透明度")
    
    # 外键
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="项目ID")
    uploaded_by = Column(Integer, ForeignKey("users.id"), comment="上传人ID")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关系
    project = relationship("Project", back_populates="drawings")
    
    def __repr__(self):
        return f"<Drawing(id={self.id}, name={self.name}, type={self.drawing_type})>"
