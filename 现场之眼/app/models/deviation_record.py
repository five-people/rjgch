"""
偏差记录模型
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from ..database import Base


class DeviationLevel(str, enum.Enum):
    """偏差级别枚举"""
    NORMAL = "normal"  # 正常
    WARNING = "warning"  # 警告
    CRITICAL = "critical"  # 严重


class DeviationRecord(Base):
    """偏差记录表"""
    __tablename__ = "deviation_records"
    
    id = Column(Integer, primary_key=True, index=True, comment="偏差记录ID")
    name = Column(String(100), nullable=False, index=True, comment="偏差点名称")
    
    # 偏差信息
    deviation_x = Column(Float, nullable=False, comment="X方向偏差")
    deviation_y = Column(Float, nullable=False, comment="Y方向偏差")
    deviation_z = Column(Float, comment="Z方向偏差")
    total_deviation = Column(Float, nullable=False, comment="总偏差")
    
    # 阈值信息
    threshold_x = Column(Float, comment="X方向阈值")
    threshold_y = Column(Float, comment="Y方向阈值")
    threshold_z = Column(Float, comment="Z方向阈值")
    total_threshold = Column(Float, comment="总阈值")
    
    # 偏差级别
    deviation_level = Column(Enum(DeviationLevel), default=DeviationLevel.NORMAL, comment="偏差级别")
    
    # 预警信息
    is_alert = Column(Boolean, default=False, comment="是否预警")
    alert_message = Column(Text, comment="预警消息")
    
    # 关联测量记录
    measurement_record_id = Column(Integer, ForeignKey("measurement_records.id"), comment="测量记录ID")
    
    # 处理状态
    is_resolved = Column(Boolean, default=False, comment="是否已解决")
    resolved_at = Column(DateTime(timezone=True), comment="解决时间")
    resolved_by = Column(Integer, ForeignKey("users.id"), comment="解决人ID")
    resolution_notes = Column(Text, comment="解决备注")
    
    # 外键
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, comment="项目ID")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    
    # 关系
    project = relationship("Project", back_populates="deviation_records")
    
    def __repr__(self):
        return f"<DeviationRecord(id={self.id}, name={self.name}, level={self.deviation_level})>"
