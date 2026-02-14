# Ghost-Dir 依赖安装说明

- 适用版本: `>=1.0.0`
- 文档状态: `active`
- 最后更新: `2026-02-10`

## 快速安装

### 使用清华镜像源(推荐,国内用户)
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 使用默认源
```bash
pip install -r requirements.txt
```

## 依赖说明

### 核心依赖

1. **PySide6 (>=6.6.0)**
   - Qt 6 的 Python 绑定
   - 提供跨平台 GUI 框架
   - 官网: https://www.qt.io/qt-for-python

2. **PySide6-Fluent-Widgets[full]**
   - Fluent Design 风格的 UI 组件库
   - **必须使用 `[full]` 版本**以启用 Mica/Acrylic 特效
   - GitHub: https://github.com/zhiyiYo/PyQt-Fluent-Widgets

3. **Pillow (>=10.0.0)**
   - Python 图像处理库
   - 用于图标和图片处理
   - 官网: https://pillow.readthedocs.io/

4. **psutil (>=5.9.0)**
   - 跨平台进程和系统工具库
   - 用于进程卫士功能
   - GitHub: https://github.com/giampaolo/psutil

5. **pywin32 (>=306)**
   - Windows API 的 Python 接口
   - 用于连接点创建和系统交互
   - GitHub: https://github.com/mhammond/pywin32

## 验证安装

安装完成后,可以运行以下命令验证:

```bash
python -c "import PySide6; import qfluentwidgets; import PIL; import psutil; import win32api; print('所有依赖安装成功!')"
```

## 常见问题

### Q: 安装 PySide6-Fluent-Widgets 失败
**A**: 确保使用 `[full]` 版本:
```bash
pip install "PySide6-Fluent-Widgets[full]"
```

### Q: pywin32 安装后无法使用
**A**: 需要运行后安装脚本:
```bash
python Scripts/pywin32_postinstall.py -install
```

### Q: 国内下载速度慢
**A**: 使用清华镜像源:
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 开发环境建议

建议使用虚拟环境:

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境 (Windows)
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
