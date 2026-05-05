"""
控制点模型
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..database import Base


class ControlPoint(Base):
    """控制点表"""
    __tablename__ = "control_points"
    
    id = Column(Integer, primary_key=True, index=True, comment="控制点ID")
    name = Column(String(100), nullable=False, index=True, comment="控制点名称")
    code = Column(String(50), comment="控制点编码")
    description = Column(Text, comment="控制点描述")
    
    # 坐标信息（现场坐标系）
    latitude = Column(Float, nullable=False, comment="纬度")
    longitude = Column(Float, nullable=False, comment="经度")
    elevation = Column(Float, comment="高程")
    
    # 坐标信息（设计坐标系）
    design_x = Column(Float, comment="设计X坐标")
    design_y = Column(Float, comment="设计Y坐标")
    design_z = Column(Float, comment="设计Z坐标")
    
    # 精度信息
    accuracy = Column(Float, comment="精度（米）")
    measurement_date = Column(DateTime(timezone=True), comment="测量日期")
    
    # 控制点类型
    point_type = Column(String(50), comment="控制点类型")
    
    # 外键
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="项目ID")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关系
    project = relationship("Project", back_populates="control_points")
    
    def __repr__(self):
        return f"<ControlPoint(id={self.id}, name={self.name}, lat={self.latitude}, lon={self.longitude})>"
