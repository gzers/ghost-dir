# 全盘 Junction 扫描特性

- 适用版本: `>=1.0.1`
- 文档状态: `active`
- 最后更新: `2026-02-26`

> **状态**: 已实现  
> **创建日期**: 2026-02-26  
> **负责模块**: 扫描服务 (Scan Service)、USN Journal 驱动 (Drivers)、链接视图 (Links View)

---

## 1. 需求概述

原有扫描功能仅基于预定义模板匹配本地已安装软件路径。本特性扩展 `SmartScanner` 的探测范围，**主动发现磁盘上所有已存在的 Junction/Symlink 目录链接**，将它们纳入管理。

非模板来源的链接没有预设分类，在扫描结果卡片上提供分类下拉选择器，默认"未分类"。

---

## 2. 探测引擎

### 双模式策略

| 模式 | 条件 | 速度 | 覆盖深度 | 实现文件 |
|------|------|------|---------|---------|
| **USN Journal** | 管理员权限 | 2-5 秒/盘 | **无限** | `src/drivers/usn_journal.py` |
| 目录遍历（降级） | 无管理员权限 | 较慢 | 2 级 | `scan_service.py` 内联 |

优先使用 USN Journal（通过 NTFS MFT 枚举），权限不足时自动降级到目录遍历。

### USN Journal 核心流程

1. `CreateFileW` 打开卷句柄（`\\.\C:`）
2. `DeviceIoControl(FSCTL_ENUM_USN_DATA)` 枚举 MFT 全部记录
3. 解析 `USN_RECORD_V2` 结构体，筛选 `REPARSE_POINT + DIRECTORY`
4. 通过 `ParentFileReferenceNumber` 链反向重建完整路径

### 磁盘范围

仅扫描 **本地固定磁盘**（`DRIVE_FIXED`），通过 `GetDriveTypeW` 排除：
- 网络驱动器（`DRIVE_REMOTE`）
- U 盘 / 移动硬盘（`DRIVE_REMOVABLE`）
- 光驱（`DRIVE_CDROM`）

---

## 3. 过滤规则

> [!IMPORTANT]
> 过滤规则的核心原则：**只排除确定是系统/驱动自动创建的链接，绝不误杀用户可能主动创建的链接**。
> 修改过滤规则时务必遵循此原则。

### 第一层：USN Journal 属性过滤（`usn_journal.py`）

在 MFT 枚举阶段，排除同时具有 `HIDDEN (0x0002)` + `SYSTEM (0x0004)` 属性的 Reparse Point 目录。

**原理**：Windows 为向后兼容创建的系统 Junction 都会标记为隐藏+系统文件，用户自建的链接不会同时带这两个标志。

**被排除的典型路径**：

| 路径 | 实际指向 |
|------|---------|
| `C:\Users\All Users` | `C:\ProgramData` |
| `C:\Users\Default User` | `C:\Users\Default` |
| `C:\Users\<user>\Application Data` | `AppData\Roaming` |
| `C:\Users\<user>\Local Settings` | `AppData\Local` |
| `C:\Users\<user>\Cookies` | `AppData\Local\...\INetCookies` |
| `C:\Users\<user>\My Documents` | `Documents` |
| `C:\Documents and Settings` | `C:\Users` |
| `...\INetCache\Content.IE5` | (IE 缓存目录) |

### 第二层：路径特征过滤（`scan_service.py :: _is_system_junction()`）

#### 2a. 顶级系统保护路径

路径第一级目录匹配以下名称时排除：

```
windows, programdata, $recycle.bin, system volume information,
recovery, boot, msocache, config.msi, documents and settings,
perflogs, intel, amd, nvidia
```

#### 2b. 已知驱动/系统内部组件目录名

路径中**任意一级目录**匹配以下名称时排除：

```
nvidia corporation    — NVIDIA 驱动内部组件链接
realtek               — Realtek 驱动内部链接
windowsapps           — Windows Store 应用内部
winsxs                — Windows Side-by-Side 程序集
assembly              — .NET GAC 程序集
windows kits          — Windows SDK
windows sidebar       — Windows 侧边栏组件
```

> [!CAUTION]
> **禁止添加以下路径到排除列表**（用户可能主动迁移）：
> - `appdata` — 用户可能迁移整个 AppData 或其子目录
> - `node_modules` — 开发者可能迁移大型依赖目录
> - `program files` 内的任意深度子目录 — 用户可能迁移具体软件
> - `microsoft` — 太宽泛，会误杀

### 第三层：链接有效性验证（`_junction_to_template()`）

- 路径已在数据库中（已管理的链接）→ 跳过
- `get_real_path()` 无法解析目标 → 跳过（目标不存在或权限不足）
- 解析后路径与原始路径相同 → 跳过（非真实链接）

---

## 4. 涉及文件

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `src/drivers/usn_journal.py` | **NEW** | USN Journal MFT 枚举驱动 |
| `src/services/scan_service.py` | MODIFY | 全盘 Junction 探测 + 过滤规则 |
| `src/gui/views/wizard/widgets/scan_result_card.py` | MODIFY | 非模板链接显示分类选择器 + 路径文本省略 |
| `src/gui/dialogs/scan_wizard/scan_flow_dialog.py` | MODIFY | 传入 category_manager |
| `src/gui/components/category_selector.py` | MODIFY | 下拉面板禁用水平滚动条 |

---

## 5. 设计决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 探测引擎 | USN Journal 优先 + 目录遍历降级 | 速度和深度的最佳平衡 |
| 磁盘范围 | 仅 `DRIVE_FIXED` | 排除网络盘、U 盘等不必要的扫描 |
| 系统链接判定 | `HIDDEN+SYSTEM` 属性 | Windows 系统兼容链接的可靠特征 |
| 过滤保守性 | 宁可多扫不可误杀 | 用户利益优先 |
| 分类默认值 | `None`（未分类） | 用户不选择也不阻塞导入 |
| 路径显示 | `ElideMiddle` + tooltip | 长路径不撑破布局 |

---

## 6. 参考资料

- [Service 层架构设计](../../architecture/overview/service-architecture-design.md)
- [数据流图](../../architecture/data-flow/data-flow-diagram.md)

---

**最后更新**: 2026-02-26
