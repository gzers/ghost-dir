# Ghost-Dir 设计模式应用

## 概述

本文档记录 Ghost-Dir 项目中使用的设计模式及其应用场景。

---

## 1. 单例模式 (Singleton Pattern)

### 应用场景

**全局信号对象**

### 实现

```python
# src/common/signals.py
from PySide6.QtCore import QObject, Signal

class GlobalSignals(QObject):
    """全局信号单例"""
    theme_changed = Signal(str)
    theme_color_changed = Signal(str)
    links_updated = Signal()
    categories_updated = Signal()
    templates_updated = Signal()

# 创建全局单例实例
global_signals = GlobalSignals()
```

### 使用

```python
from src.common.signals import global_signals

# 发送信号
global_signals.links_updated.emit()

# 连接信号
global_signals.theme_changed.connect(self.on_theme_changed)
```

### 优势

- 全局唯一的信号对象
- 避免重复创建
- 统一的事件通信中心

---

## 2. 管理器模式 (Manager Pattern)

### 应用场景

**数据和业务逻辑管理**

### 实现

```python
# CategoryManager - 分类管理
class CategoryManager:
    def __init__(self):
        self.categories: Dict[str, CategoryNode] = {}
        self.load_categories()
    
    def get_all_categories(self) -> List[CategoryNode]:
        """获取所有分类"""
    
    def add_category(self, category: CategoryNode) -> Tuple[bool, str]:
        """添加分类"""
    
    def delete_category(self, category_id: str) -> Tuple[bool, str]:
        """删除分类"""

# TemplateManager - 模板管理
class TemplateManager:
    def get_all_templates(self) -> List[Template]:
        """获取所有模板"""
    
    def add_template(self, template: Template) -> bool:
        """添加模板"""

# UserManager - 用户数据管理
class UserManager:
    def get_all_links(self) -> List[UserLink]:
        """获取所有链接"""
    
    def add_link(self, link: UserLink) -> bool:
        """添加链接"""
```

### 优势

- 集中管理相关数据
- 封装业务逻辑
- 提供统一的API接口
- 便于测试和维护

---

## 3. 数据类模式 (Data Class Pattern)

### 应用场景

**数据模型定义**

### 实现

```python
# src/data/model.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class CategoryNode:
    """分类节点数据类"""
    id: str
    name: str
    icon: str
    parent_id: Optional[str]
    order: int
    depth: int

@dataclass
class Template:
    """模板数据类"""
    id: str
    name: str
    default_src: str
    category: str
    icon: str
    description: str

@dataclass
class UserLink:
    """用户链接数据类"""
    id: str
    name: str
    source_path: str
    target_path: str
    category: str
    template_id: Optional[str]
    icon: str
```

### 优势

- 自动生成`__init__`、`__repr__`等方法
- 类型注解提供IDE支持
- 代码简洁清晰
- 易于序列化/反序列化

---

## 4. 策略模式 (Strategy Pattern)

### 应用场景

**分类冲突处理**

### 实现

```python
# src/data/category_manager.py
def add_category_with_conflict(
    self,
    category: CategoryNode,
    conflict_strategy: str = "skip"
) -> Tuple[str, bool]:
    """
    添加分类(支持冲突处理)
    
    Args:
        category: 分类对象
        conflict_strategy: 冲突策略 (skip, overwrite, rename)
    """
    if category.id in self.categories:
        if conflict_strategy == "skip":
            return category.id, False
        elif conflict_strategy == "overwrite":
            self.categories[category.id] = category
            return category.id, False
        elif conflict_strategy == "rename":
            new_id = self._generate_unique_id(category.id)
            category.id = new_id
            self.categories[new_id] = category
            return new_id, True
    
    self.categories[category.id] = category
    return category.id, False
```

### 优势

- 灵活的冲突处理
- 易于扩展新策略
- 调用方可选择策略

---

## 5. 观察者模式 (Observer Pattern)

### 应用场景

**Qt信号槽机制**

### 实现

```python
# 发布者
class ScanWorker(QThread):
    # 定义信号
    progress = Signal(int, int)  # 当前, 总数
    finished = Signal(list)      # 完成
    error = Signal(str)          # 错误
    
    def run(self):
        # 发送进度信号
        self.progress.emit(current, total)
        
        # 发送完成信号
        self.finished.emit(results)

# 订阅者
class WizardView(QWidget):
    def __init__(self):
        self.worker = ScanWorker()
        
        # 连接信号
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
    
    def on_progress(self, current, total):
        """处理进度更新"""
    
    def on_finished(self, results):
        """处理完成事件"""
```

### 优势

- 解耦发布者和订阅者
- 一对多通信
- 动态添加/移除观察者
- 线程安全(Qt自动处理)

---

## 6. 工厂模式 (Factory Pattern)

### 应用场景

**组件创建**

### 实现

```python
# src/gui/components/card.py
class Card(QWidget):
    @staticmethod
    def create_info_card(title: str, content: str) -> 'Card':
        """创建信息卡片"""
        card = Card()
        card.set_title(title)
        card.set_content(content)
        return card
    
    @staticmethod
    def create_action_card(title: str, actions: List[str]) -> 'Card':
        """创建操作卡片"""
        card = Card()
        card.set_title(title)
        card.add_actions(actions)
        return card
```

### 优势

- 封装创建逻辑
- 统一创建接口
- 便于扩展新类型

