<div align="center">

<img src="assets/icon.png" alt="Ghost-Dir" width="128" height="128">

# Ghost-Dir

[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)](docs/release/CHANGELOG.md)

Windows 跨磁盘目录迁移与连接管理工具。

支持在任意磁盘间无缝迁移文件夹，保持路径有效。内置原子事务回滚、进程阻断卫士与智能模版引擎。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## ✨ 特性

### 🎯 核心功能
- **智能向导**: 提供引导式操作流程，支持快速扫描并自动发现本机可管理的各类软件。
- **动态模版库**: 内置丰富的官方模版并支持用户自定义，提供高效的搜索、筛选与分类管理功能。
- **扫描忽略机制**: 支持将特定软件永久加入忽略列表，精简扫描结果，避免重复信息的干扰。
- **原子事务安全**: 核心操作基于事务引擎开发，提供零数据丢失保障，失败时可实现原子级回滚。
- **全自动崩溃恢复**: 若操作过程中意外中断，系统会在下次启动时自动引导并恢复数据完整性。

### 🛡️ 安全保障
- **实时进程卫士**: 迁移前智能检测文件占用状态，防止由于进程冲突导致的目录操作失败。
- **高级路径验证**: 建立黑名单过滤机制，严禁操作 C 盘根目录或系统核心文件夹，规避系统风险。
- **原生文件迁移**: 采用直接移动（Move）而非复制再删除的方式，确保不额外占用磁盘双倍空间。
- **锁文件状态记录**: 通过持久化的锁文件（Lock File）记录操作每一步状态，为异常恢复提供底层依据。

### 🎨 现代 UI 特性
- **原生系统动效**: 完美适配 Windows 11 的云母（Mica）特效与 Windows 10 的亚克力（Acrylic）毛玻璃效果。
- **Fluent Design 系统**: 界面遵循微软 Fluent 设计语言规范，采用现代化配色方案，视觉感受高端优雅。
- **高效交互布局**: 采用经典的左树右表响应式结构，辅以沉浸式导航栏与动态显示的批量操作工具栏。

## 📦 安装

### 环境要求
- Windows 10/11
- Python 3.8+
- 管理员权限（创建连接点需要）

### 安装依赖

```bash
# 使用清华镜像源（推荐）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用默认源
pip install -r requirements.txt
```

### 依赖说明
- `PySide6`: Qt 6 Python 绑定
- `PySide6-Fluent-Widgets[full]`: Fluent UI 组件库（必须使用 full 版本以启用特效）
- `psutil`: 进程管理
- `pywin32`: Windows API 支持
- `Pillow`: 图像处理

## 🚀 使用

### 开发模式运行

```bash
python run.py
```

**注意**: 程序会自动请求管理员权限，请在 UAC 提示时点击"是"。

### 打包为 exe

```bash
# 安装 PyInstaller
pip install pyinstaller

# 使用 .spec 文件打包
pyinstaller Ghost-Dir.spec
```

打包完成后，可执行文件位于 `dist/Ghost-Dir/Ghost-Dir.exe`。

## 📖 使用指南

### 1. 首次启动

程序启动时会：
1. 请求管理员权限
2. 检查是否有未完成的操作（崩溃恢复）
3. 加载模版库和用户数据

### 2. 智能向导

切换到 **"智能向导"** 页面：
1. 点击 **"开始扫描"** 按钮
2. 自动扫描本机，发现可管理的软件
3. 勾选需要管理的项目
4. 点击 **"一键导入"** 批量添加到管理列表
5. 可右键点击软件选择 **"永久忽略"**

### 3. 模版库

切换到 **"模版库"** 页面：
- 浏览所有官方和自定义模版
- 使用搜索框快速查找模版
- 按分类或类型（官方/自定义）筛选
- 点击模版卡片查看详情

### 4. 建立链接

在 **"我的链接"** 页面中：
1. 选择一个 **"未链接"** 状态的软件
2. 点击 **"🔗 建立链接"** 按钮
3. 可勾选 **"保存为自定义模版"** 复选框
4. 程序会：
   - 检查文件占用（进程卫士）
   - 移动文件到目标位置
   - 创建链接点
   - 更新状态为 **"已链接"**

### 5. 断开链接

对于 **"已链接"** 状态的软件：
1. 点击 **"🔌 断开链接"** 按钮
2. 程序会：
   - 删除链接点
   - 移动文件回源位置
   - 恢复到原始状态

### 6. 批量操作

