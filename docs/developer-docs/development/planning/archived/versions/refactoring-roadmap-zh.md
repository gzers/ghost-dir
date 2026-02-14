# Ghost-Dir QFluentWidgets 重构路线图 (Refactoring Roadmap)

- 适用版本: `历史归档`
- 文档状态: `archived`
- 最后更新: `2026-02-10`

本计划旨在将 Ghost-Dir 项目重构为 **100% 符合官方规范** 的代码，消除所有“手写 QSS”和非标准写法。

## 阶段 1: 地基与入口 (Infrastructure)
**目标:** 规范化应用程序初始化和全局主题管理。

### 检查清单 (Checklist)
- [ ] **RHI 后端:** 在 `src/main.py` 中保留 `os.environ["QSG_RHI_BACKEND"] = "d3d12"` 配置，确保 Windows 稳定性。
- [ ] **主题管理:** 使用 `setTheme(Theme.AUTO)` 替换所有手动的主题检测逻辑。
- [ ] **字体规范化:** 在 `app.py` 中调用 `setFontFamilies(['Segoe UI', 'Microsoft YaHei', 'PingFang SC'])`。
- [ ] **高分屏适配:** 确保正确设置 `AA_EnableHighDpiScaling` 等高 DPI 属性。
- [ ] **应用信息:** 使用 `setApplicationName` 和 `setApplicationVersion` 规范化信息。

### 核心文件
- `src/main.py`
- `src/gui/app.py`

---

## 阶段 2: 骨架与导航 (Shell & Navigation)
**目标:** 充分利用 `FluentWindow` 的内置功能处理窗口结构和特效。

### 检查清单 (Checklist)
- [ ] **继承关系:** 确保 `MainWindow` 继承自 `FluentWindow`。
- [ ] **导航实现:** 使用 `addSubInterface()` 添加所有界面，并为每个界面提供唯一的 `objectName`。
- [ ] **云母效果 (Mica):** 移除手动编写的透明 QSS；使用 `FluentWindow` 原生的 Mica 效果支持。
- [ ] **特效同步:** 确保在主题切换时正确处理 `windowEffect.setMicaEffect`。
- [ ] **布局清理:** 移除导航组件上冗余的 `apply_transparent_style` 手动调用。

### 核心文件
- `src/gui/windows/main_window.py`

---

## 阶段 3: 页面组件标准化 (Page & Components)
**目标:** 将所有原生 Qt 控件替换为对应的 Fluent 组件。

### 检查清单 (Checklist)
- [ ] **按钮替换:** 
    - `QPushButton` -> `PushButton` / `PrimaryPushButton` / `TransparentPushButton`
- [ ] **标签替换:** 
    - `QLabel` -> `TitleLabel` / `SubtitleLabel` / `BodyLabel` / `CaptionLabel`
- [ ] **输入框替换:** 
    - `QLineEdit` -> `LineEdit` / `SearchLineEdit`
- [ ] **图标规范化:** 
    - 将所有字符串路径替换为 `FluentIcon` 枚举（如 `FluentIcon.HOME`）。
    - 对于仅支持 `QIcon` 的旧组件，使用 `FluentIconBase.qicon()`。
- [ ] **样式清理:** 
    - **严禁:** 彻底删除所有手动调用的 `setStyleSheet`。
    - 仅在微调时允许使用 `setCustomStyleSheet(widget, lightQss, darkQss)`。

### 核心文件
- `src/gui/views/*.py`
- `src/gui/views/*/widgets/*.py`

---

## 阶段 4: 交互与反馈 (Interaction)
**目标:** 现代化用户反馈和交互机制。

### 检查清单 (Checklist)
- [ ] **对话框替换:** 
    - `QMessageBox` (阻塞式确认) -> `MessageDialog`。
    - `QMessageBox` (轻量提示) -> `InfoBar`。
- [ ] **进度反馈:** 
    - 对于耗时操作，使用 `IndeterminateProgressBar` (无确定进度条)。
- [ ] **过渡动画:** 
    - 利用 `FluentWindow` 内置的 `StackedWidget` 确保界面切换流畅。

### 核心文件
- `src/gui/` 下的全局逻辑

---

Master, 我们可以开始第一阶段了吗？
