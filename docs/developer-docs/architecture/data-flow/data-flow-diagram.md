# Ghost-Dir 数据流图

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

## 概述

本文档描述 Ghost-Dir 系统中数据的流转过程,帮助理解各模块间的交互关系。

## 整体数据流

```mermaid
graph LR
    subgraph "数据源"
        FS[文件系统]
        API[远程API]
        User[用户输入]
    end
    
    subgraph "数据层"
        JSON[JSON文件]
        Cache[内存缓存]
    end
    
    subgraph "业务层"
        TM[TemplateManager]
        CM[CategoryManager]
        UM[UserManager]
    end
    
    subgraph "表现层"
        Views[Views]
    end
    
    FS -->|扫描| TM
    API -->|获取模板| TM
    User -->|操作| Views
    
    TM <-->|读写| JSON
    CM <-->|读写| JSON
    UM <-->|读写| JSON
    
    TM -->|缓存| Cache
    
    Views -->|调用| TM
    Views -->|调用| CM
    Views -->|调用| UM
```

---

## 关键流程数据流

### 1. 应用启动流程

```mermaid
sequenceDiagram
    participant Main
    participant App
    participant UM as UserManager
    participant CM as CategoryManager
    participant TM as TemplateManager
    participant Window as MainWindow
    
    Main->>App: 创建应用实例
    App->>UM: 初始化用户管理器
    UM->>UM: 加载user_data.json
    App->>CM: 初始化分类管理器
    CM->>CM: 加载categories.json
    App->>TM: 初始化模板管理器
    TM->>TM: 加载default_templates.json
    TM->>TM: 加载template_cache.json
    App->>Window: 创建主窗口
    Window->>UM: 获取启动页配置
    UM-->>Window: startup_page
    Window->>Window: 显示对应视图
```

### 2. 智能扫描流程

```mermaid
sequenceDiagram
    participant User
    participant WizardView
    participant ScanWorker
    participant Scanner
    participant TM as TemplateManager
    participant UM as UserManager
    participant FS as FileSystem

    User->>WizardView: 点击扫描按钮
    WizardView->>ScanWorker: 启动扫描线程
    ScanWorker->>Scanner: scan()

    Scanner->>TM: get_all_templates()
    TM-->>Scanner: 所有模板列表

    Scanner->>UM: get_all_links()
    UM-->>Scanner: 已有链接列表

    Scanner->>UM: get_ignored_templates()
    UM-->>Scanner: 忽略列表

    loop 阶段1-3: 遍历每个模板
        Scanner->>TM: expand_path(template.default_src)
        TM-->>Scanner: 展开后的路径
        Scanner->>FS: 检查路径是否存在
        FS-->>Scanner: 存在性结果
        Scanner->>Scanner: 过滤已忽略/已添加/不存在
    end

    loop 阶段4: 全盘 Junction 探测
        Scanner->>FS: is_junction() / get_real_path()
        FS-->>Scanner: Junction 检测结果
        Scanner->>Scanner: 构造伪 Template (is_custom=True)
    end

    Scanner-->>ScanWorker: 发现的模板列表(含伪Template)
    ScanWorker-->>WizardView: finished信号(discovered)
    WizardView->>WizardView: 显示扫描结果
    Note over WizardView: 非模板链接显示 CategorySelector
```

### 3. 导入模板流程

```mermaid
sequenceDiagram
    participant User
    participant WizardView
    participant Scanner
    participant UM as UserManager
    participant Signals as GlobalSignals
    
    User->>WizardView: 选择模板并点击导入
    WizardView->>Scanner: import_templates(selected)
    
    loop 遍历每个模板
        Scanner->>Scanner: 创建UserLink对象
        Scanner->>UM: add_link(link)
        UM->>UM: 验证链接
        UM->>UM: 添加到links列表
        UM->>UM: save_data()
        UM-->>Scanner: 成功/失败
    end
    
    Scanner-->>WizardView: 导入数量
    WizardView->>Signals: links_updated.emit()
    Signals-->>LibraryView: 刷新链接列表
```

### 4. 分类管理流程

```mermaid
sequenceDiagram
    participant User
    participant LibraryView
    participant CM as CategoryManager
    participant TM as TemplateManager
    participant Signals as GlobalSignals
    
    User->>LibraryView: 添加分类
    LibraryView->>CM: add_category(category)
    
    CM->>CM: 验证ID唯一性
    CM->>CM: 验证父分类存在
    CM->>CM: 验证深度限制
    CM->>CM: 检查循环依赖
    
    alt 验证通过
        CM->>CM: 添加到categories字典
        CM->>CM: save_categories()
        CM-->>LibraryView: (True, "成功")
        LibraryView->>Signals: categories_updated.emit()
        Signals-->>Views: 刷新分类树
    else 验证失败
        CM-->>LibraryView: (False, "错误信息")
        LibraryView->>User: 显示错误提示
    end
```

### 5. 模板管理流程

```mermaid
sequenceDiagram
    participant User
    participant SettingsView
    participant TM as TemplateManager
    participant API as TemplateAPI
    participant Cache
    participant Signals
    
    User->>SettingsView: 刷新模板
    SettingsView->>TM: refresh_api_templates()
    
    TM->>API: fetch_templates()
    API->>API: HTTP请求
    API-->>TM: API模板列表
    
    TM->>Cache: 保存到template_cache.json
    TM->>TM: 合并本地+API模板
    TM-->>SettingsView: 模板总数
    
    SettingsView->>Signals: templates_updated.emit()
    Signals-->>WizardView: 刷新可用模板
```

