![YoloMirror](https://socialify.git.ci/VincentZyu233/YoloMirror/image?custom_description=%F0%9F%8E%AE+YoloMirror+-+%E9%80%9A%E8%BF%87+WebSocket+%E5%AE%9E%E7%8E%B0%E5%AE%9E%E6%97%B6+Minecraft+%E8%A7%86%E8%A7%92%E6%8E%A7%E5%88%B6%E7%9A%84Minecraft%E6%A8%A1%E7%BB%84%EF%BC%88%E7%8E%B0%E5%9C%A8%E5%8F%AA%E5%81%9A%E4%BA%86Fabric%EF%BC%89%EF%BC%8C%E6%94%AF%E6%8C%81%E5%B9%B3%E6%BB%91%E8%BF%87%E6%B8%A1%E5%92%8C%E8%87%AA%E5%AE%9A%E4%B9%89ws%E6%9C%8D%E5%8A%A1%E5%99%A8url&description=1&font=JetBrains+Mono&forks=1&issues=1&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fen%2Fthumb%2Fc%2Fcb%2FMinecraft_Logo-en.svg%2F960px-Minecraft_Logo-en.svg.png%3F_%3D20210929140435&name=1&owner=1&pattern=Signal&pulls=1&stargazers=1&theme=Auto)
# YoloMirror

一个基于 Fabric 的 Minecraft 模组，通过 WebSocket 实现实时视角控制。

## 功能特性

- 🎮 **实时视角控制**：通过 WebSocket 接收外部指令，平滑控制游戏中的 roll 角度
- 🔄 **平滑过渡**：视角变化采用平滑过渡算法，避免突兀的视角旋转
- 🌐 **自定义服务器**：支持自定义 WebSocket 服务器地址
- 📊 **状态查询**：实时查看连接状态和当前配置
- ⚡ **高性能**：基于 Mixin 技术，直接注入渲染流程，性能开销极小

## 技术栈

### 核心依赖

| 技术 | 版本 | 说明 |
|:---|:---|:---|
| [![Minecraft](https://img.shields.io/badge/Minecraft-1.21.8-62B47A?style=flat-square&logo=minecraft&logoColor=white)](https://minecraft.net/) | 1.21.8 | 游戏版本 |
| [![Fabric Loader](https://img.shields.io/badge/Fabric_Loader-0.17.2-96D0D1?style=flat-square&logo=fabric&logoColor=white)](https://fabricmc.net/) | 0.17.2 | 模组加载器 |
| [![Fabric API](https://img.shields.io/badge/Fabric_API-0.131.0-96D0D1?style=flat-square&logo=fabric&logoColor=white)](https://github.com/FabricMC/fabric) | 0.131.0+1.21.8 | Fabric API |
| [![Java](https://img.shields.io/badge/Java-21-007396?style=flat-square&logo=openjdk&logoColor=white)](https://openjdk.org/) | 21 | 编程语言 |
| [![Gradle](https://img.shields.io/badge/Gradle-9.2.1-02303A?style=flat-square&logo=gradle&logoColor=white)](https://gradle.org/) | 9.2.1 | 构建工具 |

### 开发依赖

| 技术 | 版本 | 说明 |
|:---|:---|:---|
| [![Fabric Loom](https://img.shields.io/badge/Fabric_Loom-1.15--SNAPSHOT-96D0D1?style=flat-square&logo=fabric&logoColor=white)](https://fabricmc.net/develop/) | 1.15-SNAPSHOT | Gradle 插件 |
| [![Yarn Mappings](https://img.shields.io/badge/Yarn-1.21.8+build.1-96D0D1?style=flat-square&logo=fabric&logoColor=white)](https://github.com/FabricMC/yarn) | 1.21.8+build.1 | 映射文件 |
| [![MixinExtras](https://img.shields.io/badge/MixinExtras-0.5.0-FF6B6B?style=flat-square)](https://github.com/LlamaLad7/MixinExtras) | 0.5.0 | Mixin 扩展 |
| [![Java-WebSocket](https://img.shields.io/badge/Java--WebSocket-1.5.4-3776AB?style=flat-square&logo=java&logoColor=white)](https://github.com/TooTallNate/Java-WebSocket) | 1.5.4 | WebSocket 客户端 |
| [![Gson](https://img.shields.io/badge/Gson-2.10.1-8E44AD?style=flat-square&logo=json&logoColor=white)](https://github.com/google/gson) | 2.10.1 | JSON 解析 |
| [![Brigadier](https://img.shields.io/badge/Brigadier-1.2.9-F59E0B?style=flat-square)](https://github.com/Mojang/brigadier) | 1.2.9 | 命令系统 |

### 构建配置

| 配置项 | 值 | 说明 |
|:---|:---|:---|
| `mod_version` | 0.1.1-alpha.1 | 模组版本 |
| `maven_group` | me.vincentzyu.qwq | Maven 组 ID |
| `archives_base_name` | yolomirror | 构建产物名称 |
| `target_java_version` | 21 | 目标 Java 版本 |

## 安装

1. 下载最新的模组文件（[Releases](https://github.com/vincentzyu/YoloMirror/releases)）
2. 将文件放入 Minecraft 的 `mods` 文件夹
3. 启动游戏

## 使用方法

### 基础命令

```bash
# 设置 roll 角度（度）
/roll <角度>

# 恢复到默认角度（0度）
/roll_recover

# 启动 WebSocket 连接（使用默认地址 ws://0.0.0.0:60321）
/start_roll_mirror

# 启动 WebSocket 连接（使用自定义地址）
/start_roll_mirror <WebSocket URL>

# 停止 WebSocket 连接
/end_roll_mirror

# 查看连接状态
/roll_mirror_status
```

### WebSocket 消息格式

发送到模组的 JSON 消息格式：

```json
{
  "type": "roll_control",
  "angle": 45.0
}
```

## 开发

### 环境要求

- JDK 21
- Gradle 9.2.1

### 构建

```bash
# 使用 build.py 脚本（Windows）
python build.py

# 指定版本号
python build.py --version 0.1.0

# 清除缓存
python build.py --clear
```

### 项目结构

```
src/
├── client/                    # 客户端代码
│   └── java/me/vincentzyu/qwq/yolomirror/
│       ├── client/
│       │   └── YoloMirrorClient.java    # 主客户端类
│       └── mixin/
│           └── client/
│               └── GameRendererMixin.java # 渲染注入
└── main/                      # 主代码
    └── java/me/vincentzyu/qwq/yolomirror/
        └── YoloMirror.java             # 模组主类
```

## 许可证

[MIT License](LICENSE.txt)

## 相关项目

- [Fabric Documentation](https://fabricmc.net/wiki/start:introduction)
- [Fabric API](https://github.com/FabricMC/fabric)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

vincentzyu