1. 勾选多个软件（复选框）
2. 底部会显示批量操作工具栏
3. 点击 **"批量建立链接"** 或 **"批量断开链接"**
4. 程序会依次处理，自动跳过不适用的项目

## 🏗️ 架构设计

### 五层金字塔架构

Ghost-Dir 采用严格的五层金字塔架构,确保代码清晰、可维护、易测试:

```
               [GUI 表现层]
                 │    │
      ┌──────────┘    │
      │               ↓
      │          [Services 业务层] ────────────┐
      │           │            │               │
      │           ↓            ↓               │
      │      [Drivers 驱动层] [DAO 数据层]     │
      │           │            │               │
      └─────┬─────┴──────┬─────┴───────┘       │
            │            │                     │
            ↓            ↓                     │
        [Models 数据定义] [Common 基础层] <──────┘
            │            │
            └─────┬──────┘
                  ↓
         [Python 标准库]
```

### 层级职责

| 层级 | 职责 | 依赖 |
|------|------|------|
| **GUI** | 用户交互、数据展示 | Services, Models, Common |
| **Services** | 业务逻辑编排、流程控制 | DAO, Drivers, Models, Common |
| **DAO** | 数据持久化 (JSON) | Models, Common |
| **Drivers** | 系统底层操作 (Junction, 进程) | Models (可选), Common |
| **Models** | 数据结构定义、基础验证 | Common (仅限) |
| **Common** | 全局配置、异常、工具 | 无 (只用标准库) |

### 核心原则

- ✅ **依赖单向向下**: 上层依赖下层,绝不反向
- ✅ **Models 和 Common 是基础**: 所有层都可以使用,但它们不依赖任何层
- ✅ **职责单一**: 每层只做自己的事,不越界
- ❌ **严禁循环依赖**: 通过依赖规则防止架构混乱

详细架构文档: [架构文档](docs/architecture/README.md)

## 🏗️ 项目结构

```
ghost-dir/
├── src/                    # 源代码
│   ├── models/            # Level 4: 数据定义层
│   │   ├── template.py    # Template 实体
│   │   ├── link.py        # UserLink 实体
│   │   └── category.py    # CategoryNode 实体
│   ├── dao/               # Level 3: 数据访问层
│   │   ├── template_dao.py # 模板数据持久化
│   │   ├── link_dao.py     # 链接数据持久化
│   │   └── category_dao.py # 分类数据持久化
│   ├── drivers/           # Level 3: 底层驱动层
│   │   ├── windows.py     # Junction, UAC ⭐
│   │   ├── fs.py          # 文件系统操作
│   │   ├── transaction.py # 事务管理器 🛡️
│   │   └── process.py     # 进程检测 🔍
│   ├── services/          # Level 2: 业务逻辑层
│   │   ├── template_svc.py # 模板业务逻辑
│   │   ├── link_svc.py     # 链接业务逻辑
│   │   └── category_svc.py # 分类业务逻辑
│   ├── gui/               # Level 1: 表现层
│   │   ├── app.py         # 应用程序主类
│   │   ├── windows/       # 窗口
│   │   │   └── main_window.py
│   │   ├── views/         # 视图
│   │   │   ├── links/         # 链接管理
│   │   │   ├── wizard/        # 智能向导
│   │   │   ├── library/       # 模版库
│   │   │   ├── help/          # 帮助页面
│   │   │   └── settings/      # 设置页面
│   │   ├── dialogs/       # 对话框
│   │   └── components/    # 组件
│   │       ├── link_table.py    # 连接表格
│   │       └── status_badge.py  # 状态徽章
│   ├── common/            # Level 5: 全局基础层
│   │   ├── config.py      # 全局配置
│   │   ├── signals.py     # 信号总线
│   │   ├── exceptions.py  # 自定义异常
│   │   └── utils.py       # 工具函数
│   └── main.py            # 程序入口
├── assets/                # 资源文件
│   ├── icon.ico           # 应用图标
│   ├── icon.png           # 应用图标 PNG
│   └── templates.json     # 模版库
├── docs/                  # 文档
│   ├── developer-docs/    # 开发文档
│   │   └── architecture/  # 架构文档
│   ├── user-docs/         # 用户文档
│   └── release/           # 发布说明
├── docs/architecture/README.md # 架构设计文档
├── requirements.txt       # 依赖列表
└── run.py                 # 开发启动脚本

## 🔧 核心技术

### 事务管理引擎 (TransactionEngine)

位于 `drivers/transaction.py`,提供原子操作保证:

```python
from src.drivers import TransactionEngine