### 6. 主题切换流程

```mermaid
sequenceDiagram
    participant User
    participant SettingsView
    participant UM as UserManager
    participant Signals as GlobalSignals
    participant App
    participant Views
    
    User->>SettingsView: 选择主题
    SettingsView->>UM: set_theme(theme)
    UM->>UM: 更新配置
    UM->>UM: save_data()
    UM-->>SettingsView: 成功
    
    SettingsView->>Signals: theme_changed.emit(theme)
    Signals-->>App: 应用主题
    App->>App: setTheme(theme)
    Signals-->>Views: 更新样式
    Views->>Views: 重新应用样式
```

---

## 数据持久化

### 文件结构

```
.ghost-dir/
├── user_data.json          # 用户数据
├── template_cache.json     # API模板缓存
└── logs/                   # 日志文件

config/
├── default_templates.json  # 内置模板
└── categories.json         # 分类配置
```

### 数据格式

#### user_data.json

```json
{
  "links": [
    {
      "id": "uuid",
      "name": "软件名称",
      "source_path": "C:\\源路径",
      "target_path": "D:\\目标路径",
      "category": "category_id",
      "template_id": "template_id",
      "icon": "icon_name"
    }
  ],
  "ignored_templates": ["template_id1", "template_id2"],
  "settings": {
    "theme": "system",
    "theme_color": "#2F6BFF",
    "startup_page": "wizard",
    "target_drive": "D:\\",
    "target_root": "D:\\Ghost_Library"
  }
}
```

#### categories.json

```json
{
  "categories": [
    {
      "id": "dev_tools",
      "name": "开发工具",
      "icon": "Code",
      "parent_id": null,
      "order": 0,
      "depth": 0
    }
  ]
}
```

---

## 数据验证

### 输入验证

```mermaid
graph TD
    Input[用户输入] --> Validate{验证}
    Validate -->|路径| PathCheck[路径合法性检查]
    Validate -->|分类| CategoryCheck[分类深度/循环检查]
    Validate -->|模板| TemplateCheck[模板路径存在性]
    
    PathCheck -->|通过| Process[处理]
    PathCheck -->|失败| Error[返回错误]
    
    CategoryCheck -->|通过| Process
    CategoryCheck -->|失败| Error
    
    TemplateCheck -->|通过| Process
    TemplateCheck -->|失败| Error
    
    Process --> Save[保存数据]
    Save --> Emit[发送信号]
    Emit --> UI[更新UI]
```

### 验证规则

1. **路径验证**
   - 不在黑名单中
   - 路径格式正确
   - 路径存在(对于源路径)

2. **分类验证**
   - ID唯一性
   - 父分类存在
   - 深度不超过3层
   - 无循环依赖

3. **模板验证**
   - ID唯一性
   - 路径可展开
   - 路径存在

---

## 数据同步

### 信号驱动更新

```mermaid
graph LR
    Manager[Manager修改数据] --> Save[保存到文件]
    Save --> Emit[发送信号]
    Emit --> View1[视图1]
    Emit --> View2[视图2]
    Emit --> View3[视图3]
    
    View1 --> Refresh1[刷新显示]
    View2 --> Refresh2[刷新显示]
    View3 --> Refresh3[刷新显示]
```

### 全局信号

- `links_updated` - 链接数据变更
- `categories_updated` - 分类数据变更
- `templates_updated` - 模板数据变更
- `theme_changed` - 主题变更
- `theme_color_changed` - 主题色变更

---

## 性能优化

### 1. 缓存策略

- **模板缓存**: API模板缓存到本地,减少网络请求
- **分类树缓存**: 分类树结构缓存,避免重复计算
- **路径展开缓存**: 环境变量展开结果缓存

### 2. 懒加载

- 视图按需创建
- 大列表虚拟滚动
- 图标资源延迟加载

### 3. 批量操作

- 批量导入模板
- 批量更新UI
- 批量保存数据

---

## 错误处理

### 数据加载失败

```mermaid
graph TD
    Load[加载数据] --> Check{文件存在?}
    Check -->|是| Parse{解析成功?}
    Check -->|否| Create[创建默认数据]
    
    Parse -->|是| Validate{验证成功?}
    Parse -->|否| Backup[使用备份]
    
    Validate -->|是| Use[使用数据]
    Validate -->|否| Fix[修复数据]
    
    Backup --> Use
    Fix --> Use
    Create --> Use
```

### 数据保存失败

```mermaid
graph TD
    Save[保存数据] --> Try{尝试保存}
    Try -->|成功| Done[完成]
    Try -->|失败| Retry{重试?}
    
    Retry -->|是| Backup[创建备份]
    Retry -->|否| Error[报告错误]
    
    Backup --> Try
    Error --> Rollback[回滚数据]
```

---

## 相关文档

- [系统架构](../overview/system-architecture.md) - 整体架构
- [核心模块](../overview/core-modules.md) - 模块详解
- [组件架构](../overview/component-architecture.md) - GUI组件

---

**最后更新**: 2026-01-28
