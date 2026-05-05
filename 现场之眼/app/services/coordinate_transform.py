"""
坐标转换服务
"""

import math
from typing import List, Tuple, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class GPSPoint:
    """GPS坐标点"""
    latitude: float  # 纬度
    longitude: float  # 经度
    elevation: float = 0.0  # 高程


@dataclass
class CoordinatePoint:
    """局部坐标点"""
    x: float  # X坐标
    y: float  # Y坐标
    z: float = 0.0  # Z坐标


class CoordinateTransformService:
    """坐标转换服务类"""
    
    def __init__(self, precision: int = 6):
        """
        初始化坐标转换服务
        
        参数:
            precision: 坐标精度（小数位数）
        """
        self.precision = precision
    
    def resection(self, 
                  control_points: List[Tuple[GPSPoint, CoordinatePoint]],
                  method: str = "least_squares") -> dict:
        """
        后方交汇算法 - 计算坐标转换参数
        
        参数:
            control_points: 控制点列表 [(GPS点, 设计坐标点), ...]
            method: 计算方法 ("least_squares" 或 "affine")
            
        返回:
            转换参数字典
        """
        if len(control_points) < 3:
            raise ValueError("至少需要3个控制点进行后方交汇")
        
        if method == "least_squares":
            return self._least_squares_resection(control_points)
        elif method == "affine":
            return self._affine_resection(control_points)
        else:
            raise ValueError(f"未知的计算方法: {method}")
    
    def _least_squares_resection(self, control_points: List[Tuple[GPSPoint, CoordinatePoint]]) -> dict:
        """
        最小二乘法后方交汇
        
        参数:
            control_points: 控制点列表
            
        返回:
            转换参数字典
        """
        n = len(control_points)
        
        # 构建设计矩阵A和观测向量b
        A = []
        b_x = []
        b_y = []
        
        for gps_point, coord_point in control_points:
            A.append([1, gps_point.latitude, gps_point.longitude])
            b_x.append(coord_point.x)
            b_y.append(coord_point.y)
        
        A = np.array(A)
        b_x = np.array(b_x)
        b_y = np.array(b_y)
        
        # 使用最小二乘法求解转换参数
        try:
            params_x = np.linalg.lstsq(A, b_x, rcond=None)[0]
            params_y = np.linalg.lstsq(A, b_y, rcond=None)[0]
        except np.linalg.LinAlgError:
            raise ValueError("矩阵计算失败，请检查控制点数据")
        
        # 计算高程转换参数（简化处理）
        elevations = [gps.elevation for gps, _ in control_points]
        z_coords = [coord.z for _, coord in control_points]
        
        if len(set(elevations)) > 1:
            # 如果有多个高程值，使用线性回归
            A_z = np.array([[1, elev] for elev in elevations])
            b_z = np.array(z_coords)
            params_z = np.linalg.lstsq(A_z, b_z, rcond=None)[0]
        else:
            # 如果只有一个高程值，使用简单偏移
            params_z = np.array([z_coords[0] - elevations[0], 0])
        
        return {
            "method": "least_squares",
            "x_params": params_x.tolist(),
            "y_params": params_y.tolist(),
            "z_params": params_z.tolist(),
            "control_points_count": n
        }
    
    def _affine_resection(self, control_points: List[Tuple[GPSPoint, CoordinatePoint]]) -> dict:
        """
        仿射变换后方交汇
        
        参数:
            control_points: 控制点列表
            
        返回:
            转换参数字典
        """
        if len(control_points) < 3:
            raise ValueError("仿射变换至少需要3个控制点")
        
        # 使用前3个控制点进行仿射变换
        gps_points = [gps for gps, _ in control_points[:3]]
        coord_points = [coord for _, coord in control_points[:3]]
        
        # 构建仿射变换矩阵
        # x = a0 + a1*lat + a2*lon
        # y = b0 + b1*lat + b2*lon
        
        A = np.array([
            [1, gps_points[0].latitude, gps_points[0].longitude],
            [1, gps_points[1].latitude, gps_points[1].longitude],
            [1, gps_points[2].latitude, gps_points[2].longitude]
        ])
        
        b_x = np.array([coord_points[0].x, coord_points[1].x, coord_points[2].x])
        b_y = np.array([coord_points[0].y, coord_points[1].y, coord_points[2].y])
        
        try:
            params_x = np.linalg.solve(A, b_x)
            params_y = np.linalg.solve(A, b_y)
        except np.linalg.LinAlgError:
            raise ValueError("矩阵计算失败，请检查控制点数据")
        
        # 计算高程转换参数
        elevations = [gps.elevation for gps in gps_points]
        z_coords = [coord.z for coord in coord_points]
        params_z = np.array([z_coords[0] - elevations[0], 0])
        
        return {
            "method": "affine",
            "x_params": params_x.tolist(),
            "y_params": params_y.tolist(),
            "z_params": params_z.tolist(),
            "control_points_count": 3
        }
    
    def gps_to_local(self, gps_point: GPSPoint, transform_params: dict) -> CoordinatePoint:
        """
        GPS坐标转换为局部坐标
        
        参数:
            gps_point: GPS坐标点
            transform_params: 转换参数
            
        返回:
            局部坐标点
        """
        x_params = transform_params.get("x_params", [0, 0, 0])
        y_params = transform_params.get("y_params", [0, 0, 0])
        z_params = transform_params.get("z_params", [0, 0])
        
        # 计算X坐标
        x = x_params[0] + x_params[1] * gps_point.latitude + x_params[2] * gps_point.longitude
        
        # 计算Y坐标
        y = y_params[0] + y_params[1] * gps_point.latitude + y_params[2] * gps_point.longitude
        
        # 计算Z坐标
        z = z_params[0] + z_params[1] * gps_point.elevation
        
        # 应用精度
        x = round(x, self.precision)
        y = round(y, self.precision)
        z = round(z, self.precision)
        
        return CoordinatePoint(x=x, y=y, z=z)
    
    def local_to_gps(self, coord_point: CoordinatePoint, transform_params: dict) -> GPSPoint:
        """
        局部坐标转换为GPS坐标
        
        参数:
            coord_point: 局部坐标点
            transform_params: 转换参数
            
        返回:
            GPS坐标点
        """
        x_params = transform_params.get("x_params", [0, 1, 0])
        y_params = transform_params.get("y_params", [0, 0, 1])
        z_params = transform_params.get("z_params", [0, 1])
        
        # 反向计算（简化处理，实际应用中可能需要更复杂的逆变换）
        # 这里使用数值方法求解
        
        def equations(vars):
            lat, lon = vars
            x = x_params[0] + x_params[1] * lat + x_params[2] * lon - coord_point.x
            y = y_params[0] + y_params[1] * lat + y_params[2] * lon - coord_point.y
            return [x, y]
        
        # 使用牛顿法求解
        lat, lon = 30.0, 114.0  # 初始猜测
        for _ in range(100):
            f = equations([lat, lon])
            
            # 计算雅可比矩阵
            J = np.array([
                [x_params[1], x_params[2]],
                [y_params[1], y_params[2]]
            ])
            
            try:
                delta = np.linalg.solve(J, -np.array(f))
            except np.linalg.LinAlgError:
                break
            
            lat += delta[0]
            lon += delta[1]
            
            if np.linalg.norm(delta) < 1e-10:
                break
        
        # 计算高程
        elevation = (coord_point.z - z_params[0]) / z_params[1] if z_params[1] != 0 else 0
        
        # 应用精度
        latitude = round(lat, self.precision)
        longitude = round(lon, self.precision)
        elevation = round(elevation, self.precision)
        
        return GPSPoint(latitude=latitude, longitude=longitude, elevation=elevation)
    
    def calculate_deviation(self, 
                           measured_point: CoordinatePoint,
                           design_point: CoordinatePoint,
                           threshold: float = 0.05) -> dict:
        """
        计算偏差
        
        参数:
            measured_point: 实测坐标点
            design_point: 设计坐标点
            threshold: 偏差阈值
            
        返回:
            偏差信息字典
        """
        # 计算各方向偏差
        deviation_x = measured_point.x - design_point.x
        deviation_y = measured_point.y - design_point.y
        deviation_z = measured_point.z - design_point.z
        
        # 计算总偏差（欧氏距离）
        total_deviation = math.sqrt(
            deviation_x ** 2 + 
            deviation_y ** 2 + 
            deviation_z ** 2
        )
        
        # 判断是否超阈值
        is_exceeded = total_deviation > threshold
        
        # 应用精度
        deviation_x = round(deviation_x, self.precision)
        deviation_y = round(deviation_y, self.precision)
        deviation_z = round(deviation_z, self.precision)
        total_deviation = round(total_deviation, self.precision)
        
        return {
            "deviation_x": deviation_x,
            "deviation_y": deviation_y,
            "deviation_z": deviation_z,
            "total_deviation": total_deviation,
            "threshold": threshold,
            "is_exceeded": is_exceeded,
            "status": "exceeded" if is_exceeded else "normal"
        }


# 创建全局坐标转换服务实例
coordinate_transform = CoordinateTransformService()
