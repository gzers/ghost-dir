# 发布文档

Ghost-Dir 项目的版本发布相关文档。

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-17`

---

## 📁 文档结构

```
release/
├── README.md                    # 本文件
├── CHANGELOG.md                 # 完整更新日志
├── release-guide.md             # 发布流程指南
├── release-templates.md         # 发布文案模板
├── archived/                    # 历史发布文档归档
│   ├── guide.md                 # 历史兼容占位（已归档）
│   └── templates.md             # 历史兼容占位（已归档）
└── notes/                       # 版本发布说明
    ├── v1.0.0.md
    └── v1.0.1.md
```

---

## 📚 文档说明

### [CHANGELOG.md](CHANGELOG.md)
**完整的版本更新日志**

记录所有版本的变更历史，遵循 [Keep a Changelog](https://keepachangelog.com/) 规范。

### [release-guide.md](release-guide.md)
**发布流程指南**

详细的版本发布流程、检查清单和规范说明。

### [release-templates.md](release-templates.md)
**发布文案模板**

GitHub Release 发布文案，可直接复制使用。

### 历史兼容文件归档说明

- `guide.md` 已更名为 `release-guide.md`
- `templates.md` 已更名为 `release-templates.md`
- 旧兼容占位文件已迁移至 [archived/](./archived/)

### [notes/](notes/)
**版本发布说明**

每个版本的详细发布说明文档：
- [v1.0.1.md](notes/v1.0.1.md) - 1.0.1 版本发布说明
- [v1.0.0.md](notes/v1.0.0.md) - 1.0.0 版本发布说明

---

## 🚀 快速发布

### 使用自动化脚本

```powershell
# 发布新版本
.\scripts\release.ps1 -Version "1.0.1"
```

脚本会自动完成：
1. 更新版本号（`src/__init__.py`）
2. 更新 README 徽章
3. 检查 CHANGELOG
4. 构建可执行文件
5. 打包发布文件
6. 创建 Git 标签

### 手动发布

参考 [release-guide.md](release-guide.md) 中的详细步骤。

---

## 🤖 AI 辅助发版

在对话中发送一句话即可自动完成全套版本文档更新：

```
发 X.Y.Z，变更：
- fix: 修复了 xxx
- feat: 新增了 yyy
- chg: 优化了 zzz
```

**极简模式**（自动从 git log 提取变更）：

```
发 X.Y.Z
```

AI 会自动更新：

1. `src/__init__.py` 中的 `__version__`
2. `README.md` 中的版本徽章与版本历史
3. `docs/release/CHANGELOG.md` 新增条目
4. `docs/release/notes/vX.Y.Z.md`（新建发布说明）
5. `docs/release/README.md` 目录索引
6. `docs/README.md` 最后更新日期

---

## 📋 发布检查清单

- [ ] 更新 `CHANGELOG.md`
- [ ] 创建版本发布说明（如 `notes/v1.1.0.md`）
- [ ] 运行发布脚本
- [ ] 推送到远程仓库
- [ ] 创建 GitHub Release
- [ ] 使用 `release-templates.md` 中的文案宣传

---

**最后更新**：2026-02-17
