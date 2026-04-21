# 现场之眼 - 技术架构与开发路线图

## 项目架构图

```
┌─────────────────────────────────────────────────────────┐
│                    现场之眼 App                          │
│                  (Xczy Application)                      │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    ┌───▼────┐        ┌───▼────┐       ┌───▼────┐
    │    UI   │        │ Domain │       │  Data  │
    │ Layer   │        │ Layer  │       │ Layer  │
    └────────┘        └────────┘       └────────┘
        │                 │                 │
        │                 │                 │
    ┌───▼────────────────┴──────────────────▼───┐
    │      Android Framework & Libraries        │
    │  (Compose, Lifecycle, Room, etc.)         │
    └─────────────────────────────────────────┘
        │
    ┌───▼─────────────────────────────────┐
    │     Native Android APIs             │
    │ (Location, Camera, Storage, etc.)   │
    └─────────────────────────────────────┘
```

## 软件架构

### 分层架构 (Layered Architecture)

```
┌────────────────────────────────────────────────────────┐
│  Presentation Layer (UI/UX)                            │
│  ├─ MainActivity                                       │
│  ├─ Screen Components (Composable)                     │
│  │  ├─ MeasurementScreen                              │
│  │  ├─ ARViewScreen                                   │
│  │  ├─ OfflineManagementScreen                        │
│  │  ├─ RecordsScreen                                  │
│  │  └─ ProfileScreen                                  │
│  └─ UI Components & Navigation                        │
└────────────────────────────────────────────────────────┘
                          │
                ┌─────────▼──────────┐
                │  ViewModel Layer   │
                │  (Logic & State)   │
                └─────────┬──────────┘
                          │
┌────────────────────────────────────────────────────────┐
│  Domain Layer (Business Logic)                         │
│  ├─ Repositories (Data Access)                        │
│  ├─ Use Cases (Business Rules)                        │
│  │  ├─ LocationUseCase                               │
│  │  ├─ CoordinateConversionUseCase                   │
│  │  ├─ OfflineDataUseCase                            │
│  │  └─ ...                                            │
│  └─ Models & Entities                                 │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│  Data Layer (Data Management)                          │
│  ├─ Local Database (Room)                             │
│  │  ├─ MeasurementRecords                            │
│  │  ├─ ProjectData                                    │
│  │  └─ UserPreferences                                │
│  ├─ Local Storage (SharedPreferences)                 │
│  ├─ Remote API (Future)                               │
│  └─ Location Service                                  │
└────────────────────────────────────────────────────────┘
```

## 当前项目结构

```
com/example/xczy/
├── MainActivity.kt                    # App入口
│
├── ui/
│   ├── screen/                       # 页面层
│   │   ├── MeasurementScreen.kt       # 测量页面 ✅
│   │   ├── ARViewScreen.kt            # AR视图页面 ✅
│   │   ├── OfflineManagementScreen.kt # 离线管理页面 ✅
│   │   ├── RecordsScreen.kt           # 记录页面 ✅
│   │   └── ProfileScreen.kt           # 我的页面 ✅
│   │
│   ├── component/                    # 可复用组件（待开发）
│   │   ├── CoordinateDisplay.kt
│   │   ├── StatusCard.kt
│   │   └── ...
│   │
│   ├── navigation/                   # 导航配置
│   │   └── NavigationConfig.kt        # 导航配置 ✅
│   │
│   └── theme/                        # 主题定义
│       └── Theme.kt
│
├── data/                             # 数据层（待开发）
│   ├── database/
│   │   ├── AppDatabase.kt
│   │   ├── dao/
│   │   │   ├── MeasurementDao.kt
│   │   │   ├── ProjectDao.kt
│   │   │   └── RecordDao.kt
│   │   └── entity/
│   │       ├── MeasurementEntity.kt
│   │       ├── ProjectEntity.kt
│   │       └── RecordEntity.kt
│   ├── preference/
│   │   └── UserPreferences.kt
│   └── repository/
│       ├── LocationRepository.kt
│       ├── OfflineDataRepository.kt
│       ├── MeasurementRepository.kt
│       └── ProjectRepository.kt
│
├── domain/                           # 业务层（待开发）
│   ├── model/
│   │   ├── Location.kt
│   │   ├── ProjectCoordinate.kt
│   │   └── MeasurementRecord.kt
│   ├── usecase/
│   │   ├── LocationUseCase.kt
│   │   ├── CoordinateConversionUseCase.kt
│   │   ├── OfflineDataUseCase.kt
│   │   └── MeasurementUseCase.kt
│   └── repository/
│       └── (interfaces)
│
├── viewmodel/                        # 状态管理（待开发）
│   ├── MeasurementViewModel.kt
│   ├── ARViewModel.kt
│   ├── OfflineViewModel.kt
│   ├── RecordsViewModel.kt
│   └── ProfileViewModel.kt
│
├── util/                             # 工具类
│   ├── CoordinateConverter.kt         # 坐标转换算法
│   ├── Constants.kt                   # 常量定义
│   ├── Extensions.kt                  # Kotlin扩展函数
│   └── Logger.kt                      # 日志工具
│
└── service/                          # 后台服务（待开发）
    ├── LocationService.kt
    ├── SyncService.kt
    └── NotificationService.kt
```

