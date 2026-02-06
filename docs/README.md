# Ghost-Dir 文档中心

欢迎来到 Ghost-Dir 项目文档!

## 📚 文档导航

### 架构文档
- [架构概览](architecture/README.md) - 项目架构设计和最佳实践

### 迁移文档
- [GUI 层迁移总结](migration/gui-migration-summary.md) - GUI 层迁移的完整记录

## 🏗️ 项目架构

Ghost-Dir 采用五层金字塔架构:

```
GUI Layer (表现层)
    ↓
Services Layer (业务逻辑层)
    ↓
DAO/Drivers Layer (数据访问/系统驱动层)
    ↓
Models Layer (数据模型层)
    ↓
Common Layer (全局基础层)
```

详细信息请查看 [架构文档](architecture/README.md)。

## 📖 快速开始

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行应用**
   ```bash
   python run.py
   ```

3. **查看架构**
   - 阅读 [ARCHITECTURE.md](../ARCHITECTURE.md)
   - 查看 [架构文档](architecture/README.md)

## 🔧 开发指南

### 添加新功能

1. **定义数据模型** (models/)
2. **实现数据访问** (dao/)
3. **编写业务逻辑** (services/)
4. **创建用户界面** (gui/)

### 代码规范

- 遵循五层架构原则
- 单向依赖 (上层依赖下层)
- 使用类型注解
- 添加文档字符串

## 📝 更新日志

### 2026-02-07
- ✅ 完成 GUI 层迁移 (30个文件)
- ✅ 重建核心模块 (14个文件)
- ✅ 删除旧代码目录 (core, data, utils)
- ✅ 创建文档中心

## 🤝 贡献指南

欢迎贡献!请遵循以下步骤:

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](../LICENSE) 文件。
