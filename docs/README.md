# Ghost-Dir 项目文档索引

## 📁 文档结构

```
docs/
├── planning/           # 规划文档
│   └── v7.4-implementation-plan.md
├── progress/           # 进度文档
│   ├── v7.4-task-checklist.md
│   ├── development-walkthrough.md
│   ├── refactoring-summary.md  # 包含 View/Widgets 分层规范 ⭐
│   └── CURRENT_STATUS.md
```

---

## 📋 规划文档 (Planning)

### [v7.4 实现计划](planning/v7.4-implementation-plan.md)
**用途**: v7.4 版本的完整实现计划

**内容**:
- PRD v7.4 vs 当前版本对比
- 详细实施计划（Phase 1-5）
- 新增文件清单
- 工作量评估
- 兼容性注意事项
- 验收标准

**适用场景**: 
- 开始新的开发阶段
- 了解整体架构变更
- 评估工作量

---

## 📊 进度文档 (Progress)

### [v7.4 任务清单](progress/v7.4-task-checklist.md)
**用途**: 实时跟踪开发进度

**内容**:
- Phase 1: 数据层升级 ✅
- Phase 2: 新增视图 ⏳
- Phase 3: 导航结构重构 ✅
- Phase 4: 功能增强 ⏳
- Phase 5: 测试与验证 ⏳
- Phase 6: 文档更新 ⏳

**适用场景**:
- 查看当前完成度
- 确定下一步工作
- 跨设备继续开发

### [开发总结](progress/development-walkthrough.md)
**用途**: 已完成功能的详细总结

**内容**:
- 最新进展
- 新增功能详解
- 完整功能清单
- 使用指南
- 文件清单

**适用场景**:
- 了解已实现功能
- 查看使用方法
- 功能验收

### [重构总结](progress/refactoring-summary.md)
**用途**: Views 模块化重构记录

**内容**:
- 重构前后对比
- 新的目录结构
- 设计模式应用
- 最佳实践建议

**适用场景**:
- 了解代码结构
- 学习模块化设计
- 代码审查

---

## 🧪 测试文档 (Testing)

### [Phase 1 测试报告](testing/phase1-test-report.md)
**用途**: 数据层升级的测试验证

**内容**:
- 测试范围
- 已完成功能测试
- 发现的问题
- 测试总结

**适用场景**:
- 验证数据层功能
- 问题排查
- 质量保证

---

## 🚀 快速开始

### 新设备继续开发

1. **查看进度**
   ```bash
   # 查看任务清单
   cat docs/progress/v7.4-task-checklist.md
   ```

2. **了解计划**
   ```bash
   # 查看实现计划
   cat docs/planning/v7.4-implementation-plan.md
   ```

3. **继续开发**
   - 根据任务清单中的 `[ ]` 未完成项
   - 参考实现计划中的详细说明
   - 更新任务清单标记进度

### 当前状态 (2026-01-21)

**已完成** ✅:
- Phase 1: 数据层升级（100%）
- Phase 3: 导航结构重构（100%）

**进行中** 🔄:
- Phase 2: 新增视图（占位完成，待详细实现）
- Phase 4: 功能增强（待实现）

**下一步**:
1. 实现新增连接对话框的"保存为模版"功能
2. 增强设置页面（默认仓库路径）
3. 优化扫描逻辑（过滤已忽略和已添加）
4. 详细实现智能向导和模版库视图

---

## 📝 文档更新规范

### 更新任务清单
完成任务后，将 `[ ]` 改为 `[x]`：
```markdown
- [x] 已完成的任务
- [ ] 未完成的任务
```

### 添加测试报告
新的测试报告放在 `docs/testing/` 下：
```
docs/testing/
├── phase1-test-report.md
├── phase2-test-report.md  # 新增
└── integration-test.md     # 新增
```

### 更新进度文档
重大进展更新 `development-walkthrough.md`

---

## 🔗 相关链接

- [项目 README](../README.md)
- [PRD 文档](../docs/planning/v7.4-implementation-plan.md)
- [源代码](../src/)

---

**最后更新**: 2026-01-21  
**当前版本**: v7.4 (开发中)  
**完成度**: 约 40%