**状态说明**：
- ✅ 已完成
- ⏳ 开发中
- 📋 待开发

## 技术栈

### 核心框架
| 组件 | 版本 | 说明 |
|------|------|------|
| Kotlin | 1.9+ | 官方开发语言 |
| Compose | 1.5+ | 现代声明式UI框架 |
| Android API | 24-36 | 支持的API级别 |

### 主要库

#### UI & Navigation
```gradle
// Compose
androidx.compose.ui:ui:1.5.0
androidx.compose.material3:material3:1.1.0
androidx.compose.material3:material3-adaptive-navigation-suite:1.1.0

// Navigation
androidx.navigation:navigation-compose:2.7.0
```

#### Data & Storage
```gradle
// Database
androidx.room:room-runtime:2.5.2
androidx.room:room-ktx:2.5.2

// DataStore (for preferences)
androidx.datastore:datastore-preferences:1.0.0

// Serialization
kotlinx.serialization:kotlinx-serialization-json:1.5.1
```

#### Lifecycle & Coroutines
```gradle
// Lifecycle
androidx.lifecycle:lifecycle-runtime-ktx:2.6.1
androidx.lifecycle:lifecycle-viewmodel-compose:2.6.1

// Coroutines
org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.1
org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.1
```

#### Location & Sensors
```gradle
// Location Services (待集成)
com.google.android.gms:play-services-location:21.0.1

// ARCore (待集成)
com.google.ar:core:1.40.0

// Sensors & Accelerometer
// (Built-in Android API)
```

#### Dependency Injection (待选择)
```gradle
// Hilt (Recommended)
com.google.dagger:hilt-android:2.46
com.google.dagger:hilt-compiler:2.46

// Or Koin (Lighter)
io.insert-koin:koin-android:3.4.0
```

#### Testing
```gradle
// Unit Testing
junit:junit:4.13.2
io.mockk:mockk:1.13.5

// UI Testing
androidx.compose.ui:ui-test-junit4:1.5.0
androidx.test.espresso:espresso-core:3.5.1
```

## 开发进度 (Roadmap)

### ✅ Phase 1 - UI框架 (完成)
**时间**: 2026-04-20

**目标**: 搭建完整的UI界面框架

**完成内容**:
- [x] 项目结构初始化
- [x] 5个主页面UI实现
- [x] 导航框架搭建
- [x] UI设计规范定义
- [x] 文档与指南编写

**关键文件**:
- MainActivity.kt (主入口)
- MeasurementScreen.kt
- ARViewScreen.kt
- OfflineManagementScreen.kt
- RecordsScreen.kt
- ProfileScreen.kt

---

### ⏳ Phase 2 - 数据层 (2-3周)
**目标**: 实现数据存储和管理

**计划任务**:
- [ ] Room数据库设计与实现
- [ ] Entity数据模型定义
- [ ] DAO接口实现
- [ ] Repository数据访问层
- [ ] SharedPreferences用户偏好设置
- [ ] 数据库初始化和迁移

**关键类**:
```
data/
├── database/
│   ├── AppDatabase.kt
│   ├── entity/
│   │   ├── MeasurementEntity.kt
│   │   ├── ProjectEntity.kt
│   │   └── RecordEntity.kt
│   └── dao/
│       ├── MeasurementDao.kt
│       ├── ProjectDao.kt
│       └── RecordDao.kt
└── repository/
    ├── LocationRepository.kt
    ├── MeasurementRepository.kt
    └── ProjectRepository.kt
```

---

### ⏳ Phase 3 - 业务逻辑层 (2-3周)
**目标**: 实现核心业务逻辑

**计划任务**:
- [ ] ViewModel状态管理
- [ ] LocationUseCase GPS定位逻辑
- [ ] CoordinateConversionUseCase坐标转换
- [ ] OfflineDataUseCase离线管理逻辑
- [ ] MeasurementUseCase测量记录管理
- [ ] 状态流(StateFlow)集成

**关键类**:
```
domain/
├── model/
│   ├── Location.kt
│   ├── ProjectCoordinate.kt
│   └── MeasurementRecord.kt
├── usecase/
│   ├── LocationUseCase.kt
│   ├── CoordinateConversionUseCase.kt
│   └── OfflineDataUseCase.kt
└── repository/
    └── (Repository interfaces)

viewmodel/
├── MeasurementViewModel.kt
├── ARViewModel.kt
├── OfflineViewModel.kt
├── RecordsViewModel.kt
└── ProfileViewModel.kt
```

---

### ⏳ Phase 4 - GPS与定位 (1-2周)
**目标**: 集成GPS定位功能

**计划任务**:
- [ ] Google Play Services Location集成
- [ ] 权限申请与处理
- [ ] 实时位置更新
- [ ] 位置精度监测
- [ ] 定位状态管理

**关键代码示例**:
```kotlin
// LocationService.kt
class LocationService {
    fun getLastLocation(): Location?
    fun requestLocationUpdates(callback: (Location) -> Unit)
    fun stopLocationUpdates()
}
```