---

## 7. 模板方法模式 (Template Method Pattern)

### 应用场景

**基础页面组件**

### 实现

```python
# src/gui/components/base_page.py
class BasePage(QWidget):
    """基础页面模板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI(模板方法)"""
        self._setup_layout()
        self._create_header()
        self._create_content()
        self._create_footer()
    
    def _setup_layout(self):
        """设置布局(可重写)"""
        self.layout = QVBoxLayout(self)
    
    def _create_header(self):
        """创建头部(子类实现)"""
        raise NotImplementedError
    
    def _create_content(self):
        """创建内容(子类实现)"""
        raise NotImplementedError
    
    def _create_footer(self):
        """创建底部(可重写)"""
        pass

# 具体页面
class WizardView(BasePage):
    def _create_header(self):
        """实现头部创建"""
        self.header = CardHeader("智能向导", "自动发现可管理的软件")
    
    def _create_content(self):
        """实现内容创建"""
        self.scan_card = ScanProgressCard()
```

### 优势

- 定义算法骨架
- 子类实现具体步骤
- 代码复用
- 统一的页面结构

---

## 8. 组合模式 (Composite Pattern)

### 应用场景

**分类树结构**

### 实现

```python
# src/data/model.py
@dataclass
class CategoryNode:
    """分类节点(可以是叶子或容器)"""
    id: str
    name: str
    icon: str
    parent_id: Optional[str]  # None表示根节点
    order: int
    depth: int

# src/data/category_manager.py
class CategoryManager:
    def get_children(self, parent_id: Optional[str] = None) -> List[CategoryNode]:
        """获取子分类(递归结构)"""
        return [
            cat for cat in self.categories.values()
            if cat.parent_id == parent_id
        ]
    
    def _get_all_descendants(self, category_id: str) -> List[CategoryNode]:
        """获取所有子孙分类(递归)"""
        descendants = []
        children = self.get_children(category_id)
        for child in children:
            descendants.append(child)
            descendants.extend(self._get_all_descendants(child.id))
        return descendants
```

### 优势

- 统一处理叶子和容器
- 树形结构自然表达
- 递归操作简单

---

## 9. 适配器模式 (Adapter Pattern)

### 应用场景

**环境变量路径展开**

### 实现

```python
# src/data/template_manager.py
class TemplateManager:
    def expand_path(self, path: str) -> str:
        """
        展开路径中的环境变量
        适配Windows环境变量到实际路径
        """
        import os
        return os.path.expandvars(path)
    
    # 使用示例
    # "%APPDATA%\\Software" -> "C:\\Users\\User\\AppData\\Roaming\\Software"
```

### 优势

- 适配不同的路径格式
- 隐藏环境变量细节
- 统一的路径处理

---

## 10. 命令模式 (Command Pattern)

### 应用场景

**事务操作(规划中)**

### 设计

```python
# 未来实现
class Command:
    """命令接口"""
    def execute(self):
        raise NotImplementedError
    
    def undo(self):
        raise NotImplementedError

class CreateLinkCommand(Command):
    """创建链接命令"""
    def __init__(self, link: UserLink):
        self.link = link
    
    def execute(self):
        """执行创建"""
        user_manager.add_link(self.link)
    
    def undo(self):
        """撤销创建"""
        user_manager.delete_link(self.link.id)

class Transaction:
    """事务管理器"""
    def __init__(self):
        self.commands = []
    
    def add_command(self, command: Command):
        self.commands.append(command)
    
    def commit(self):
        """提交所有命令"""
        for cmd in self.commands:
            cmd.execute()
    
    def rollback(self):
        """回滚所有命令"""
        for cmd in reversed(self.commands):
            cmd.undo()
```

### 优势

- 操作可撤销
- 事务原子性
- 操作历史记录

---

## 设计模式总结

| 模式 | 应用场景 | 主要优势 |
|------|---------|---------|
| 单例模式 | 全局信号 | 全局唯一,统一通信 |
| 管理器模式 | 数据管理 | 集中管理,统一API |
| 数据类模式 | 数据模型 | 简洁清晰,类型安全 |
| 策略模式 | 冲突处理 | 灵活可扩展 |
| 观察者模式 | 信号槽 | 解耦,一对多通信 |
| 工厂模式 | 组件创建 | 封装创建逻辑 |
| 模板方法模式 | 基础页面 | 代码复用,统一结构 |
| 组合模式 | 分类树 | 统一处理,递归简单 |
| 适配器模式 | 路径展开 | 适配不同格式 |
| 命令模式 | 事务操作 | 可撤销,原子性 |

---

## 最佳实践

### 1. 选择合适的模式

- 不要为了使用模式而使用模式
- 根据实际需求选择
- 保持代码简洁

### 2. 模式组合

- 多个模式可以组合使用
- 例如: 单例 + 观察者(GlobalSignals)
- 例如: 管理器 + 策略(CategoryManager)

### 3. 避免过度设计

- 简单问题简单解决
- 复杂问题才考虑模式
- 保持YAGNI原则(You Aren't Gonna Need It)

---

## 相关文档

- [系统架构](../overview/system-architecture.md) - 整体架构
- [核心模块](../overview/core-modules.md) - 模块详解
- [组件架构](../overview/component-architecture.md) - GUI组件

---

**最后更新**: 2026-01-28
