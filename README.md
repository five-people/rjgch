# 现场之眼 (Xczy) - AR工程测量与施工辅助工具

## 项目概述

**现场之眼**是一款基于 Android 的增强现实（AR）工程测量与施工辅助工具软件。通过集成 GPS 定位、坐标转换、AR 实景叠加等先进技术，为工程测量与施工人员提供高效的现场辅助工作平台。

### 核心功能特性

1. **GPS 定位与坐标关联** 📍
   - 直接获取设备实时 GPS 坐标
   - 自动标记和关联工程项目坐标系
   - 显示精度等级和定位状态

2. **智能坐标换算** 🔄
   - 基于后方交汇算法的自动坐标转换
   - GPS 坐标 ↔ 项目坐标无缝转换
   - 减少人工计算成本

3. **AR 实景叠加可视化** 🎯
   - 将工程图纸与 3D 模型叠加到实时相机画面
   - 网格辅助线显示
   - 实时模型透明度调整

4. **离线作业支持** 📴
   - 完整的离线工作模式
   - 离线数据管理和同步
   - 项目离线包下载与版本管理

5. **施工偏差检测与预警** ⚠️
   - 实时偏差监测
   - 超标自动警告提醒
   - 历史数据对比分析

6. **完整的记录管理** 📋
   - 所有测量记录存档
   - 异常记录标记和追踪
   - 数据分析和报表导出

## 项目结构

```
d:/android/xiangmu/xczy/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── AndroidManifest.xml
│   │       ├── java/com/example/xczy/
│   │       │   ├── MainActivity.kt          # 主入口
│   │       │   ├── ui/
│   │       │   │   ├── screen/
│   │       │   │   │   ├── MeasurementScreen.kt       # 测量页面
│   │       │   │   │   ├── ARViewScreen.kt            # AR视图页面
│   │       │   │   │   ├── OfflineManagementScreen.kt # 离线管理页面
│   │       │   │   │   ├── RecordsScreen.kt           # 记录页面
│   │       │   │   │   └── ProfileScreen.kt           # 我的页面
│   │       │   │   ├── navigation/
│   │       │   │   │   └── NavigationConfig.kt        # 导航配置
│   │       │   │   └── theme/
│   │       │   │       └── Theme.kt                  # UI主题
│   │       │   └── model/                 # 数据模型（待开发）
│   │       └── res/                       # 资源文件
│   ├── build.gradle.kts
│   └── proguard-rules.pro
├── gradle/
├── build.gradle.kts
├── settings.gradle.kts
└── README.md
```

## 主要页面说明

### 1. 测量页面 (Measurement Screen)
- **功能模块**：
  - GPS 定位信息实时显示（纬度、经度、优度、海拔）
  - 自动坐标换算结果（项目X/Y坐标）
  - 开始/停止定位按钮
  - 刷新数据按钮

- **设计风格**：工程简洁风格，高对比度，卡片式布局

### 2. AR视图页面 (AR View Screen)
- **功能模块**：
  - 实时相机预览区域（模拟AR相机视图）
  - 3D模型叠加显示
  - 网格辅助线
  - 坐标实时显示
  - 控制面板：模型透明度调整、网格开关、偏差检测开关

### 3. 离线管理页面 (Offline Management Screen)
- **功能模块**：
  - 存储使用统计
  - 同步状态显示
  - 项目数据卡片列表
  - 立即同步按钮
  - 添加项目 / 清理缓存操作

### 4. 记录页面 (Records Screen)
- **功能模块**：
  - 记录统计信息（总数、异常数、今日数）
  - 筛选功能（全部、异常、今日）
  - 历史记录列表显示
  - 坐标信息和偏差值展示
  - 导出数据 / 分析报告按钮

### 5. 我的页面 (Profile Screen)
- **功能模块**：
  - 用户信息卡片（头像、昵称、工号、在线状态）
  - 工作统计（项目数、测量次数、工时）
  - 功能设置（工作模式、通知、自动校准）
  - 系统信息（版本、缓存大小、设置）
  - 关于我们 / 反馈建议 / 退出登录

