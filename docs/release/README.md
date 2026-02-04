# 发布文档

Ghost-Dir 项目的版本发布相关文档。

---

## 📁 文档列表

### [CHANGELOG.md](CHANGELOG.md)
**版本更新日志**

记录所有版本的变更历史，遵循 [Keep a Changelog](https://keepachangelog.com/) 规范。

### [guide.md](guide.md)
**发布流程指南**

详细的版本发布流程、检查清单和规范说明。

### [copy.md](copy.md)
**发布文案模板**

各平台发布文案，可直接复制使用。

### 版本发布说明

- [v1.0.0.md](v1.0.0.md) - 1.0.0 版本发布说明

---

## 🚀 快速发布

### 使用自动化脚本

```powershell
# 发布新版本
.\scripts\release.ps1 -Version "1.0.0"
```

脚本会自动完成：
1. 更新版本号（`src/__init__.py`）
2. 更新 README 徽章
3. 检查 CHANGELOG
4. 构建可执行文件
5. 打包发布文件
6. 创建 Git 标签

### 手动发布

参考 [guide.md](guide.md) 中的详细步骤。

---

## 📋 发布检查清单

- [ ] 更新 `CHANGELOG.md`
- [ ] 创建版本发布说明（如 `v1.1.0.md`）
- [ ] 运行发布脚本
- [ ] 推送到远程仓库
- [ ] 创建 GitHub Release
- [ ] 使用 `copy.md` 中的文案宣传

---

**最后更新**：2026-02-04
