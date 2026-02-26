# Ghost-Dir 发布指南

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

本文档描述 Ghost-Dir 项目的版本发布流程和规范。

---

## 📋 发布检查清单

### 发布前准备

- [ ] 所有计划功能已完成并测试
- [ ] 所有已知 Bug 已修复或记录
- [ ] 代码已通过所有测试
- [ ] 文档已更新（README、用户文档、API 文档）
- [ ] 依赖版本已确认并更新

### 版本信息更新

- [ ] 更新 `src/__init__.py` 中的 `__version__`
- [ ] 更新 `src/common/config.py` 中的 `APP_VERSION`
- [ ] 更新 `README.md` 中的版本徽章和版本历史
- [ ] 创建或更新 `CHANGELOG.md`
- [ ] 创建 `docs/release/notes/vX.Y.Z.md`（针对当前版本）
- [ ] 在 `docs/release/release-templates.md` 顶部插入新版本发布文案模板

### 发布资源准备

- [ ] 准备发布文案（GitHub Release）
- [ ] 准备截图和演示视频（如有）
- [ ] 准备安装包和压缩文件

### Git 操作

- [ ] 提交所有更改
- [ ] 创建版本标签
- [ ] 推送到远程仓库
- [ ] 创建 GitHub Release

### 发布后

- [ ] 验证下载链接可用
- [ ] 更新项目主页（如有）
- [ ] 发布公告（社交媒体、论坛等）
- [ ] 监控用户反馈和问题报告

---

## 🔢 版本号规范

Ghost-Dir 遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)。

### 版本号格式

```
主版本号.次版本号.修订号
例如：1.2.3
```

### 版本号递增规则

1. **主版本号（Major）**：不兼容的 API 修改
   - 重大架构变更
   - 破坏性更新
   - 不向下兼容的功能修改

2. **次版本号（Minor）**：向下兼容的功能性新增
   - 新增功能
   - 功能增强
   - 向下兼容的 API 变更

3. **修订号（Patch）**：向下兼容的问题修正
   - Bug 修复
   - 性能优化
   - 文档更新

### 版本号示例

- `1.0.0` → `1.0.1`：修复 Bug
- `1.0.1` → `1.1.0`：新增功能
- `1.1.0` → `2.0.0`：重大更新

---

## 📝 CHANGELOG 编写规范

### 文件结构

```markdown
# 更新日志

## [版本号] - 发布日期

### 新增 (Added)
- 新功能描述

### 变更 (Changed)
- 现有功能的变更

### 弃用 (Deprecated)
- 即将移除的功能

### 移除 (Removed)
- 已移除的功能

### 修复 (Fixed)
- Bug 修复

### 安全 (Security)
- 安全相关的修复
```

### 编写原则

1. **面向用户**：使用用户能理解的语言
2. **具体明确**：描述具体变更，避免模糊表述
3. **分类清晰**：按类型分组（新增、修复、变更等）
4. **时间倒序**：最新版本在最上方
5. **链接引用**：提供相关 Issue 或 PR 链接

### 示例

```markdown
## [1.1.0] - 2026-03-01

### 新增
- 添加空间分析功能，显示迁移后节省的磁盘空间 (#123)
- 支持符号链接（Symbolic Link），实现跨物理驱动器迁移 (#145)

### 修复
- 修复批量操作时进度显示不准确的问题 (#156)
- 修复特殊字符路径导致连接失败的问题 (#167)

### 变更
- 优化扫描性能，扫描速度提升 50% (#178)
```

---

## 📄 RELEASE_NOTES 编写规范

### 文件结构

```markdown
# 项目名称 版本号 发布说明

## 版本信息
- 版本号
- 发布日期
- 代号（可选）
- 状态

## 项目简介
- 核心价值
- 典型应用场景

## 核心亮点
- 主要新增功能
- 重大改进

## 主要功能
- 功能列表

## 技术特性
- 架构设计
- 核心组件

## 安装与使用
- 系统要求
- 快速开始

## 已知问题与限制
- 系统限制
- 功能限制
- 计划改进

## 文档资源
- 用户文档
- 开发文档

## 升级指南（如适用）
- 升级步骤
- 注意事项

## 贡献与反馈
- 报告问题
- 功能建议
- 参与贡献

## 致谢
- 开源项目
- 社区贡献
```

### 编写原则

1. **全面详细**：涵盖所有重要信息
2. **突出亮点**：强调核心功能和改进
3. **易于理解**：使用清晰的语言和结构
4. **视觉友好**：使用标题、列表、表格、图标等
5. **可操作性**：提供明确的安装和使用指南

