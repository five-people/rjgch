-- 创建数据库
CREATE DATABASE IF NOT EXISTS `field_eye_db` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_general_ci;

USE `field_eye_db`;

-- 用户表
CREATE TABLE `User` (
  `user_id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
  `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
  `password` VARBINARY(255) NOT NULL COMMENT 'AES-256加密密码',
  `role` ENUM('worker', 'manager') NOT NULL COMMENT '角色：施工员(worker)/管理员(manager)',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_login` TIMESTAMP NULL COMMENT '最后登录时间',
  `sync_status` ENUM('pending', 'synced', 'failed') DEFAULT 'pending' COMMENT '同步状态'
) ENGINE=InnoDB;

-- 项目表
CREATE TABLE `Project` (
  `project_id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '项目ID',
  `project_name` VARCHAR(100) NOT NULL COMMENT '项目名称',
  `base_point_coord` VARCHAR(255) NOT NULL COMMENT '基准点坐标（设计坐标系）',
  `coordinate_system` ENUM('WGS-84', 'CGCS2000', 'Local') NOT NULL COMMENT '坐标系类型',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `sync_status` ENUM('pending', 'synced', 'failed') DEFAULT 'pending' COMMENT '同步状态'
) ENGINE=InnoDB;

-- 用户-项目关联表
CREATE TABLE `UserProject` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL COMMENT '用户ID',
  `project_id` INT NOT NULL COMMENT '项目ID',
  `access_level` ENUM('read', 'write') DEFAULT 'read' COMMENT '访问权限',
  FOREIGN KEY (`user_id`) REFERENCES `User`(`user_id`) ON DELETE CASCADE,
  FOREIGN KEY (`project_id`) REFERENCES `Project`(`project_id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 测点表
CREATE TABLE `MeasurementPoint` (
  `point_id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '测点ID',
  `project_id` INT NOT NULL COMMENT '项目ID',
  `gps_longitude` DECIMAL(9,6) NOT NULL COMMENT 'GPS经度',
  `gps_latitude` DECIMAL(8,6) NOT NULL COMMENT 'GPS纬度',
  `altitude` DECIMAL(6,2) COMMENT '海拔',
  `measured_coord` VARCHAR(255) NOT NULL COMMENT '实测坐标（转换后）',
  `positioning_accuracy` DECIMAL(5,2) COMMENT '定位精度',
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '时间戳',
  `sync_status` ENUM('pending', 'synced', 'failed') DEFAULT 'pending' COMMENT '同步状态',
  FOREIGN KEY (`project_id`) REFERENCES `Project`(`project_id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 偏差记录表
CREATE TABLE `DeviationRecord` (
  `record_id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
  `point_id` INT NOT NULL COMMENT '测点ID',
  `design_coord` VARCHAR(255) NOT NULL COMMENT '设计坐标',
  `measured_coord` VARCHAR(255) NOT NULL COMMENT '实测坐标',
  `deviation_x` DECIMAL(6,2) NOT NULL COMMENT 'X方向偏差值(mm)',
  `deviation_y` DECIMAL(6,2) NOT NULL COMMENT 'Y方向偏差值(mm)',
  `deviation_z` DECIMAL(6,2) NOT NULL COMMENT 'Z方向偏差值(mm)',
  `is_exceeded` BOOLEAN DEFAULT 0 COMMENT '是否超阈值',
  `warning_type` ENUM('vibration', 'voice', 'both') COMMENT '预警类型',
  `reviewed_by` INT NULL COMMENT '审核人ID',
  `sync_status` ENUM('pending', 'synced', 'failed') DEFAULT 'pending' COMMENT '同步状态',
  FOREIGN KEY (`point_id`) REFERENCES `MeasurementPoint`(`point_id`) ON DELETE CASCADE,
  FOREIGN KEY (`reviewed_by`) REFERENCES `User`(`user_id`)
) ENGINE=InnoDB;

-- 缓存文件表
CREATE TABLE `CacheMetadata` (
  `cache_id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '缓存ID',
  `project_id` INT NOT NULL COMMENT '项目ID',
  `file_type` ENUM('blueprint', '3d_model', 'base_data') NOT NULL COMMENT '文件类型',
  `local_path` VARCHAR(255) NOT NULL COMMENT '本地路径',
  `file_size` BIGINT UNSIGNED COMMENT '文件大小(字节)',
  `last_access` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后访问时间',
  `sync_status` ENUM('pending', 'synced', 'failed') DEFAULT 'pending' COMMENT '同步状态',
  FOREIGN KEY (`project_id`) REFERENCES `Project`(`project_id`) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 索引优化
CREATE INDEX `idx_timestamp` ON `MeasurementPoint` (`timestamp`);
CREATE INDEX `idx_exceeded` ON `DeviationRecord` (`is_exceeded`);