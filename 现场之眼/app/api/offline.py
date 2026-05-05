"""
离线管理相关API
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta

from ..database import get_db
from ..models.offline_cache import OfflineCache, CacheType, CacheStatus
from ..models.user import User
from ..models.project import Project
from ..models.control_point import ControlPoint
from ..models.design_coordinate import DesignCoordinate
from ..schemas.offline import OfflineCacheCreate, OfflineCacheUpdate, OfflineCacheResponse, OfflineCacheListResponse
from ..config import settings
from .auth import get_current_active_user

router = APIRouter()


async def _prepare_cache_data(project_id: int, cache_type: CacheType, db: Session) -> dict:
    """
    准备缓存数据
    
    参数:
        project_id: 项目ID
        cache_type: 缓存类型
        db: 数据库会话
        
    返回:
        缓存数据
    """
    if cache_type == CacheType.CONTROL_POINT:
        control_points = db.query(ControlPoint).filter(
            ControlPoint.project_id == project_id
        ).all()
        return {
            "control_points": [
                {
                    "id": cp.id,
                    "name": cp.name,
                    "code": cp.code,
                    "latitude": cp.latitude,
                    "longitude": cp.longitude,
                    "elevation": cp.elevation,
                    "design_x": cp.design_x,
                    "design_y": cp.design_y,
                    "design_z": cp.design_z
                }
                for cp in control_points
            ]
        }
    
    elif cache_type == CacheType.DESIGN_COORDINATE:
        design_coords = db.query(DesignCoordinate).filter(
            DesignCoordinate.project_id == project_id
        ).all()
        return {
            "design_coordinates": [
                {
                    "id": dc.id,
                    "name": dc.name,
                    "code": dc.code,
                    "design_x": dc.design_x,
                    "design_y": dc.design_y,
                    "design_z": dc.design_z,
                    "latitude": dc.latitude,
                    "longitude": dc.longitude,
                    "elevation": dc.elevation
                }
                for dc in design_coords
            ]
        }
    
    elif cache_type == CacheType.PROJECT_DATA:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目不存在"
            )
        return {
            "project": {
                "id": project.id,
                "name": project.name,
                "code": project.code,
                "coordinate_system": project.coordinate_system.value,
                "reference_latitude": project.reference_latitude,
                "reference_longitude": project.reference_longitude,
                "reference_elevation": project.reference_elevation,
                "deviation_threshold_x": project.deviation_threshold_x,
                "deviation_threshold_y": project.deviation_threshold_y,
                "deviation_threshold_z": project.deviation_threshold_z
            }
        }
    
    else:
        return {}


@router.post("/prepare", status_code=status.HTTP_201_CREATED)
async def prepare_offline_data(
    project_id: int,
    cache_types: List[CacheType] = Query(..., description="缓存类型列表"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    准备离线数据
    
    参数:
        project_id: 项目ID
        cache_types: 缓存类型列表
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        准备结果
    """
    # 验证项目是否存在
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 删除旧的缓存
    old_caches = db.query(OfflineCache).filter(
        OfflineCache.project_id == project_id,
        OfflineCache.user_id == current_user.id
    ).all()
    
    for old_cache in old_caches:
        db.delete(old_cache)
    
    # 创建新的缓存记录
    created_caches = []
    for cache_type in cache_types:
        # 根据缓存类型准备数据
        cache_data = await _prepare_cache_data(project_id, cache_type, db)
        
        # 创建缓存记录
        cache = OfflineCache(
            name=f"{project.code}_{cache_type.value}",
            cache_type=cache_type,
            cache_key=f"{project_id}_{current_user.id}_{cache_type.value}",
            cache_data=cache_data,
            status=CacheStatus.SYNCED,
            synced_at=datetime.utcnow(),
            sync_version=str(datetime.utcnow().timestamp()),
            expires_at=datetime.utcnow() + timedelta(days=30),
            project_id=project_id,
            user_id=current_user.id
        )
        
        db.add(cache)
        created_caches.append(cache)
    
    db.commit()
    
    return {
        "success": True,
        "message": "离线数据准备成功",
        "created_caches": len(created_caches),
        "cache_types": [ct.value for ct in cache_types]
    }


