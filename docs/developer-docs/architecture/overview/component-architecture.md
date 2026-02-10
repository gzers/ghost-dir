# 组件化架构说明

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

## 概述

本项目采用完全组件化的架构设计，每个组件都有独立的文件，职责清晰，易于维护和复用。

## 组件文件结构

### 扫描向导相关组件

```
src/gui/views/wizard/widgets/
├── __init__.py                 # 组件导出
├── scan_worker.py              # 扫描工作线程（独立文件）
├── scan_progress.py            # 扫描进度卡片（独立文件）
└── scan_result_card.py         # 扫描结果卡片（独立文件）
```

### 通用可复用组件

```
src/gui/components/
├── __init__.py                 # 组件导出
├── card.py                     # 基础卡片组件
├── card_header.py              # 卡片头部组件（新增）
├── progress_indicator.py       # 进度指示器组件（新增）
├── status_badge.py             # 状态徽章组件
├── action_button_group.py      # 操作按钮组组件
├── empty_state.py              # 空状态组件
├── info_card.py                # 信息卡片组件
├── link_table.py               # 链接表格组件
└── base_page.py                # 基础页面组件
```

## 组件化原则

### 1. 单一职责原则
每个组件只负责一个明确的功能：
- ✅ `ScanWorker` - 只负责后台扫描任务
- ✅ `CardHeader` - 只负责卡片头部显示
- ✅ `ProgressIndicator` - 只负责进度显示
- ✅ `ScanProgressCard` - 只负责组合和协调

### 2. 独立文件原则
每个组件都有独立的文件：
- ✅ 便于查找和定位
- ✅ 避免文件过大
- ✅ 减少合并冲突
- ✅ 提高可维护性

### 3. 可复用原则
组件设计时考虑复用性：
- ✅ `CardHeader` 可用于任何卡片
- ✅ `ProgressIndicator` 可用于任何需要进度显示的场景
- ✅ `ScanWorker` 可用于任何后台扫描任务

### 4. 清晰的 API 原则
每个组件提供清晰的公共接口：
- ✅ 明确的方法命名
- ✅ 完整的类型注解
- ✅ 详细的文档字符串
- ✅ 合理的信号定义

## 组件依赖关系

### 层次结构

```
应用层 (wizard_view.py)
    ↓ 使用
业务组件层 (scan_progress.py, scan_result_card.py)
    ↓ 使用
通用组件层 (card_header.py, progress_indicator.py)
    ↓ 使用
基础组件层 (card.py, qfluentwidgets)
    ↓ 使用
样式系统 (styles/)
    ↓ 使用
国际化系统 (i18n/)
```

### 依赖规则

1. **向下依赖** - 上层可以依赖下层，下层不能依赖上层
2. **同层独立** - 同层组件之间尽量独立，避免相互依赖
3. **接口隔离** - 通过信号和槽机制解耦组件

## 组件详细说明

### ScanWorker (扫描工作线程)

**文件：** `src/gui/views/wizard/widgets/scan_worker.py`

**职责：**
- 在后台线程执行扫描任务
- 避免阻塞 UI 线程
- 通过信号通知主线程

**信号：**
- `progress(int, int)` - 扫描进度
- `finished(list)` - 扫描完成
- `error(str)` - 扫描错误

**使用场景：**
- 任何需要后台扫描的场景
- 需要避免 UI 冻结的长时间操作

### CardHeader (卡片头部)

**文件：** `src/gui/components/card_header.py`

**职责：**
- 显示卡片的图标、标题和副标题
- 使用统一的样式系统
- 提供动态更新接口

**方法：**
- `set_title(title)` - 设置标题
- `set_subtitle(subtitle)` - 设置副标题

**使用场景：**
- 任何需要标准化卡片头部的场景
- 需要图标+标题+副标题组合的地方

### ProgressIndicator (进度指示器)

**文件：** `src/gui/components/progress_indicator.py`

**职责：**
- 显示进度条和状态文本
- 支持确定和不确定进度
- 提供清晰的状态管理 API

