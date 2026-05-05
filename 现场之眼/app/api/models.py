"""
3D模型管理相关API
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import os
from datetime import datetime

from ..database import get_db
from ..models.model3d import Model3D, Model3DStatus
from ..models.user import User
from ..models.project import Project
from ..schemas.model3d import Model3DCreate, Model3DUpdate, Model3DResponse, Model3DListResponse
from ..config import settings
from .auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=Model3DResponse, status_code=status.HTTP_201_CREATED)
async def create_model(
    model_data: Model3DCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建3D模型记录
    
    参数:
        model_data: 3D模型创建数据
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        创建的3D模型记录
    """
    # 检查项目是否存在
    project = db.query(Project).filter(Project.id == model_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 创建3D模型记录
    model = Model3D(
        **model_data.dict(),
        uploaded_by=current_user.id,
        status=Model3DStatus.READY
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    
    return model


@router.post("/upload", response_model=Model3DResponse, status_code=status.HTTP_201_CREATED)
async def upload_model(
    project_id: int,
    name: str = Query(..., description="模型名称"),
    model_type: str = Query("building", description="模型类型"),
    file: UploadFile = File(..., description="3D模型文件"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    上传3D模型文件
    
    参数:
        project_id: 项目ID
        name: 模型名称
        model_type: 模型类型
        file: 3D模型文件
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        创建的3D模型记录
    """
    # 检查项目是否存在
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 检查文件类型
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型: {file_ext}"
        )
    
    # 检查文件大小
    file_size = 0
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小超过限制: {settings.MAX_FILE_SIZE}字节"
        )
    
    # 创建上传目录
    upload_dir = os.path.join(settings.UPLOAD_DIR, "models_3d", str(project_id))
    os.makedirs(upload_dir, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, file_name)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    
    # 创建3D模型记录
    model = Model3D(
        name=name,
        file_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        file_format=file_ext[1:],
        model_type=model_type,
        project_id=project_id,
        uploaded_by=current_user.id,
        status=Model3DStatus.READY
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    
    return model


@router.get("/", response_model=Model3DListResponse)
async def list_models(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    project_id: Optional[int] = Query(None, description="项目ID筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取3D模型列表
    
    参数:
        skip: 跳过记录数
        limit: 返回记录数
        project_id: 项目ID筛选
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        3D模型列表
    """
    query = db.query(Model3D)
    
    if project_id:
        query = query.filter(Model3D.project_id == project_id)
    
    total = query.count()
    models = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "models_3d": models,
        "skip": skip,
        "limit": limit
    }


@router.get("/{model_id}", response_model=Model3DResponse)
async def get_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取3D模型详情
    
    参数:
        model_id: 3D模型ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        3D模型详情
    """
    model = db.query(Model3D).filter(Model3D.id == model_id).first()
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="3D模型不存在"
        )
    
    return model


@router.put("/{model_id}", response_model=Model3DResponse)
async def update_model(
    model_id: int,
    model_data: Model3DUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新3D模型
    
    参数:
        model_id: 3D模型ID
        model_data: 3D模型更新数据
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        更新后的3D模型信息
    """
    model = db.query(Model3D).filter(Model3D.id == model_id).first()
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="3D模型不存在"
        )
    
    # 更新3D模型
    update_data = model_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(model, field, value)
    
    db.commit()
    db.refresh(model)
    
    return model


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除3D模型
    
    参数:
        model_id: 3D模型ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        无内容
    """
    model = db.query(Model3D).filter(Model3D.id == model_id).first()
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="3D模型不存在"
        )
    
    # 删除文件
    if os.path.exists(model.file_path):
        os.remove(model.file_path)
    
    db.delete(model)
    db.commit()
    
    return None
