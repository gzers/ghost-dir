# 数据迁移功能开发文档

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

> **状态**: 规划中  
> **创建日期**: 2026-02-08  
> **负责模块**: 链接管理 (Link Management)

---

## 1. 需求概述

当用户在添加或编辑链接时遇到路径冲突（目标路径已存在文件/文件夹），系统应提供友好的数据迁移流程：

1. **确认对话框**：告知用户路径冲突，询问是否进行数据迁移
2. **进度对话框**：显示迁移进度（百分比、当前文件、总量等）
3. **结果对话框**：显示迁移成功/失败信息

同样，在取消链接时，如果需要将数据从目标路径迁移回源路径，也应提供相同的流程。

---

## 2. 架构设计

### 2.1 服务层设计

#### MigrationService (新增)

**文件路径**: `src/services/migration_service.py`

**职责**: 负责文件/文件夹的迁移逻辑，包括大小计算、复制/移动、进度回调

**核心方法**:

```python
class MigrationWorker(QObject):
    """迁移工作线程"""
    progress_updated = Signal(int, int, str)  # (current_bytes, total_bytes, current_file)
    migration_finished = Signal(bool, str)     # (success, error_msg)
    
    def migrate(self, source: str, target: str, mode: str):
        """执行迁移操作"""

class MigrationService:
    def calculate_total_size(self, path: str) -> int:
        """计算文件/文件夹总大小（字节）"""
    
    def migrate_data_async(
        self, 
        source: str, 
        target: str, 
        mode: str,  # "copy" 或 "move"
        progress_callback: Callable,
        finished_callback: Callable
    ):
        """异步迁移数据"""
    
    def cancel_migration(self):
        """取消正在进行的迁移"""
```

**实现要点**:
- 使用 `QThread` + `QObject` 模式实现异步迁移（参考 `LinkService._start_worker`）
- 使用 `shutil.copy2` 保留文件元数据
- 使用 `os.scandir` 递归遍历文件夹
- 每复制一个文件后触发进度回调
- 支持取消操作（通过 `is_aborted` 标志）

---

### 2.2 UI 层设计

#### 2.2.1 MigrationConfirmDialog

**文件路径**: `src/gui/dialogs/migration/confirm_dialog.py`

**继承**: `MessageBoxBase`

**UI 元素**:
- 标题: "检测到路径冲突"
- 说明: 描述冲突情况
- 源路径、目标路径显示
- 大小信息: 显示目标路径现有数据大小
- 警告提示区域
- 按钮: "迁移并继续" / "取消"

---

#### 2.2.2 MigrationProgressDialog

**文件路径**: `src/gui/dialogs/migration/progress_dialog.py`

**继承**: `MessageBoxBase`

**UI 元素**:
- 标题: "正在迁移数据"
- 状态描述: "正在复制: xxx.txt"
- 进度条: `ProgressBar` - 显示百分比
- 进度文本: "已完成 50MB / 100MB (50%)"
- 按钮: "取消"

**实现要点**:
- 连接 `MigrationService` 的进度回调信号
- 实时更新进度条和状态文本
- 支持取消操作

---

#### 2.2.3 MigrationResultDialog

**文件路径**: `src/gui/dialogs/migration/result_dialog.py`

**继承**: `MessageBoxBase`

**UI 元素**:
- 成功时: 绿色对勾图标 + "迁移成功" + 统计信息
- 失败时: 红色叉号图标 + "迁移失败" + 错误信息
- 按钮: "确定"

---

## 3. 集成方案

### 3.1 修改 LinkService

在 `validate_and_add_link` 和 `validate_and_update_link` 方法中添加路径冲突检测:

```python
# 检查目标路径是否已存在
if os.path.exists(target_path):
    return False, "TARGET_EXISTS"
```

### 3.2 修改 EditLinkDialog 和 AddLinkDialog

在 `validate` 方法中处理迁移流程:

