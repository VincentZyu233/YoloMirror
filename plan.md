# YoloMirror 项目规划

## 项目概述
基于 Fabric Mod + Python 后端 + MediaPipe + YOLO 的实时摄像头交互系统

## 技术栈

### 前端 (Fabric Mod)
- **语言**: Java
- **框架**: Fabric API
- **功能**: 
  - 接收 Python 后端指令
  - 实时渲染控制 (roll 角度等)
  - 双向通信支持

### 后端 (Python)
- **语言**: Python 3.10+
- **GUI**: PyQt5/PyQt6
- **AI 框架**: MediaPipe (初始), YOLO (后续)
- **通信**: WebSocket (初始), UDP (预留)

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                     Minecraft (Fabric Mod)                   │
│  ┌──────────────────┐  ┌────────────────────────────────┐  │
│  │  YoloMirrorClient│  │   GameRendererMixin            │  │
│  │  - 命令注册       │  │   - 世界渲染注入               │  │
│  │  - roll 控制      │  │   - 实时角度应用               │  │
│  └────────┬─────────┘  └────────────────────────────────┘  │
│           │                                                  │
│           │  WebSocket/UDP                                   │
└───────────┼──────────────────────────────────────────────────┘
            │
            │  双向通信
            │
┌───────────┼──────────────────────────────────────────────────┐
│           │              Python Backend                      │
│  ┌────────▼─────────┐  ┌────────────────────────────────┐  │
│  │  Communication   │  │   AI Processing Engine         │  │
│  │  - WebSocket     │  │   - MediaPipe (初始)            │  │
│  │  - UDP (预留)    │  │   - YOLO (后续)                 │  │
│  │  - 消息队列       │  │   - 姿态识别                    │  │
│  └────────┬─────────┘  │   - 手势识别                    │  │
│           │            │   - 面部追踪                    │  │
│  ┌────────▼─────────┘  └────────────────────────────────┘  │
│  │     GUI (PyQt)   │                                       │
│  │  - 实时摄像头    │                                       │
│  │  - 数据可视化    │                                       │
│  │  - 控制面板      │                                       │
│  └──────────────────┘                                       │
└──────────────────────────────────────────────────────────────┘
```

## 模块设计

### 1. 通信层 (Communication Layer)

#### WebSocket 服务端
```python
# 目录结构
backend/
├── communication/
│   ├── __init__.py
│   ├── websocket_server.py      # WebSocket 服务
│   ├── udp_server.py            # UDP 服务 (预留)
│   └── protocol.py              # 通信协议定义
```

#### 消息协议
```json
// 客户端 -> 服务端
{
  "type": "status_update",
  "timestamp": 1234567890,
  "data": {...}
}

