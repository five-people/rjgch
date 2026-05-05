"""
认证服务
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..config import settings
from ..models.user import User, UserRole


class AuthService:
    """认证服务类"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        验证密码
        
        参数:
            plain_password: 明文密码
            hashed_password: 加密密码
            
        返回:
            密码是否匹配
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """
        加密密码
        
        参数:
            password: 明文密码
            
        返回:
            加密后的密码
        """
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        创建访问令牌
        
        参数:
            data: 要编码的数据
            expires_delta: 过期时间增量
            
        返回:
            JWT令牌
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict) -> str:
        """
        创建刷新令牌
        
        参数:
            data: 要编码的数据
            
        返回:
            JWT刷新令牌
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> dict:
        """
        解码令牌
        
        参数:
            token: JWT令牌
            
        返回:
            解码后的数据
            
        异常:
            JWTError: 令牌无效
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError as e:
            raise JWTError(f"令牌解码失败: {str(e)}")
    
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        """
        验证用户
        
        参数:
            db: 数据库会话
            username: 用户名
            password: 密码
            
        返回:
            用户对象，验证失败返回None
        """
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_user(self, db: Session, username: str, email: str, password: str, 
                   full_name: Optional[str] = None, phone: Optional[str] = None,
                   role: UserRole = UserRole.WORKER) -> User:
        """
        创建用户
        
        参数:
            db: 数据库会话
            username: 用户名
            email: 邮箱
            password: 密码
            full_name: 真实姓名
            phone: 手机号
            role: 用户角色
            
        返回:
            创建的用户对象
        """
        hashed_password = self.get_password_hash(password)
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            phone=phone,
            role=role,
            is_active=True,
            is_verified=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_current_user(self, db: Session, token: str) -> User:
        """
        获取当前用户
        
        参数:
            db: 数据库会话
            token: JWT令牌
            
        返回:
            当前用户对象
            
        异常:
            JWTError: 令牌无效
        """
        payload = self.decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise JWTError("令牌中缺少用户名")
        
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise JWTError("用户不存在")
        return user


# 创建全局认证服务实例
auth_service = AuthService()
