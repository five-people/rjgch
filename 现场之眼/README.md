# 现场之眼 - 后端服务

基于FastAPI的AR施工测量辅助软件后端系统。

## 功能特性

- 用户认证与授权
- 项目管理
- 坐标转换（后方交汇算法）
- 测量记录管理
- 图纸管理
- 3D模型管理
- 离线数据管理

## 技术栈

- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PostgreSQL
- Redis
- JWT认证

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

### 3. 初始化数据库

```bash
python -c "from app.database import init_db; init_db()"
```

### 4. 启动服务

```bash
python main.py
```

服务将在 http://localhost:8000 启动。

## API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

