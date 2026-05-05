"""
测量记录相关API
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models.measurement_record import MeasurementRecord, MeasurementStatus
from ..models.user import User
from ..models.project import Project
from ..schemas.measurement import MeasurementCreate, MeasurementResponse, MeasurementListResponse
from .auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=MeasurementResponse, status_code=status.HTTP_201_CREATED)
async def create_measurement(
    measurement_data: MeasurementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建测量记录
    
    参数:
        measurement_data: 测量记录数据
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        创建的测量记录
    """
    # 检查项目是否存在
    project = db.query(Project).filter(Project.id == measurement_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 创建测量记录
    measurement = MeasurementRecord(
        **measurement_data.dict(),
        user_id=current_user.id
    )
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    
    return measurement


@router.get("/", response_model=MeasurementListResponse)
async def list_measurements(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    project_id: Optional[int] = Query(None, description="项目ID筛选"),
    status: Optional[MeasurementStatus] = Query(None, description="状态筛选"),
    is_offline: Optional[bool] = Query(None, description="离线记录筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取测量记录列表
    
    参数:
        skip: 跳过记录数
        limit: 返回记录数
        project_id: 项目ID筛选
        status: 状态筛选
        is_offline: 离线记录筛选
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        测量记录列表
    """
    query = db.query(MeasurementRecord)
    
    # 筛选条件
    if project_id:
        query = query.filter(MeasurementRecord.project_id == project_id)
    
    if status:
        query = query.filter(MeasurementRecord.status == status)
    
    if is_offline is not None:
        query = query.filter(MeasurementRecord.is_offline == is_offline)
    
    total = query.count()
    measurements = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "measurements": measurements,
        "skip": skip,
        "limit": limit
    }


@router.get("/{measurement_id}", response_model=MeasurementResponse)
async def get_measurement(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取测量记录详情
    
    参数:
        measurement_id: 测量记录ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        测量记录详情
    """
    measurement = db.query(MeasurementRecord).filter(MeasurementRecord.id == measurement_id).first()
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="测量记录不存在"
        )
    
    return measurement


@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_measurement(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    删除测量记录
    
    参数:
        measurement_id: 测量记录ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        无内容
    """
    measurement = db.query(MeasurementRecord).filter(MeasurementRecord.id == measurement_id).first()
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="测量记录不存在"
        )
    
    db.delete(measurement)
    db.commit()
    
    return None


@router.post("/sync-offline", response_model=dict)
async def sync_offline_measurements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    同步离线测量记录
    
    参数:
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        同步结果
    """
    # 查询所有离线测量记录
    offline_measurements = db.query(MeasurementRecord).filter(
        MeasurementRecord.is_offline == True,
        MeasurementRecord.user_id == current_user.id
    ).all()
    
    synced_count = 0
    
    for measurement in offline_measurements:
        measurement.is_offline = False
        synced_count += 1
    
    db.commit()
    
    return {
        "success": True,
        "synced_count": synced_count,
        "message": f"成功同步{synced_count}条离线测量记录"
    }


@router.get("/statistics/summary", response_model=dict)
async def get_measurement_statistics(
    project_id: Optional[int] = Query(None, description="项目ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取测量统计信息
    
    参数:
        project_id: 项目ID
        db: 数据库会话
        current_user: 当前用户
        
    返回:
        统计信息
    """
    query = db.query(MeasurementRecord)
    
    if project_id:
        query = query.filter(MeasurementRecord.project_id == project_id)
    
    total = query.count()
    normal_count = query.filter(MeasurementRecord.status == MeasurementStatus.NORMAL).count()
    warning_count = query.filter(MeasurementRecord.status == MeasurementStatus.WARNING).count()
    error_count = query.filter(MeasurementRecord.status == MeasurementStatus.ERROR).count()
    offline_count = query.filter(MeasurementRecord.is_offline == True).count()
    
    return {
        "total": total,
        "normal_count": normal_count,
        "warning_count": warning_count,
        "error_count": error_count,
        "offline_count": offline_count
    }
