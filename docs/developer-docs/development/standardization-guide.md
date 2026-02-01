# Ghost-Dir 标准化开发规约 (Standardization Guide)

本指南旨在规范项目中的路径处理、输入验证及分类数据交互，以确保系统的健壮性和视觉一致性。

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

---

## 4. UI 渲染规范

- **路径显示**: 显示在 Caption 或 Label 上的路径必须经过标准化, 移除 `\\?\` 等技术前缀。
- **括号处理**: 除非是特定的 UI 装饰需求, 否则不应在代码中硬编码 `[分类名]` 这种修饰, 应保持显示文案的纯净。