**方法：**
- `start_indeterminate()` - 开始不确定进度
- `set_progress(current, total)` - 设置确定进度
- `set_status(text)` - 设置状态文本
- `complete()` - 完成进度
- `hide_progress()` - 隐藏进度条
- `reset()` - 重置状态

**使用场景：**
- 任何需要显示进度的场景
- 文件下载、数据处理等长时间操作

### ScanProgressCard (扫描进度卡片)

**文件：** `src/gui/views/wizard/widgets/scan_progress.py`

**职责：**
- 组合 CardHeader 和 ProgressIndicator
- 管理扫描流程的 UI 状态
- 提供扫描相关的操作按钮

**信号：**
- `scan_clicked()` - 扫描按钮点击
- `import_clicked()` - 导入按钮点击
- `refresh_clicked()` - 刷新按钮点击
- `cancel_clicked()` - 取消按钮点击

**方法：**
- `start_scanning()` - 开始扫描状态
- `update_progress(current, total)` - 更新进度
- `scan_finished(discovered_count, selected_count)` - 扫描完成
- `scan_error(error_msg)` - 扫描出错
- `update_selected_count(count)` - 更新选中数量
- `reset()` - 重置状态

**使用场景：**
- 智能向导页面的扫描功能
- 任何需要扫描+导入流程的场景

## 组件化的优势

### 1. 可维护性 ⬆️
- 每个组件职责清晰，易于理解
- 修改一个组件不影响其他组件
- 独立文件便于查找和定位

### 2. 可复用性 ⬆️
- 通用组件可在多处使用
- 减少代码重复
- 提高开发效率

### 3. 可测试性 ⬆️
- 每个组件可独立测试
- 便于编写单元测试
- 提高代码质量

### 4. 可扩展性 ⬆️
- 新增功能只需添加新组件
- 不影响现有组件
- 降低系统复杂度

### 5. 团队协作 ⬆️
- 不同开发者可并行开发不同组件
- 减少代码冲突
- 提高开发效率

## 最佳实践

### 创建新组件时

1. **确定职责** - 明确组件的单一职责
2. **独立文件** - 为组件创建独立的文件
3. **清晰 API** - 设计清晰的公共接口
4. **类型注解** - 添加完整的类型注解
5. **文档完善** - 编写详细的文档字符串
6. **样式系统** - 使用统一的样式系统
7. **国际化** - 使用 i18n 系统管理文案
8. **信号机制** - 使用信号和槽解耦组件

### 使用组件时

1. **按需导入** - 只导入需要的组件
2. **遵循接口** - 通过公共 API 使用组件
3. **避免侵入** - 不要直接访问组件内部属性
4. **信号连接** - 通过信号和槽通信
5. **资源管理** - 及时清理不再使用的组件

## 文件组织规范

### 组件文件模板

```python
"""
组件名称
组件描述
"""
from PySide6.QtWidgets import ...
from PySide6.QtCore import ...

from ...styles import ...
from ...i18n import t


class ComponentName(BaseClass):
    """
    组件类
    
    详细描述组件的功能和用途
    """
    
    # 信号定义
    signal_name = Signal(...)
    
    def __init__(self, parent=None):
        """
        初始化组件
        
        Args:
            parent: 父组件
        """
        super().__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """初始化 UI（私有方法）"""
        pass
    
    def public_method(self, arg: type) -> type:
        """
        公共方法
        
        Args:
            arg: 参数描述
            
        Returns:
            返回值描述
        """
        pass
```

### 导出规范

在 `__init__.py` 中明确导出：

```python
"""
模块描述
"""
from .component1 import Component1
from .component2 import Component2

__all__ = ['Component1', 'Component2']
```

## 总结

通过完全的组件化架构，我们实现了：

✅ **每个组件一个文件** - 清晰的文件组织  
✅ **单一职责** - 每个组件职责明确  
✅ **高度复用** - 通用组件可在多处使用  
✅ **易于维护** - 修改影响范围小  
✅ **便于测试** - 每个组件可独立测试  
✅ **团队协作** - 减少代码冲突  

这种架构为项目的长期发展提供了坚实的基础。