---

## 🏗️ 构建可执行文件

### 使用 PyInstaller

```bash
# 安装 PyInstaller
pip install pyinstaller

# 使用 spec 文件构建
pyinstaller Ghost-Dir.spec

# 输出目录
dist/Ghost-Dir/
```

### 构建配置（Ghost-Dir.spec）

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('config', 'config')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Ghost-Dir',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\icon.ico'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Ghost-Dir',
)
```

### 打包发布

```bash
# 压缩构建产物
cd dist
Compress-Archive -Path Ghost-Dir -DestinationPath Ghost-Dir-1.0.0-win64.zip

# 验证压缩包
# 解压到临时目录并测试运行
```

---

## 🏷️ Git 标签和发布

### 创建版本标签

```bash
# 创建带注释的标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签到远程
git push origin v1.0.0

# 推送所有标签
git push origin --tags
```

### GitHub Release

1. **前往 Releases 页面**：
   - https://github.com/gzers/ghost-dir/releases/new

2. **选择标签**：
   - 选择刚创建的标签（如 `v1.0.0`）

3. **填写发布信息**：
   - **标题**：Ghost-Dir 1.0.0 - Genesis
   - **描述**：使用准备好的发布文案（见下文）

4. **上传文件**：
- `Ghost-Dir-1.0.0-win64.zip`
- `CHANGELOG.md`（可选）
- `notes/v1.0.0.md`（可选）

5. **发布选项**：
   - ✅ Set as the latest release
   - ⬜ Set as a pre-release（仅用于测试版）

6. **发布**：
   - 点击 "Publish release"

---

## 📢 发布文案模板

### GitHub Release 文案

```markdown
# 🎉 Ghost-Dir 1.0.0 - Genesis

**首个正式版本发布！**

Ghost-Dir 是一款专为 Windows 设计的跨磁盘目录迁移与连接管理工具。

## ✨ 核心亮点

- **智能向导**：自动扫描本机可管理软件，一键批量导入
- **模版库**：内置 50+ 官方模版，覆盖常见软件
- **安全保障**：事务管理、崩溃恢复、进程卫士
- **现代 UI**：Fluent Design，Windows 11/10 原生特效

## 📦 下载

- **Windows 64-bit**：`Ghost-Dir-1.0.0-win64.zip`（发布页附件）

## 📚 文档

- [完整发布说明](notes/v1.0.0.md)
- [更新日志](CHANGELOG.md)
- [用户文档](../user-docs/README.md)

## 🚀 快速开始

1. 下载并解压 `Ghost-Dir-1.0.0-win64.zip`
2. 运行 `Ghost-Dir.exe`
3. 在 UAC 提示时点击"是"授予管理员权限
4. 开始使用！

## ⚠️ 系统要求

- Windows 10/11
- 管理员权限
- NTFS 文件系统

## 🐛 问题反馈

如遇到问题，请提交 [Issue](https://github.com/gzers/ghost-dir/issues)。

---

**完整更新内容请查看 [CHANGELOG.md](CHANGELOG.md)**
```

### 社交媒体文案

```
🎉 Ghost-Dir 1.0.0 正式发布！

一款专为 Windows 设计的跨磁盘目录迁移工具：
✅ 智能扫描本机软件
✅ 一键迁移释放 C 盘空间
✅ 零数据丢失保障
✅ Fluent Design 现代界面

立即下载：https://github.com/gzers/ghost-dir/releases

#GhostDir #Windows #开源工具
```

---

## 🔄 发布后维护

### 监控反馈

- 定期检查 GitHub Issues
- 关注用户反馈和问题报告
- 收集功能建议

### 快速修复

如发现严重 Bug：

1. 立即修复并测试
2. 发布修订版本（如 1.0.1）
3. 更新 CHANGELOG
4. 创建新的 Release

### 版本规划

- 根据用户反馈规划下一版本
- 更新项目路线图
- 在 GitHub Projects 中跟踪进度

---

## 📅 发布周期建议

- **主版本**：6-12 个月
- **次版本**：1-3 个月
- **修订版**：按需发布（Bug 修复）

---

## 🔗 相关资源

- [语义化版本规范](https://semver.org/lang/zh-CN/)
- [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
- [GitHub Release 文档](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [PyInstaller 文档](https://pyinstaller.org/)

---

**最后更新**：2026-02-04
