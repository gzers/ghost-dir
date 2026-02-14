# Ghost-Dir 标准化开发规约 (Standardization Guide)

本指南旨在规范项目中的路径处理、输入验证及分类数据交互，以确保系统的健壮性和视觉一致性。

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

---

## 1. 路径标准化 (Path Standardization)

### 1.1 背景
Windows 环境下, `QFileDialog` 或系统 API 可能返回带有 `\\?\` 或 `\\?\UNC\` 前缀的路径。直接使用此类路径会导致逻辑校验失效或 UI 显示异常。

### 1.2 处理规范
所有业务逻辑在接收、存储或显示路径前, **必须**通过 `PathValidator` 进行标准化。

**❌ 禁止的做法:**
```python
path = path.replace("/", "\\")  # 不够健壮
```

**✅ 推荐的做法:**
```python
from src.common.validators import PathValidator

# 标准化路径：移除 UNC 前缀、统一分隔符、清理末尾斜杠
clean_path = PathValidator().normalize(raw_path)
```

---

## 2. GUI 输入校验 (GUI Input Validation)

### 2.1 校验组件
为了统一交互反馈, 涉及路径或名称输入的场景应使用 `ValidatedLineEdit` 组件。

### 2.2 使用示例
```python
from src.gui.components import ValidatedLineEdit
from src.common.validators import PathValidator, NameValidator

# 创建带校验的输入框
self.pathEdit = ValidatedLineEdit(self)
self.pathEdit.addValidator(PathValidator())

# 获取时自动获取清洗后的值
path = self.pathEdit.get_validated_value()
```

---

## 3. 分类系统规范 (Category System)

### 3.1 名称权威来源
分类名称的 **唯一真相来源** 是 `config/categories.json` 中的 `name` 字段。

### 3.2 国际化限制
**禁止** 在 `src/gui/i18n` 翻译字典中硬编码特定的业务分类 ID (如 `hardware`, `social`) 对应的中文名称。国际化仅用于系统通用文案 (如 "全部", "未分类")。

### 3.3 文案获取
必须通过 `get_category_text` 获取显示文案, 它将优先查询 `CategoryManager` 的配置。

**✅ 标准用法:**
```python
from src.gui.i18n import get_category_text

# 传入 ID, 返回配置文件中定义的显示名
display_name = get_category_text(link.category_id)
```

### 3.4 ID 驱动原则
组件间的信号传递 (Signal/Slot) 应优先传递 `category_id` 而非 `category_name`, 以防止名称修改导致逻辑断裂。

### 3.5 绑定限制 (Binding Restriction)
模板必须绑定到具体的一级或二级 **叶子分类 (Leaf Category)**。禁止将模板直接绑定到非叶子节点的父分类下，以确保数据结构的清晰。

---

## 4. UI 渲染规范 (UI Rendering)

### 4.1 路径显示
显示在 Caption 或 Label 上的路径必须经过标准化, 移除 `\\?\` 等技术前缀。

### 4.2 括号处理
除非是特定的 UI 装饰需求, 否则不应在代码中硬编码 `[分类名]` 这种修饰, 应保持显示文案的纯净。

### 4.3 渲染避坑指南 (Critical Rendering Pitfalls)
> [!IMPORTANT]
> **原生渲染优先原则**: 严禁过度自定义官方组件（尤其是 TreeWidget, TableWidget 等复杂容器）的内部子项 (::item) 样式。
- **背景分块问题**: 禁止手动为 `TreeWidget::item:hover` 或 `selected` 设置背景颜色。Fluent 组件自带动态高亮遮罩，手动设置背景会破坏遮罩的层级，导致渲染分块或错位。
- **文字对齐与可见性**: 在禁用非叶子节点时，务必在 QSS 中显式指定 `TreeWidget` 的 `color` 属性，防止系统自动计算的灰度导致文字在特定主题下“消失”。

### 4.4 布局对齐
针对对话框表单，优先使用 `QFormLayout` 进行自动对齐，Label 统一右对齐。

---

## 5. 样式引用规范 (Styling Constants)
严禁在业务逻辑中硬编码像素值或颜色值。应调用 `src.gui.styles` 中的统一接口：
- **间距**: `get_spacing("md")`
- **边距**: `get_layout_margins()["compact"]`
- **主题感知**: 优先使用官方的 `setCustomStyleSheet(widget, lightQss, darkQss)`。

---

## 6. 命名与架构规约 (Naming & Architecture)

### 6.1 模块后缀分类
为了从文件名和类名直观区分业务层与执行层, 遵循以下后缀规范:

- **Service 层 (`src/services`)**:
  - 文件后缀: `*_service.py` (如 `scan_service.py`, `config_service.py`)
  - 类名后缀: `*Service` (如 `CategoryService`, `TemplateService`)
  - 职责: 业务流编排、规则校验、跨模块协同

- **DAO 层 (`src/dao`)**:
  - 文件后缀: `*_dao.py` (如 `template_dao.py`, `link_dao.py`)
  - 类名后缀: `*DAO`
  - 职责: 数据持久化与查询，不承载 UI 与流程编排

- **Drivers 层 (`src/drivers`)**:
  - 文件后缀: 与能力对应 (如 `windows.py`, `transaction.py`, `fs.py`)
  - 职责: 底层原子能力（文件系统、事务、Windows API）

### 6.2 依赖拓扑
- **GUI** 可以调用 **Services**，不直接依赖 DAO/Drivers。
- **Services** 可以调用 **DAO** 与 **Drivers**。
- **DAO/Drivers** 严禁反向导入 `src/services` 或 `src/gui`。
- 底层原子操作应优先封装在 `src/drivers`，避免散落在视图代码中。

---

## 7. UI/UX 交互与布局规约 (UX Standards)

### 7.1 表格垂直居中 (Vertical Alignment)
为了解决自定义单元格组件（如 Badge, Button, ProgressRing）与普通文字在表格行中基线不一致的问题, 遵循 **对齐代理容器 (Alignment Proxy)** 模式。

- **标准高度**: 容器高度固定为 **40px** (与表格默认行高一致)。
- **对齐方式**: 容器布局强制设为 `Qt.AlignmentFlag.AlignVCenter`。
- **工厂方法**: 优先使用基类定义的 `create_alignment_container()` 以保证一致性。

### 7.2 异步操作通知 (Notification Norms)
反馈系统必须遵循全局一致的物理视觉中心。

- **位置规范**: 所有的操作反馈通知 (Success/Error `InfoBar`) 必须统一定位在窗口 **顶部中心**。在调用时传递位置参数字符串 `'TopCenter'`。
- **反馈标准**: 
    - **去冗余化**: 异步执行中 **禁止** 使用 `StateToolTip` (紫色气泡) 进行辅助反馈，以免遮挡操作行或造成视觉噪点。
    - **原生驱动**: 必须直接使用 `InfoBar.success` 或 `InfoBar.error` 静态方法，确保自动带有官方标准的成功/错误图标。

### 7.3 平滑加载动画 (Loading Feedback)
对于任何耗时超过 500ms 的局部操作, **必须** 提供上下文感知的反馈。

- **行内反馈**: 在表格单元格操作中, 必须使用 `IndeterminateProgressRing` (16x16) 替代原始文字或按钮。
- **生命周期绑定**: 加载动画应与异步任务的 `on_start` 和 `on_finished` 回调严格绑定, 禁止让界面进入“无感知的静止”状态。

---

## 8. 常用开发命令 (Dev Cheatsheet)
- **启动应用**: `python debug_start.py`
- **语法检查**: `python -m py_compile [file_path]`
- **安装依赖**: `pip install -r requirements.txt`
