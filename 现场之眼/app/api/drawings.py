"""
图纸管理相关API
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import os
import shutil
from datetime import datetime

from ..database import get_db
from ..models.drawing import Drawing, DrawingStatus
from ..models.user import User
from ..models.project import Project
from ..schemas.drawing import DrawingCreate, DrawingUpdate, DrawingResponse, DrawingListResponse
from ..config import settings
from .auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=DrawingResponse, status_code=status.HTTP_201_CREATED)
async def create_drawing(
    drawing_data: DrawingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建图纸记录
    
    参数:
        drawing_data: 图纸创建数据
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        创建的图纸记录
    """
    # 检查项目是否存在
    project = db.query(Project).filter(Project.id == drawing_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 创建图纸记录
    drawing = Drawing(
        **drawing_data.dict(),
        uploaded_by=current_user.id,
        status=DrawingStatus.READY
    )
    db.add(drawing)
    db.commit()
    db.refresh(drawing)
    
    return drawing


@router.post("/upload", response_model=DrawingResponse, status_code=status.HTTP_201_CREATED)
async def upload_drawing(
    project_id: int,
    name: str = Query(..., description="图纸名称"),
    drawing_type: str = Query("plan", description="图纸类型"),
    file: UploadFile = File(..., description="图纸文件"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    上传图纸文件
    
    参数:
        project_id: 项目ID
        name: 图纸名称
        drawing_type: 图纸类型
        file: 图纸文件
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        创建的图纸记录
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
    upload_dir = os.path.join(settings.UPLOAD_DIR, "drawings", str(project_id))
    os.makedirs(upload_dir, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, file_name)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    
    # 创建图纸记录
    drawing = Drawing(
        name=name,
        file_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        file_format=file_ext[1:],
        drawing_type=drawing_type,
        project_id=project_id,
        uploaded_by=current_user.id,
        status=DrawingStatus.READY
    )
    db.add(drawing)
    db.commit()
    db.refresh(drawing)
    
    return drawing


@router.get("/", response_model=DrawingListResponse)
async def list_drawings(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    project_id: Optional[int] = Query(None, description="项目ID筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取图纸列表
    
    参数:
        skip: 跳过记录数
        limit: 返回记录数
        project_id: 项目ID筛选
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        图纸列表
    """
    query = db.query(Drawing)
    
    if project_id:
        query = query.filter(Drawing.project_id == project_id)
    
    total = query.count()
    drawings = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "drawings": drawings,
        "skip": skip,
        "limit": limit
    }


@router.get("/{drawing_id}", response_model=DrawingResponse)
async def get_drawing(
    drawing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取图纸详情
    
    参数:
        drawing_id: 图纸ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        图纸详情
    """
    drawing = db.query(Drawing).filter(Drawing.id == drawing_id).first()
    if not drawing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图纸不存在"
        )
    
    return drawing


@router.put("/{drawing_id}", response_model=DrawingResponse)
async def update_drawing(
    drawing_id: int,
    drawing_data: DrawingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新图纸
    
    参数:
        drawing_id: 图纸ID
        drawing_data: 图纸更新数据
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        更新后的图纸信息
    """
    drawing = db.query(Drawing).filter(Drawing.id == drawing_id).first()
    if not drawing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图纸不存在"
        )
    
    # 更新图纸
    update_data = drawing_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(drawing, field, value)
    
    db.commit()
    db.refresh(drawing)
    
    return drawing


@router.delete("/{drawing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drawing(
    drawing_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除图纸
    
    参数:
        drawing_id: 图纸ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        无内容
    """
    drawing = db.query(Drawing).filter(Drawing.id == drawing_id).first()
    if not drawing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图纸不存在"
        )
    
    # 删除文件
    if os.path.exists(drawing.file_path):
        os.remove(drawing.file_path)
    
    db.delete(drawing)
    db.commit()
    
    return None