# 使用上下文管理器确保安全
with TransactionEngine(src, dst, link_id) as tx:
    tx.establish_link()  # 失败自动回滚
```

**工作流程**:
1. 写入锁文件 `.ghost.lock`
2. 移动文件到目标位置
3. 创建 Junction 连接点
4. 成功：删除锁文件
5. 失败：自动回滚到原始状态

### Windows 驱动 (windows.py)

封装 Windows API 操作:

```python
from src.drivers.windows import create_junction, is_admin

# 检查管理员权限
if not is_admin():
    raise PermissionError("需要管理员权限")

# 创建 Junction
create_junction(source, target)
```

### 进程检测 (process.py)

检测文件占用状态:

```python
from src.drivers.process import is_process_running

if is_process_running("steam.exe"):
    # 显示警告，提供"结束进程"选项
    pass
```

### 崩溃恢复

启动时检查 `.ghost.lock` 文件：
- 存在 → 上次操作异常中断
- 读取记录 → 自动恢复到操作前状态
- 删除锁文件 → 恢复完成

## 🎨 UI 设计

### 状态系统

| 状态 | 图标 | 说明 | 操作 |
|------|------|------|------|
| 🔴 未链接 | DISCONNECTED | 实体在源位置 | 建立链接 |
| 🟢 已链接 | CONNECTED | 实体在目标位置，源位置有链接点 | 断开链接 |
| 🟡 就绪 | READY | 源位置无文件，目标位置有文件 | 重新链接 |
| ⚪ 失效 | INVALID | 链接断开或路径不存在 | 删除 |

### 窗口特效

- **Windows 11**: 自动启用 Mica 云母效果
- **Windows 10**: 自动启用 Acrylic 亚克力效果
- **其他系统**: 回退到纯色背景

## ⚠️ 注意事项

### 安全提示

1. **管理员权限**: 创建连接点必须以管理员身份运行
2. **路径黑名单**: 禁止操作以下目录：
   - `C:\`
   - `C:\Windows`
   - `C:\Program Files`
   - `C:\Users`
3. **数据备份**: 虽然有回滚机制，但建议重要数据提前备份

### 已知限制

1. **仅支持 Windows**: 连接点（Junction）是 Windows 特有功能
2. **需要 NTFS**: 目标驱动器必须是 NTFS 文件系统
3. **不支持跨驱动器**: 连接点只能在同一物理驱动器内工作（符号链接可以，但本项目使用 Junction）

## 📝 版本历史

### v1.0.2 (2026-02-26)

查看完整更新日志：[CHANGELOG.md](docs/release/CHANGELOG.md)  
查看发布说明：[v1.0.2.md](docs/release/notes/v1.0.2.md)

### v1.0.1 (2026-02-17)

查看完整更新日志：[CHANGELOG.md](docs/release/CHANGELOG.md)  
查看发布说明：[v1.0.1.md](docs/release/notes/v1.0.1.md)

### v1.0.0 (2026-02-04) 🎉

查看完整更新日志：[CHANGELOG.md](docs/release/CHANGELOG.md)  
查看发布说明：[v1.0.0.md](docs/release/notes/v1.0.0.md)

## 📝 后续计划

### ✅ 已完成
- [x] **术语统一**：将 `connected` 重命名为 `links`，国际化文案"连接"改为"链接"

### 🚧 进行中

#### 核心架构优化重构
- [ ] 服务层解耦：将业务逻辑从 Manager 迁移到独立 Service 层
- [ ] 事务引擎增强：支持嵌套事务和更细粒度的回滚点
- [ ] 异步操作优化：统一异步任务管理，避免 UI 阻塞
- [ ] 错误处理标准化：建立统一的异常体系和错误码
- [ ] 依赖注入完善：实现完整的 DI 容器，减少硬编码依赖

#### 配置系统改进
- [ ] 配置导出/导入功能：支持备份和迁移用户配置
- [ ] 配置版本管理：自动处理配置文件格式升级
- [ ] 配置验证增强：更严格的 JSON Schema 校验

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [PySide6](https://www.qt.io/qt-for-python) - Qt for Python
- [PySide6-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) - Fluent Design 组件库
- [psutil](https://github.com/giampaolo/psutil) - 跨平台进程管理

---

<div align="center">

**Made with ❤️ by Ghost-Dir Team**

</div>