// 服务端 -> 客户端
{
  "type": "roll_control",
  "angle": 45.0,
  "duration": 1000
}
```

### 2. AI 处理引擎 (AI Processing Engine)

```python
backend/
├── ai/
│   ├── __init__.py
│   ├── base_engine.py           # AI 引擎基类
│   ├── mediapipe_engine.py      # MediaPipe 实现
│   ├── yolov8_engine.py         # YOLO 实现 (后续)
│   └── processors/
│       ├── __init__.py
│       ├── pose_processor.py    # 姿态处理器
│       ├── hand_processor.py    # 手势处理器
│       └── face_processor.py    # 面部处理器
```

#### 功能规划
- **MediaPipe 初始功能**:
  - 实时姿态追踪 (Pose Detection)
  - 手势识别 (Hand Tracking)
  - 面部关键点检测
  
- **YOLO 扩展功能**:
  - 物体检测与追踪
  - 自定义模型支持
  - 多目标追踪

### 3. GUI 界面 (PyQt)

```python
backend/
├── gui/
│   ├── __init__.py
│   ├── main_window.py           # 主窗口
│   ├── camera_widget.py         # 摄像头显示
│   ├── visualization_widget.py  # 数据可视化
│   └── control_panel.py         # 控制面板
```

#### 界面功能
- 左侧: 实时摄像头画面
- 右侧-top: AI 数据可视化 (关键点、骨架)
- 右侧-bottom: 控制面板
  - Roll 角度滑块
  - 模式选择 (姿态/手势/面部)
  - 阈值调节
  - 连接状态显示

### 4. Fabric Mod 扩展

```java
src/
├── main/
│   ├── java/me/vincentzyu/qwq/yolomirror/
│   │   ├── client/
│   │   │   ├── YoloMirrorClient.java
│   │   │   ├── network/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── websocket_client.py  # Python 封装
│   │   │   │   └── protocol.py
│   │   │   └── ai/
│   │   │       ├── __init__.py
│   │   │       ├── AIDataReceiver.java
│   │   │       └── AIMotionApplier.java
│   │   └── common/
│   │       └── config/
│   │           ├── __init__.py
│   │           └── ConfigManager.java
```

## 开发阶段

### Phase 1: 基础框架搭建 ✅
- [x] Fabric Mod Roll 控制 Demo (已完成)
- [ ] Python 后端基础框架
- [ ] WebSocket 通信实现
- [ ] PyQt 基础界面 (摄像头显示)

### Phase 2: MediaPipe 集成
- [ ] MediaPipe 姿态追踪
- [ ] 姿态数据处理与映射
- [ ] 实时数据可视化
- [ ] Roll 角度自动控制

### Phase 3: 扩展功能
- [ ] 手势识别集成
- [ ] 面部追踪集成
- [ ] UDP 通信支持
- [ ] 多玩家支持

### Phase 4: YOLO 集成
- [ ] YOLOv8 集成
- [ ] 物体检测与追踪
- [ ] 自定义模型支持
- [ ] 性能优化

### Phase 5: 高级功能
- [ ] 模式切换 (自动/手动)
- [ ] 配置文件系统
- [ ] 数据记录与回放
- [ ] 多摄像头支持

## 通信协议设计

### 消息类型
```python
# 客户端 -> 服务端
STATUS_UPDATE = "status_update"
REQUEST_CONTROL = "request_control"
ERROR = "error"

# 服务端 -> 客户端
ROLL_CONTROL = "roll_control"
POSE_DATA = "pose_data"
HAND_DATA = "hand_data"
FACE_DATA = "face_data"
CONFIG_UPDATE = "config_update"
```

### 数据格式
```python
# 姿态数据示例
{
  "type": "pose_data",
  "timestamp": 1234567890,
  "pose_landmarks": [
    {"x": 0.5, "y": 0.3, "z": 0.1, "visibility": 0.9},
    ...
  ],
  "pose_classification": "standing",
  "confidence": 0.95
}

# Roll 控制指令
{
  "type": "roll_control",
  "angle": 45.0,
  "duration": 1000,
  "easing": "smoothstep"
}
```

## 预留扩展点

### 1. 通信协议
- [x] WebSocket 实现
- [ ] UDP 通信 (预留接口)
- [ ] gRPC (预留接口)
- [ ] MQTT (预留接口)

### 2. AI 引擎
- [x] MediaPipe 集成
- [ ] YOLO 集成
- [ ] TensorFlow Lite (预留)
- [ ] ONNX Runtime (预留)

### 3. 数据源
- [x] 摄像头输入
- [ ] 视频文件输入
- [ ] 多摄像头同步
- [ ] 外部视频流输入

## 开发规范

### 代码组织
- 模块化设计，高内聚低耦合
- 清晰的接口定义
- 完整的类型注解
- 详细的文档注释

### 命名规范
- Python: PEP 8
- Java: Google Java Style
- 配置文件: snake_case
- 常量: UPPER_SNAKE_CASE

### 版本管理
- 主分支: main
- 开发分支: dev
- 功能分支: feature/xxx
- 修复分支: fix/xxx

## 参考资源

- MediaPipe: https://github.com/google-ai-edge/mediapipe
- Fabric API: https://fabricmc.net/
- YOLOv8: https://github.com/ultralytics/ultralytics
- PyQt: https://www.riverbankcomputing.com/software/pyqt/

## 下一步行动

1. 创建 Python 后端项目结构
2. 实现 WebSocket 通信基础框架
3. 集成 MediaPipe 姿态追踪
4. 实现 PyQt 基础界面
5. 连接 Fabric Mod 进行端到端测试
