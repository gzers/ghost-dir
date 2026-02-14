

# QFluentWidgets 组件参考

- 适用版本: `>=1.0.0`
- 文档状态: `external`
- 最后更新: `2026-02-10`


基于 PyQt-Fluent-Widgets 的组件使用参考和示例代码。

## 📚 组件分类

### [basic-input/](./basic-input/) - 基础输入组件

常用的基础输入组件:
- PushButton - 按钮
- LineEdit - 单行输入框
- ComboBox - 下拉选择框
- CheckBox - 复选框
- RadioButton - 单选按钮
- Slider - 滑块
- SpinBox - 数字输入框

### [date-time/](./date-time/) - 日期时间组件

日期和时间选择组件:
- DatePicker - 日期选择器
- TimePicker - 时间选择器
- CalendarPicker - 日历选择器

### [dialogs/](./dialogs/) - 对话框组件

对话框和浮出层组件:
- MessageBox - 消息框
- Dialog - 对话框
- Flyout - 浮出层
- TeachingTip - 教学提示

### [navigation/](./navigation/) - 导航组件

导航和菜单组件:
- NavigationInterface - 导航界面
- BreadcrumbBar - 面包屑导航
- TabView - 标签页视图
- Pivot - 透视导航

### [layout/](./layout/) - 布局组件

布局相关组件:
- FlowLayout - 流式布局
- VBoxLayout - 垂直布局
- HBoxLayout - 水平布局

### [status-info/](./status-info/) - 状态信息组件

状态显示和信息提示组件:
- ProgressBar - 进度条
- ProgressRing - 进度环
- InfoBar - 信息栏
- ToolTip - 工具提示
- StateToolTip - 状态提示

### [text/](./text/) - 文本组件

文本显示和编辑组件:
- Label - 标签
- TextEdit - 多行文本编辑
- PlainTextEdit - 纯文本编辑
- BodyLabel - 正文标签
- TitleLabel - 标题标签

### [views/](./views/) - 视图组件

列表和表格视图组件:
- ListView - 列表视图
- TableView - 表格视图
- TreeView - 树形视图
- CardWidget - 卡片组件

### [windows/](./windows/) - 窗口组件

窗口和框架组件:
- FluentWindow - Fluent风格窗口
- MSFluentWindow - 微软Fluent窗口
- SplitFluentWindow - 分割窗口

### [menus/](./menus/) - 菜单组件

菜单相关组件:
- Menu - 菜单
- RoundMenu - 圆角菜单
- SystemTrayMenu - 系统托盘菜单

### [scroll/](./scroll/) - 滚动组件

滚动相关组件:
- ScrollArea - 滚动区域
- SmoothScrollArea - 平滑滚动区域
- SingleDirectionScrollArea - 单向滚动区域

### [material/](./material/) - 材料组件

材料设计相关组件:
- AcrylicLabel - 亚克力标签
- TransparentToolButton - 透明工具按钮

### [media/](./media/) - 媒体组件

媒体播放相关组件:
- VideoWidget - 视频组件
- MediaPlayBarBase - 媒体播放栏

---

## 🚀 快速开始

参考 [快速开始指南](./getting-started.md) 了解如何使用 QFluentWidgets。

## 📖 使用示例

每个组件分类下都有 `examples/` 目录,包含该分类的示例代码:

```
basic-input/
├── README.md           # 组件说明
└── examples/           # 示例代码
    ├── button_demo.py
    ├── lineedit_demo.py
    └── ...
```

## 📝 许可证

QFluentWidgets 使用 GPLv3 许可证,详见 [LICENSE](./LICENSE)。

## 📋 更新日志

查看 [CHANGELOG.md](./CHANGELOG.md) 了解版本更新历史。

---

## 相关文档

- [UI设计规范](../../README.md) - UI设计规范主页
- [排版规范](../../typography/) - 文本层级和样式
- [主题规范](../../themes/) - 主题和配色

---

**最后更新**: 2026-01-28

