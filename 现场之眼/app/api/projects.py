"""
项目管理相关API
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.project import Project, ProjectStatus
from ..models.user import User
from ..schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse
from .auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建项目
    
    参数:
        project_data: 项目创建数据
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        创建的项目信息
    """
    # 检查项目编码是否已存在
    existing_project = db.query(Project).filter(Project.code == project_data.code).first()
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="项目编码已存在"
        )
    
    # 创建项目
    project = Project(
        **project_data.dict(),
        owner_id=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return project


@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    status: Optional[ProjectStatus] = Query(None, description="项目状态筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取项目列表
    
    参数:
        skip: 跳过记录数
        limit: 返回记录数
        status: 项目状态筛选
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        项目列表
    """
    query = db.query(Project)
    
    # 根据用户角色筛选
    if current_user.role.value != "admin":
        query = query.filter(Project.owner_id == current_user.id)
    
    # 根据状态筛选
    if status:
        query = query.filter(Project.status == status)
    
    total = query.count()
    projects = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "projects": projects,
        "skip": skip,
        "limit": limit
    }


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取项目详情
    
    参数:
        project_id: 项目ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        项目详情
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 权限检查
    if current_user.role.value != "admin" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问该项目"
        )
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新项目
    
    参数:
        project_id: 项目ID
        project_data: 项目更新数据
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        更新后的项目信息
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 权限检查
    if current_user.role.value != "admin" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改该项目"
        )
    
    # 更新项目
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除项目
    
    参数:
        project_id: 项目ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        无内容
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 权限检查
    if current_user.role.value != "admin" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除该项目"
        )
    
    db.delete(project)
    db.commit()
    
    return None


@router.post("/{project_id}/activate", response_model=ProjectResponse)
async def activate_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    激活项目
    
    参数:
        project_id: 项目ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        更新后的项目信息
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 权限检查
    if current_user.role.value != "admin" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权激活该项目"
        )
    
    project.status = ProjectStatus.ACTIVE
    db.commit()
    db.refresh(project)
    
    return project


@router.post("/{project_id}/complete", response_model=ProjectResponse)
async def complete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    完成项目
    
    参数:
        project_id: 项目ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        更新后的项目信息
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 权限检查
    if current_user.role.value != "admin" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权完成该项目"
        )
    
    project.status = ProjectStatus.COMPLETED
    db.commit()
    db.refresh(project)
    
    return project
