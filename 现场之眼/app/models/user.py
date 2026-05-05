"""
用户模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from ..database import Base


class UserRole(str, enum.Enum):
    """用户角色枚举"""
    ADMIN = "admin"  # 管理员
    SUPERVISOR = "supervisor"  # 技术负责人
    WORKER = "worker"  # 施工员/测量员


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    hashed_password = Column(String(255), nullable=False, comment="加密密码")
    full_name = Column(String(100), comment="真实姓名")
    phone = Column(String(20), comment="手机号")
    role = Column(Enum(UserRole), default=UserRole.WORKER, nullable=False, comment="用户角色")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_verified = Column(Boolean, default=False, comment="是否验证")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    last_login = Column(DateTime(timezone=True), comment="最后登录时间")
    
    # 关系
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    measurement_records = relationship("MeasurementRecord", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
