"""
设计坐标模型
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..database import Base


class DesignCoordinate(Base):
    """设计坐标表"""
    __tablename__ = "design_coordinates"
    
    id = Column(Integer, primary_key=True, index=True, comment="设计坐标ID")
    name = Column(String(100), nullable=False, index=True, comment="坐标点名称")
    code = Column(String(50), comment="坐标点编码")
    description = Column(Text, comment="坐标点描述")
    
    # 设计坐标
    design_x = Column(Float, nullable=False, comment="设计X坐标")
    design_y = Column(Float, nullable=False, comment="设计Y坐标")
    design_z = Column(Float, comment="设计Z坐标")
    
    # 转换后的地理坐标
    latitude = Column(Float, comment="转换后纬度")
    longitude = Column(Float, comment="转换后经度")
    elevation = Column(Float, comment="转换后高程")
    
    # 坐标类型
    coordinate_type = Column(String(50), comment="坐标类型")
    
    # 外键
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="项目ID")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关系
    project = relationship("Project", back_populates="design_coordinates")
    
    def __repr__(self):
        return f"<DesignCoordinate(id={self.id}, name={self.name}, x={self.design_x}, y={self.design_y})>"
