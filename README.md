# Ghost-Dir

<div align="center">

<img src="assets/icon.png" alt="Ghost-Dir" width="128" height="128">

**目录连接管理器 - 安全迁移 C 盘文件**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## ✨ 特性

### 🎯 核心功能
- **智能向导**: 引导式操作，快速扫描本机可管理软件
- **模版库**: 浏览官方和自定义模版，支持搜索和筛选
- **自定义模版**: 保存常用配置为模版，方便快速添加
- **扫描忽略**: 永久忽略不需要的软件，避免重复扫描
- **事务安全**: 零数据丢失保障，原子回滚机制
- **崩溃恢复**: 意外中断自动恢复，确保数据完整性

### 🛡️ 安全保障
- **进程卫士**: 操作前检测文件占用，避免错误
- **路径验证**: 黑名单机制，防止误操作系统目录
- **无缓存移动**: 直接移动文件，不占用双倍空间
- **锁文件机制**: 记录操作状态，支持崩溃恢复

### 🎨 现代 UI
- **Windows 11**: 云母（Mica）半透明效果
- **Windows 10**: 亚克力（Acrylic）毛玻璃效果
- **Fluent Design**: 遵循微软 Fluent 设计语言
- **响应式布局**: 左树右表，批量操作工具栏

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

# 打包
pyinstaller --name="Ghost-Dir" \
            --windowed \
            --icon=assets/icon.ico \
            --add-data="assets;assets" \
            src/main.py
```

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

### 4. 建立连接

在 **"我的连接"** 页面中：
1. 选择一个 **"未连接"** 状态的软件
2. 点击 **"🔗 建立连接"** 按钮
3. 可勾选 **"保存为自定义模版"** 复选框
4. 程序会：
   - 检查文件占用（进程卫士）
   - 移动文件 C → D
   - 创建连接点 C ← D
   - 更新状态为 **"已连接"**

### 5. 断开连接

对于 **"已连接"** 状态的软件：
1. 点击 **"🔌 断开连接"** 按钮
2. 程序会：
   - 删除连接点
   - 移动文件 D → C
   - 恢复到原始状态

### 6. 批量操作

1. 勾选多个软件（复选框）
2. 底部会显示批量操作工具栏
3. 点击 **"批量建立连接"** 或 **"批量断开连接"**
4. 程序会依次处理，自动跳过不适用的项目

## 🏗️ 项目结构

```
ghost-dir/
├── src/                    # 源代码
│   ├── common/            # 公共模块
│   │   ├── config.py      # 全局配置
│   │   ├── signals.py     # 信号总线
│   │   └── resource_loader.py  # 资源加载器
│   ├── core/              # 核心业务逻辑
│   │   ├── transaction.py # 事务管理器 ⭐
│   │   ├── safety.py      # 进程卫士 🛡️
│   │   ├── scanner.py     # 智能扫描器 🔍
│   │   └── link_opt.py    # 连接点操作
│   ├── data/              # 数据层
│   │   ├── model.py       # 数据模型
│   │   ├── template_manager.py  # 模版管理器
│   │   └── user_manager.py      # 用户数据管理器
│   ├── gui/               # 界面层
│   │   ├── app.py         # 应用程序主类
│   │   ├── windows/       # 窗口
│   │   │   └── main_window.py
│   │   ├── views/         # 视图
│   │   │   ├── console/       # 主控制台
│   │   │   ├── wizard/        # 智能向导
│   │   │   ├── library/       # 模版库
│   │   │   ├── help/          # 帮助页面
│   │   │   └── settings/      # 设置页面
│   │   ├── dialogs/       # 对话框
│   │   └── components/    # 组件
│   │       ├── link_table.py    # 连接表格
│   │       └── status_badge.py  # 状态徽章
│   ├── utils/             # 工具
│   │   └── admin.py       # UAC 提权
│   └── main.py            # 程序入口
├── assets/                # 资源文件
│   ├── icon.ico           # 应用图标
│   ├── icon.png           # 应用图标 PNG
│   └── templates.json     # 模版库
├── requirements.txt       # 依赖列表
└── run.py                 # 开发启动脚本
```

## 🔧 核心技术

### 事务管理器 (TransactionManager)

```python
# 使用上下文管理器确保安全
with TransactionManager(src, dst, link_id) as tx:
    tx.establish_link()  # 自动回滚
```

**工作流程**:
1. 写入锁文件 `.ghost.lock`
2. 移动文件 C → D
3. 创建连接点 C ← D
4. 成功：删除锁文件
5. 失败：自动回滚（D → C）

### 进程卫士 (ProcessGuard)

```python
guard = ProcessGuard()
processes = guard.scan_handles(path)
if processes:
    # 显示警告，提供"结束进程"选项
    guard.kill_processes(processes)
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
| 🔴 未连接 | DISCONNECTED | 实体在 C 盘 | 建立连接 |
| 🟢 已连接 | CONNECTED | 实体在 D 盘，C 盘有连接点 | 断开连接 |
| 🟡 就绪 | READY | C 盘无文件，D 盘有文件 | 重新连接 |
| ⚪ 失效 | INVALID | 连接断开或路径不存在 | 删除 |

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

### v7.4 (2026-01-21) ✅

**新增功能**:
- ✅ 智能向导视图：自动扫描本机可管理软件
- ✅ 模版库视图：浏览官方和自定义模版，支持搜索和筛选
- ✅ 自定义模版：保存常用配置为模版
- ✅ 扫描忽略：永久忽略不需要的软件
- ✅ 默认仓库路径配置
- ✅ 日志文件夹快捷访问

**UI 改进**:
- ✅ 5 页面导航：智能向导、我的连接、模版库、帮助、设置
- ✅ View/Widgets 分层：模块化设计，易于维护
- ✅ Fluent Design 设计语言统一

**代码质量**:
- ✅ 导入路径统一
- ✅ 组件职责分离
- ✅ 信号通信机制

## 📝 后续计划

### Phase 5: 集成和测试
- [ ] 完善批量操作逻辑
- [ ] 添加空间分析缓存
- [ ] 单元测试
- [ ] 集成测试

### Phase 6: 优化和打包
- [ ] 性能优化
- [ ] 错误处理完善
- [ ] PyInstaller 打包配置
- [ ] 安装程序制作

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