## 技术栈

### 前端框架
- **Jetpack Compose**：现代声明式UI框架
- **Kotlin**：官方推荐的 Android 开发语言
- **Material Design 3**：谷歌最新设计规范

### 核心库
```gradle
dependencies {
    // Compose UI相关
    implementation "androidx.compose.ui:ui"
    implementation "androidx.compose.material3:material3"
    implementation "androidx.compose.runtime:runtime"
    
    // Compose Navigation（未来扩展）
    implementation "androidx.navigation:navigation-compose"
    
    // Activity
    implementation "androidx.activity:activity-compose"
    
    // 其他
    implementation "androidx.lifecycle:lifecycle-runtime-ktx"
}
```

## 设计规范

### 颜色体系
- **主色**：`#2196F3` (蓝色) - 品牌色
- **成功**：`#4CAF50` (绿色) - 正常/成功状态
- **警告**：`#FF9800` (橙色) - 注意状态
- **错误**：`#FF6B6B` (红色) - 异常/错误状态
- **背景**：`#FFFFFF` (白色) - 主背景
- **辅助**：`#F5F5F5` - 卡片背景
- **文字**：`#000000` / `#808080` / `#CCCCCC` - 不同层级

### 字体规范
- **标题**：14-20sp, Bold (600-700)
- **正文**：12-14sp, Regular (400)
- **辅助**：11-12sp, Regular (400)

### 间距规范
- **基础单位**：4dp
- **小间距**：8dp
- **中间距**：12-16dp
- **大间距**：24-32dp

## 快速开始

### 环境要求
- Android Studio 2022.1 或更高版本
- Gradle 7.0+
- Kotlin 1.8+
- minSdkVersion: 23+
- targetSdkVersion: 34+

### 编译构建
```bash
# 克隆项目
cd d:/android/xiangmu/xczy

# 构建 Debug 版本
./gradlew assembleDebug

# 构建 Release 版本
./gradlew assembleRelease

# 运行应用
./gradlew installDebug
```

### 在 IDE 中运行
1. 在 Android Studio 中打开项目
2. 选择 "Build" → "Build Bundle(s) / APK(s)" → "Build APK(s)"
3. 或按 `Shift + F10` 在模拟器中运行

## 后续开发计划

### Phase 1 - 基础功能（已完成）
- ✅ UI 界面设计与实现
- ✅ 页面导航框架
- ✅ 基本数据展示

### Phase 2 - 核心功能（开发中）
- ⏳ GPS 定位集成（通过 Location API）
- ⏳ 坐标转换算法实现
- ⏳ 本地数据存储（Room Database）
- ⏳ 网络同步功能

### Phase 3 - AR 功能
- ⏳ ARCore 集成
- ⏳ 3D 模型渲染
- ⏳ 实时叠加显示

### Phase 4 - 高级功能
- ⏳ 离线工作模式完善
- ⏳ 数据分析与报表
- ⏳ 用户认证与权限管理
- ⏳ 云端同步

## 文件说明

### MainActivity.kt
应用入口和主界面容器，使用 `NavigationSuiteScaffold` 实现底部导航。

### Screen 页面文件
各个功能页面的 Composable 函数，完全独立且可复用。

### NavigationConfig.kt
导航配置和路由定义，便于未来扩展到声明式导航。

## 常见问题

**Q: 如何添加新的导航页面？**

A: 
1. 在 `ui/screen/` 中创建新的 Screen 文件
2. 在 `AppDestinations` enum 中添加新的目标
3. 在 `XczyApp()` 的 when 语句中添加对应逻辑

**Q: 如何自定义主题颜色？**

A: 在 `ui/theme/` 中修改主题定义，使用 Material Design 3 的 ColorScheme。

**Q: 图标资源从哪里获取？**

A: 项目使用 Material Icons，可通过 `androidx.compose.material.icons` 直接使用。

## 许可证

本项目为内部工程项目，未明确支持开源发布。

## 联系方式

如有问题或建议，请联系开发团队。

---

**项目启动日期**：2026年4月
**最后更新**：2026年4月20日
