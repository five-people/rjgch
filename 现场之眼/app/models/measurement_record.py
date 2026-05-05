"""
测量记录模型
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from ..database import Base


class MeasurementStatus(str, enum.Enum):
    """测量状态枚举"""
    NORMAL = "normal"  # 正常
    WARNING = "warning"  # 警告
    ERROR = "error"  # 错误


class MeasurementRecord(Base):
    """测量记录表"""
    __tablename__ = "measurement_records"
    
    id = Column(Integer, primary_key=True, index=True, comment="测量记录ID")
    name = Column(String(100), nullable=False, index=True, comment="测量点名称")
    
    # 实测坐标（GPS获取）
    measured_latitude = Column(Float, nullable=False, comment="实测纬度")
    measured_longitude = Column(Float, nullable=False, comment="实测经度")
    measured_elevation = Column(Float, comment="实测高程")
    
    # 转换后的设计坐标
    converted_x = Column(Float, comment="转换后X坐标")
    converted_y = Column(Float, comment="转换后Y坐标")
    converted_z = Column(Float, comment="转换后Z坐标")
    
    # 设计坐标
    design_x = Column(Float, comment="设计X坐标")
    design_y = Column(Float, comment="设计Y坐标")
    design_z = Column(Float, comment="设计Z坐标")
    
    # 偏差
    deviation_x = Column(Float, comment="X方向偏差")
    deviation_y = Column(Float, comment="Y方向偏差")
    deviation_z = Column(Float, comment="Z方向偏差")
    total_deviation = Column(Float, comment="总偏差")
    
    # 状态
    status = Column(Enum(MeasurementStatus), default=MeasurementStatus.NORMAL, comment="测量状态")
    is_offline = Column(Boolean, default=False, comment="是否离线记录")
    
    # GPS精度
    gps_accuracy = Column(Float, comment="GPS精度（米）")
    
    # 设备信息
    device_id = Column(String(100), comment="设备ID")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 外键
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="项目ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="测量员ID")
    
    # 时间戳
    measured_at = Column(DateTime(timezone=True), server_default=func.now(), comment="测量时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关系
    project = relationship("Project", back_populates="measurement_records")
    user = relationship("User", back_populates="measurement_records")
    
    def __repr__(self):
        return f"<MeasurementRecord(id={self.id}, name={self.name}, status={self.status})>"