```python
def validate(self):
    success, msg = self.connection_service.validate_and_update_link(...)
    
    if not success and msg == "TARGET_EXISTS":
        # 显示确认对话框 -> 进度对话框 -> 结果对话框
        # ...
```

---

## 4. 用户交互流程

### 4.1 添加链接时目标路径已存在

```
用户点击保存
  ↓
验证路径
  ↓
目标路径已存在 → 显示 MigrationConfirmDialog
  ↓
用户点击"迁移并继续"
  ↓
显示 MigrationProgressDialog
  ↓
MigrationService 开始迁移（实时更新进度）
  ↓
迁移成功 → 显示 MigrationResultDialog（成功）
  ↓
创建链接并刷新列表
```

### 4.2 取消链接时迁移数据回源路径

```
用户点击取消链接
  ↓
检查是否需要迁移
  ↓
需要迁移 → 显示 MigrationConfirmDialog
  ↓
用户确认 → 显示 MigrationProgressDialog
  ↓
迁移数据回源路径
  ↓
成功 → 删除符号链接 → 显示成功提示
```

---

## 5. 文件结构

```
src/
├── services/
│   ├── migration_service.py          # [NEW] 迁移服务
│   └── link_service.py                # [MODIFY] 集成迁移检测
├── gui/
│   └── dialogs/
│       ├── migration/                 # [NEW] 迁移对话框目录
│       │   ├── __init__.py
│       │   ├── confirm_dialog.py      # [NEW] 确认对话框
│       │   ├── progress_dialog.py     # [NEW] 进度对话框
│       │   └── result_dialog.py       # [NEW] 结果对话框
│       ├── edit_link/
│       │   └── dialog.py              # [MODIFY] 集成迁移流程
│       └── add_link/
│           └── dialog.py              # [MODIFY] 集成迁移流程
```

---

## 6. 验证计划

### 6.1 单元测试

**文件**: `tests/test_migration_service.py`

**测试用例**:
- `test_calculate_total_size()` - 测试计算文件夹总大小
- `test_migrate_single_file()` - 测试迁移单个文件
- `test_migrate_folder()` - 测试迁移文件夹
- `test_migrate_with_progress_callback()` - 测试进度回调
- `test_cancel_migration()` - 测试取消迁移
- `test_rollback_on_failure()` - 测试失败时回滚

### 6.2 手动测试场景

#### 场景 1: 小文件迁移
- 创建测试文件夹（< 10MB）
- 验证确认对话框显示
- 验证进度条更新
- 验证成功对话框

#### 场景 2: 大文件夹迁移
- 创建大文件夹（> 100MB）
- 验证进度条平滑更新
- 验证状态文本实时显示

#### 场景 3: 取消迁移
- 在进度对话框中点击"取消"
- 验证迁移立即停止
- 验证已复制的文件被清理

#### 场景 4: 磁盘空间不足
- 准备大于剩余磁盘空间的文件夹
- 验证失败对话框显示
- 验证错误信息明确

---

## 7. 设计决策

### 7.1 迁移模式
**决策**: 默认使用"复制"模式
**理由**: 更安全，避免数据丢失风险

### 7.2 取消链接时的行为
**决策**: 不自动迁移数据回源路径
**理由**: 避免操作繁琐，用户可手动处理

### 7.3 进度显示粒度
**决策**: 每复制一个文件触发一次回调
**理由**: 提供实时反馈，对于大量小文件可考虑节流

### 7.4 错误处理策略
**决策**: 遇到单个文件失败时立即中止并回滚
**理由**: 保证数据完整性

### 7.5 对话框样式
**决策**: 不显示文件列表预览和详细日志
**理由**: 保持界面简洁，减少信息过载

---

## 8. 参考资料

- [PyQt Threading Best Practices](../pyqt-threading-best-practices.md)
- [Standardization Guide](../standardization-guide.md)
- [LinkService 实现](../../../../src/services/link_service.py)
- [QFluentWidgets 文档](https://qfluentwidgets.com/)

---

**相关文档**:
- [开发规划（Active）](./active/)
- [架构设计文档](../../architecture/README.md)