---

### ⏳ Phase 5 - 坐标转换 (1-2周)
**目标**: 实现GPS ↔ 项目坐标转换

**计划任务**:
- [ ] 后方交汇算法实现
- [ ] 坐标系参数配置
- [ ] 转换结果缓存
- [ ] 精度评估
- [ ] 校准点管理

**算法参考**:
```
后方交汇法 (Resection):
1. 选择3个已知点（控制点）
2. 从测站点看向已知点
3. 通过计算得出测站点坐标

公式 (Simplified):
新坐标 = 旋转矩阵 × (GPS坐标 - 参考点) + 基准点
```

---

### ⏳ Phase 6 - AR实现 (3-4周)
**目标**: 实现AR实景叠加

**计划任务**:
- [ ] ARCore SDK集成
- [ ] 相机权限与预览
- [ ] 3D模型加载与显示
- [ ] 模型叠加与对齐
- [ ] 性能优化

**相关库**:
```gradle
// Google ARCore
com.google.ar:core:1.40.0
android.arch.navigation:navigation-runtime-ktx
```

---

### ⏳ Phase 7 - 离线同步 (2-3周)
**目标**: 完善离线工作与数据同步

**计划任务**:
- [ ] 离线数据包制作
- [ ] 增量同步实现
- [ ] 冲突解决策略
- [ ] 网络检测与自动同步
- [ ] 数据完整性校验

---

### ⏳ Phase 8 - 偏差检测 (1-2周)
**目标**: 实现施工偏差监测

**计划任务**:
- [ ] 偏差计算算法
- [ ] 实时警告提示
- [ ] 后台检测服务
- [ ] 通知推送集成
- [ ] 历史偏差分析

---

### ⏳ Phase 9 - 测试与优化 (2-3周)
**目标**: 质量保证与性能优化

**计划任务**:
- [ ] 单元测试编写 (>80% coverage)
- [ ] UI自动化测试
- [ ] 集成测试
- [ ] 性能优化与分析
- [ ] 内存泄漏检查
- [ ] 电量优化

---

### ⏳ Phase 10 - 发布准备 (1周)
**目标**: APP上线前的最后准备

**计划任务**:
- [ ] 代码审查与清理
- [ ] 文档完善
- [ ] 版本号设定
- [ ] 隐私政策补充
- [ ] Google Play应用商店配置
- [ ] Beta测试

---

## 关键技术难点

### 1. 坐标转换算法 🔄
**难度**: ⭐⭐⭐⭐
- **问题**: 从GPS坐标到项目坐标的准确转换
- **解决方案**:
  - 使用后方交汇法或相似变换
  - 通过多个控制点提高精度
  - 实现校准流程

### 2. AR实景叠加 📷
**难度**: ⭐⭐⭐⭐⭐
- **问题**: 3D模型与实景的精确对齐
- **解决方案**:
  - 充分利用ARCore的本地化
  - 实时IMU数据融合
  - 相机标定

### 3. 离线同步数据一致性 🔄
**难度**: ⭐⭐⭐⭐
- **问题**: 多设备修改数据造成冲突
- **解决方案**:
  - 时间戳版本控制
  - 终端获胜（Last-Write-Wins）或冲突检测
  - 同步日志记录

### 4. GPS定位精度 📍
**难度**: ⭐⭐⭐
- **问题**: 室外开阔地 vs 复杂环境
- **解决方案**:
  - 使用Kalman滤波优化定位
  - 多源融合 (GPS + GNSS + WiFi)
  - A-GPS辅助定位

### 5. 电池与性能 🔋
**难度**: ⭐⭐⭐
- **问题**: GPS定位和AR实时处理耗电大
- **解决方案**:
  - 位置更新频率优化
  - 后台任务优化
  - 电源管理策略

## 依赖关系图

```
MeasurementScreen
    ├─ LocationService
    │   └─ LocationRepository
    │       └─ Room Database
    ├─ CoordinateConverter
    │   └─ CoordinateConversionUseCase
    └─ MeasurementViewModel

ARViewScreen
    ├─ ARCore
    ├─ CameraPermission
    ├─ LocationService
    └─ DeviationDetectionUseCase

OfflineManagementScreen
    ├─ ProjectRepository
    └─ SyncService

RecordsScreen
    ├─ MeasurementRepository
    └─ RecordDao

ProfileScreen
    └─ UserPreferences
```

## 构建与部署

### 本地构建
```bash
# Debug版本
./gradlew assembleDebug

# Release版本
./gradlew assemble Release

# 运行测试
./gradlew test
./gradlew connectedAndroidTest

# 代码分析
./gradlew lint
./gradlew detekt
```

### CI/CD流程（未来）
```
Git Push
    ↓
GitHub Actions Triggered
    ↓
Build (./gradlew build)
    ↓
Test (Unit + UI Tests)
    ↓
Lint & Code Analysis
    ↓
Build APK/Bundle
    ↓
Sign Release Build
    ↓
Upload to Play Store (Beta)
    ↓
Monitor Crash Reports
```

---

**文档版本**：v1.0
**更新日期**：2026年4月20日
**维护者**：开发团队