@router.get("/", response_model=OfflineCacheListResponse)
async def list_caches(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    project_id: Optional[int] = Query(None, description="项目ID筛选"),
    cache_type: Optional[CacheType] = Query(None, description="缓存类型筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取离线缓存列表
    
    参数:
        skip: 跳过记录数
        limit: 返回记录数
        project_id: 项目ID筛选
        cache_type: 缓存类型筛选
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        离线缓存列表
    """
    query = db.query(OfflineCache).filter(OfflineCache.user_id == current_user.id)
    
    if project_id:
        query = query.filter(OfflineCache.project_id == project_id)
    
    if cache_type:
        query = query.filter(OfflineCache.cache_type == cache_type)
    
    total = query.count()
    caches = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "caches": caches,
        "skip": skip,
        "limit": limit
    }


@router.get("/{cache_id}", response_model=OfflineCacheResponse)
async def get_cache(
    cache_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取离线缓存详情
    
    参数:
        cache_id: 缓存ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        离线缓存详情
    """
    cache = db.query(OfflineCache).filter(
        OfflineCache.id == cache_id,
        OfflineCache.user_id == current_user.id
    ).first()
    
    if not cache:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="离线缓存不存在"
        )
    
    # 更新最后访问时间
    cache.last_accessed = datetime.utcnow()
    db.commit()
    
    return cache


@router.put("/{cache_id}", response_model=OfflineCacheResponse)
async def update_cache(
    cache_id: int,
    cache_data: OfflineCacheUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    更新离线缓存
    
    参数:
        cache_id: 缓存ID
        cache_data: 缓存更新数据
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        更新后的缓存信息
    """
    cache = db.query(OfflineCache).filter(
        OfflineCache.id == cache_id,
        OfflineCache.user_id == current_user.id
    ).first()
    
    if not cache:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="离线缓存不存在"
        )
    
    # 更新缓存
    update_data = cache_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cache, field, value)
    
    db.commit()
    db.refresh(cache)
    
    return cache


@router.delete("/{cache_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cache(
    cache_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除离线缓存
    
    参数:
        cache_id: 缓存ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        无内容
    """
    cache = db.query(OfflineCache).filter(
        OfflineCache.id == cache_id,
        OfflineCache.user_id == current_user.id
    ).first()
    
    if not cache:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="离线缓存不存在"
        )
    
    # 删除文件
    if cache.file_path:
        import os
        if os.path.exists(cache.file_path):
            os.remove(cache.file_path)
    
    db.delete(cache)
    db.commit()
    
    return None


@router.get("/status/project/{project_id}", response_model=dict)
async def get_project_cache_status(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取项目缓存状态
    
    参数:
        project_id: 项目ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        项目缓存状态
    """
    # 验证项目是否存在
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 查询项目的所有缓存
    caches = db.query(OfflineCache).filter(
        OfflineCache.project_id == project_id,
        OfflineCache.user_id == current_user.id
    ).all()
    
    # 统计缓存状态
    total = len(caches)
    synced = len([c for c in caches if c.status == CacheStatus.SYNCED])
    outdated = len([c for c in caches if c.status == CacheStatus.OUTDATED])
    syncing = len([c for c in caches if c.status == CacheStatus.SYNCING])
    error = len([c for c in caches if c.status == CacheStatus.ERROR])
    
    return {
        "project_id": project_id,
        "project_name": project.name,
        "total_caches": total,
        "synced": synced,
        "outdated": outdated,
        "syncing": syncing,
        "error": error,
        "is_ready": total > 0 and syncing == 0 and error == 0
    }


@router.post("/clear/project/{project_id}", response_model=dict)
async def clear_project_cache(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    清除项目缓存
    
    参数:
        project_id: 项目ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        清除结果
    """
    # 验证项目是否存在
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 查询项目的所有缓存
    caches = db.query(OfflineCache).filter(
        OfflineCache.project_id == project_id,
        OfflineCache.user_id == current_user.id
    ).all()
    
    # 删除缓存
    deleted_count = 0
    for cache in caches:
        # 删除文件
        if cache.file_path:
            import os
            if os.path.exists(cache.file_path):
                os.remove(cache.file_path)
        
        db.delete(cache)
        deleted_count += 1
    
    db.commit()
    
    return {
        "success": True,
        "deleted_count": deleted_count,
        "message": f"成功清除{deleted_count}个缓存"
    }
