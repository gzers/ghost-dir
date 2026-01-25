# Role: QFluentWidgets Expert Developer

You are an expert in Python GUI development using PySide6 and QFluentWidgets.
Use the following official documentation context to refactor user code.
Strictly prefer `qfluentwidgets` components over native Qt widgets.
Always use `FluentIcon` enum for icons instead of file paths.
==================================================



============================================================
# Guide > About
============================================================
---
title: 简介
date: 2023-08-17 15:02:30
permalink: /zh/pages/about/
---

[**QFluentWidgets**](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) 是一个基于 C++ Qt/PyQt/PySide 的 Fluent Design 风格组件库，包含数以百计的流畅设计组件，为简化开发、提高效率而生。




## 特性
* **美观优雅**：内置 160+ 开源非商用 Fluent Design 组件，开箱即用，快速打造卓越应用
* **矢量图标**：内置 175 个 Fluent Design 矢量图标，随心缩放，依旧清晰
* **高度可定制**：支持无缝切换亮暗主题和主题色，满足用户的个性化需求
* **所见即所得**：搭载设计师插件，直接在 QtDesigner 中预览和使用组件
* **自由缩放**：支持自定义界面缩放，适配不同分辨率的屏幕
* **简单易学**：保留原生组件的 API，只需替换类名即可完成美化
* **国际化**：支持多国语言，满足不同用户群体的需求
* **跨平台**：支持 Windows、Linux 和 MacOS

## 许可证

Python 组件库非商用的许可证为 [GPLv3](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/LICENSE)，如果你的非商用项目使用了组件库，**必须使用 GPLv3 许可证进行软件分发**。

Python 组件库商用需购买 [商业许可证](/zh/pages/pro) 以获得商用授权。

C++ 组件库没有开源，可从官网顶部导航栏下载体验编译好的示例程序，如需购买使用请先了解 [价格方案](/zh/price) 并联系 [shokokawaii@foxmail.com](mailto:shokokawaii@foxmail.com) 或 QQ：1953658489。

组件库受软件著作权保护，软著登字第12532763号，任何盗用组件库，破解组件库，未经授权而商业使用均视为侵权。

::: info GPLv3
GPLv3 许可证具有 Copyleft 特性，如果非商用项目使用 Python 组件库进行开发，必须将整个软件以 GPLv3 许可证发布。用户拿到你的程序的时候必须可以获得源代码，同时用户可以将代码免费送给其它人。
:::

## 致谢
感谢所有为这个组件库的发展做出贡献以及支持过自己的小伙伴们：

<a href="https://github.com/zhiyiYo/PyQt-Fluent-Widgets/graphs/contributors"></a>




============================================================
# Guide > Install
============================================================
---
title: 安装
date: 2023-08-17 15:37:01
permalink: /zh/pages/install/
---

执行下述安装指令之前建议搭建一个新的虚拟环境，Python 版本最低 3.7：

:::: code-group
::: code-group-item PyQt5
```shell
# 安装轻量版
pip install PyQt-Fluent-Widgets -i https://pypi.org/simple/

# 安装完整版 (支持亚克力组件)
pip install "PyQt-Fluent-Widgets[full]" -i https://pypi.org/simple/
```
:::
::: code-group-item PyQt6
```shell
# 安装轻量版
pip install PyQt6-Fluent-Widgets -i https://pypi.org/simple/

# 安装完整版
pip install "PyQt6-Fluent-Widgets[full]" -i https://pypi.org/simple/
```
:::
::: code-group-item PySide2
```shell
# 安装轻量版
pip install PySide2-Fluent-Widgets -i https://pypi.org/simple/

# 安装完整版
pip install "PySide2-Fluent-Widgets[full]" -i https://pypi.org/simple/
```
:::
::: code-group-item PySide6
```shell
# 安装轻量版
pip install PySide6-Fluent-Widgets -i https://pypi.org/simple/

# 安装完整版
pip install "PySide6-Fluent-Widgets[full]" -i https://pypi.org/simple/
```
:::
::::

[高级版](/zh/pages/pro)组件库包含更多组件，可在发行页面下载 `PyQt-Fluent-Widgets-Pro-Gallery.zip` 进行预览，购买链接见[价格页面](/zh/price/)。

::: warning 警告
请勿同时安装 PyQt-Fluent-Widgets、PyQt6-Fluent-Widgets、PySide2-Fluent-Widgets 和 PySide6-Fluent-Widgets，因为他们的包名都是 `qfluentwidgets`.

如果混用 PyQt 和 PySide，会导致程序直接闪退，遇到此问题请自行检查安装的组件库是否对应所使用的 PyQt/PySide。
:::

## 运行示例
使用 pip 安装好 QFluentWidgets 包并下载好项目仓库**对应分支**的代码之后，就可以运行 examples 目录下的任意示例程序，比如：
```shell
cd examples/gallery
python demo.py
```

如果遇到 `ImportError: cannot import name 'XXX' from 'qfluentwidgets'`，这表明安装的包版本过低，可以按照上面的安装指令将 pypi 源替换为 https://pypi.org/simple 并重新安装最新版本的包。

## 如何入门

1. 掌握 Qt 的信号槽机制、事件机制、按钮和输入框等常用组件的使用
2. 安装组件库并下载 [GitHub 仓库](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) 源代码
3. 阅读并运行 examples 文件夹中的实例
4. 阅读官网文档

::: tip 提示
除了 `InfoBar`、`Pivot` 和 `FluentWindow` 等自定义组件需要阅读文档外，按钮、输入框和标签这种组件仅仅是修改了样式表或重写了 `paintEvent`，API 与 Qt 内置组件保持一致，只要修改类名为 QFluentWidgets 的组件名即可，没有任何额外的学习成本。
:::



============================================================
# Guide > Theme
============================================================
---
title: 主题
date: 2023-08-17 17:31:30
permalink: /zh/pages/theme/
---

## 切换主题


`setTheme()` 函数用于切换 qfluentwidgets 全部组件的亮暗主题。该函数接受下述值：

- `Theme.LIGHT`：浅色主题
- `Theme.DARK`：深色主题
- `Theme.AUTO`：跟随系统主题。如果无法检测到系统的主题，将使用浅色主题。

当主题发生改变时，`qconfig` 会发出 `themeChanged` 信号，组件库提供了 `toggleTheme()` 快速切换亮暗主题。

## 样式表

如果想在主题发生改变时，自动切换界面的样式，可以继承 `StyleSheetBase` 类并重写 `path()` 方法。下述代码实现了一个能够自动切换背景颜色的 `Window` 类，它的 qss 文件路径为 `qss/light/window.qss` 和 `qss/dark/window.qss`：

```python
from enum import Enum
from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    WINDOW = "window"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f"qss/{theme.value.lower()}/{self.value}.qss"


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.label = QLabel("Label", self)

        # 使用流畅样式表
        StyleSheet.WINDOW.apply(self)
```

样式表文件：

* 浅色模式 `qss/light/window.qss`

    ```css
    Window {
        background-color: rgb(249, 249, 249);
    }

    Window>QLabel {
        color: --ThemeColorPrimary;   /* 使用组件库的主题色 */
        font: 14px --FontFamilies;    /* 使用组件库的字体 */
    }
    ```

* 深色模式 `qss/dark/window.qss`

    ```css
    Window {
        background-color: rgb(32, 32, 32);
    }

    Window>QLabel {
        color: --ThemeColorPrimary;
        font: 14px --FontFamilies;
    }
    ```

样式表支持下述几种占位符：

* `--ThemeColorPrimary`
* `--ThemeColorLight1`
* `--ThemeColorLight2`
* `--ThemeColorLight3`
* `--ThemeColorDark1`
* `--ThemeColorDark2`
* `--ThemeColorDark3`
* `--FontFamilies`


### 跟随系统主题

qfluentwidgets 提供了系统主题监听器线程 `SystemThemeListener`，可用于跟随系统主题。

下面是一个简单的使用示例：

```python
from qfluentwidgets import FluentWindow, SystemThemeListener, isDarkTheme


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()

        # 创建主题监听器
        self.themeListener = SystemThemeListener(self)

        # 创建并添加子界面
        # ...

        # 启动监听器
        self.themeListener.start()

    def closeEvent(self, e):
        # 停止监听器线程
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)

    def _onThemeChangedFinished(self):
        super()._onThemeChangedFinished()

        # 云母特效启用时需要增加重试机制
        if self.isMicaEffectEnabled():
            QTimer.singleShot(100, lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()))

```

## 自定义样式
如果你对内置组件的样式感到不满，希望对其进行微调，可以使用 `setCustomStyleSheet()` 在原有样式的基础上添加新样式，该函数的签名如下：
```python
def setCustomStyleSheet(widget: QWidget, lightQss: str, darkQss: str) -> None
```


其中 `widget` 是需要调整样式的组件，`lightQss` 和 `darkQss` 是浅/深色主题下 **添加** 的自定义样式。

举个例子，将 `PushButton` 的圆角调成 10px：


```python
button = PushButton('Button', self)

# 添加自定义样式表
qss = 'PushButton{border-radius: 10px}'
setCustomStyleSheet(button, qss, qss)
```


在 QtDesigner 中，你可以通过新增动态属性来达到自定义样式的目的，操作步骤如下：

1. 添加字符串类型的动态属性

   

2. 在创建动态属性对话框中将属性名设置为 `lightCustomQss`，深色模式就设置为 `darkCustomQss`

   

3. 点击属性旁边的 `...` 按钮，在编辑文本对话框中编辑 `lightCustomQss`

   


## 主题色

`themeColor()` 返回主题色，`setThemeColor()` 用于修改全部组件的主题色。该函数接受三种类型的值：

- `QColor`
- `Qt.GlobalColor`
- `str`：十六进制颜色字符串或者颜色名字，比如 `#0065d5` 或者 `red`

当主题色发生改变时，`qconfig` 管理的配置实例会发出 `themeColorChanged` 信号。

### 系统主题色
`qframelesswindow` v0.4.3 及以上版本提供了获取 Windows 和 macOS 系统主题色的接口，可搭配 `setThemeColor()` 使用：
```python
import sys
from qframelesswindow.utils import getSystemAccentColor

# 只能获取 Windows 和 macOS 的主题色
if sys.platform in ["win32", "darwin"]:
   setThemeColor(getSystemAccentColor(), save=False)
```

## 字体

qfluentwidgets v1.9.0 及以上版本支持调用 `setFontFamilies()` 来自定义组件库所使用的字体。

`fontFamilies()` 返回当前字体，默认的字体家族为 `['Segoe UI', 'Microsoft YaHei', 'PingFang SC']`。



============================================================
# Guide > Icon
============================================================
---
title: 图标
date: 2023-08-17 17:35:27
permalink: /zh/pages/icon/
---

## 内置图标
QFluentWidgets 中的组件一般支持以下三种图标参数类型：
* `str`: 图标路径
* `QIcon`：Qt 图标
* `FluentIconBase`: 流畅图标抽象类

QFluentWidgets 提供的 `FluentIcon` 继承自 `FluentIconBase`, 包含数百个矢量图标，可以在 [gallery](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases/download/v1.1.6/PyQt-Fluent-Widgets-Gallery_v1.1.6_lite_windows_x64.zip) 示例的图标界面查看和搜索图标。



## 适配 Qt 原生组件
对于不支持 `FluentIconBase` 的类，比如只支持 `QIcon` 的 `QListWidgetItem`，可以调用 `FluentIconBase.qicon()` 返回一个能够自动切换主题的 `QIcon`。


## 自定义图标
### 更改颜色
流畅图标基类提供了 `FluentIconBase.icon()` 方法:

```python
def icon(self, theme=Theme.AUTO, color: QColor = None) -> QIcon:
```


可以根据传入的主题或者颜色返回一个 `QIcon` 图标，只有在图标类型为 svg 图标时，`color` 参数才会起作用。下面给出一个示例：


```python
# 使用浅色主题图标
button = ToolButton(FluentIcon.ADD.icon(Theme.LIGHT))

# 使用深色主题图标
button = ToolButton(FluentIcon.ADD.icon(Theme.DARK))

# 使用颜色名称
button = ToolButton(FluentIcon.ADD.icon(color='red'))

# 使用十六进制字符串
button = ToolButton(FluentIcon.ADD.icon(color='#ff0000'))

# 使用 Qt.GlobalColor
button = ToolButton(FluentIcon.ADD.icon(color=Qt.red))

# 使用 QColor
button = ToolButton(FluentIcon.ADD.icon(color=QColor(255, 0, 0)))
```

流畅图标基类提供了 `FluentIconBase.colored()` 方法来自定义深色和浅色模式下的图标颜色：

```python
def colored(self, lightColor: QColor, darkColor: QColor) -> ColoredFluentIcon:
```

下述代码返回了一个浅色模式下为红色，深色模式下为蓝色的图标：

```python
icon = FluentIcon.ADD.colored(QColor(255, 0, 0), QColor(0, 0, 255))
button.setIcon(icon)
```



### 添加图标

#### SVG 图标
如果想在切换主题时自动更换图标，可以继承 `FluentIconBase` 类并重写 `path()` 函数来给出不同主题下图标的路径。下面是一个示例：


```python
from enum import Enum

from qfluentwidgets import getIconColor, Theme, FluentIconBase


class MyFluentIcon(FluentIconBase, Enum):
    """ Custom icons """

    ADD = "Add"
    CUT = "Cut"
    COPY = "Copy"

    def path(self, theme=Theme.AUTO):
        # getIconColor() 根据主题返回字符串 "white" 或者 "black"
        return f':/icons/{self.value}_{getIconColor(theme)}.svg'
```


之后就可以将 `MyFluentIcon` 实例作为参数传给需要图标的组件，比如：

```python
from qfluentwidgets import ToolButton, toggleTheme

# 创建工具按钮
button = ToolButton(MyFluentIcon.ADD)

# 更换图标
button.setIcon(MyFluentIcon.CUT)

# 切换主题，图标也会跟着改变
button.clicked.connect(toggleTheme)
```

#### 图标字体

组件库支持使用图标字体，可以继承 `FluentFontIconBase` 类并重写 `path()` 函数来给出图标字体的路径。下面是一个示例：

```python
class PhotoFontIcon(FluentFontIconBase):
    """ Custom icon font icon """

    def path(self, theme=Theme.AUTO):
        return "/path/to/font.ttf"

    def iconNameMapPath(self):
        """ 如果想使用 `fromName` 来创建图标，需要重写此方法 """
        return "/path/to/fontNameMap.json"
```

`iconNameMapPath()` 给出了图标名称到图标码点的映射表文件路径，如果不想通过 `FluentFontIconBase.fromName()` 来创建图标，则无需重写此函数。映射表文件的格式如下：

```json
{
    "cloud": "\ue753",
    "filter": "\ue71c",
    "smile": "\ue76e"
}
```

下面是图标字体的使用示例：

```python
# 使用码点创建图标
button = ToolButton(PhotoFontIcon("\ue77b"))

# 使用名称来创建图标
button = ToolButton(PhotoFontIcon.fromName("smile"))

# 自定义图标颜色
button = ToolButton(PhotoFontIcon.fromName("cloud").colored("#275EFF", Qt.GlobalColor.darkCyan))
```


### 视频教程




============================================================
# Guide > Setting
============================================================
---
title: 设置
date: 2023-08-17 19:15:59
permalink: /zh/pages/setting/
---

QFluentWidgets 将每个配置项表示为界面的一个设置卡。用户在设置卡上的交互行为将会改变相应配置项的值，同时 QFluentWidgets 会自动更新配置文件。

## 配置项

 `ConfigItem` 类表示一个配置项， `QConfig` 类用于读写 `ConfigItem` 项的值。当 `ConfigItem` 的值发生改变时，`QConfig` 类会自动将配置项的值同步到配置文件中。

由于配置文件可能被用户手动篡改，导致配置项的值非法，所以 QFluentWidgets 使用 `ConfigValidator` 类及其子类来验证和修正配置项的值。

QFluentWidgets 使用 json 文件来保存配置，而 json 文件只支持字符串、布尔值、列表和字典，对于枚举类或者 `QColor`，无法直接将它们的值写入 json 文件中。为了解决这个问题，QFluentWidgets 提供了 `ConfigSerializer` 类及其子类来序列化和反序列化配置项。举个栗子，可以使用 `ColorSerializer` 来序列化值类型为 `QColor` 的配置项。

`ConfigItem` 的属性如下表所示：

| 属性         | 数据类型           | 描述                                         |
| ------------ | ------------------ | -------------------------------------------- |
| `group`      | `str`              | 配置项所属的组别                             |
| `name`       | `str`              | 配置项的名字                                 |
| `default`    | `Any`              | 配置项的默认值，当配置值非法时将被默认值替代 |
| `validator`  | `ConfigValidator`  | 配置校验器                                   |
| `serializer` | `ConfigSerializer` | 配置序列化器                                 |
| `restart`    | `bool`             | 配置更新后是否重启应用                       |

为了正确读写配置项的值，应该将 `ConfigItem` 的实例添加到 `QConfig` 子类的类属性中，然后使用 `qconfig.load()` 来加载配置文件。下面是一个简单的例子：

```python
class MvQuality(Enum):
    """ MV quality enumeration class """

    FULL_HD = "Full HD"
    HD = "HD"
    SD = "SD"
    LD = "LD"

    @staticmethod
    def values():
        return [q.value for q in MvQuality]


class Config(QConfig):
    """ Config of application """

    # main window
    enableAcrylic = ConfigItem("MainWindow", "EnableAcrylic", False, BoolValidator())
    playBarColor = ColorConfigItem("MainWindow", "PlayBarColor", "#225C7F")
    themeMode = OptionsConfigItem("MainWindow", "ThemeMode", "Light", OptionsValidator(["Light", "Dark", "Auto"]), restart=True)
    recentPlaysNumber = RangeConfigItem("MainWindow", "RecentPlayNumbers", 300, RangeValidator(10, 300))

    # online
    onlineMvQuality = OptionsConfigItem("Online", "MvQuality", MvQuality.FULL_HD, OptionsValidator(MvQuality), EnumSerializer(MvQuality))


# 创建配置实例并使用配置文件来初始化它
cfg = Config()
qconfig.load('config/config.json', cfg)
```

## 设置卡

PyQt-Fluent-Widgets 内置了许多类型的设置卡：

|          Class           | 描述               |
| :----------------------: | ------------------ |
|     `HyperlinkCard`      | 超链接设置卡       |
|    `ColorSettingCard`    | 拾色器设置卡       |
| `CustomColorSettingCard` | 颜色选择按钮设置卡 |
|  `ComboBoxSettingCard`   | 下拉框设置卡       |
|    `RangeSettingCard`    | 滑动条设置卡       |
|    `PushSettingCard`     | 按钮设置卡         |
| `PrimaryPushSettingCard` | 主题色按钮设置卡   |
|   `SwitchSettingCard`    | 开关按钮设置卡     |
|   `OptionsSettingCard`   | 单选按钮设置卡     |
| `FolderListSettingCard`  | 文件夹列表设置卡   |

可以通过 `SettingCardGroup.addSettingCard()` 将多个设置卡添加到同一个组中，`SettingCardGroup` 会根据设置卡的高度自动调整自己的布局。

对于上述组件的具体使用方式，参见 [setting_interface.py](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/window/settings/setting_interface.py).







============================================================
# Components > Window > Fluent Window
============================================================
---
title: 流畅窗口
date: 2024-03-14 13:52:00
permalink: /zh/pages/components/fluentwindow/
---

## [FluentWindow](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/window/fluent_window/index.html#)



`FluentWindow` 对侧边导航栏和层叠组件进行了封装，使用这个类可以十分方便地创建多界面窗口。

### 添加子界面
只需调用 `addSubInterface()` 方法就能完成子界面的添加：

```python
def addSubInterface(
    self,
    interface: QWidget,
    icon: FluentIconBase | QIcon | str,
    text: str,
    position=NavigationItemPosition.TOP,
    parent: QWidget = None
) -> NavigationTreeWidget
```

各个参数解释如下：
* `interface`: 需要添加的子界面
* `icon`：侧边栏菜单项图标
* `text`：侧边栏菜单项文本
* `position`：侧边栏菜单项的位置
* `parent`：侧边栏父菜单项对应的子界面

::: warning 警告
调用 `addSubInterface()` 之前必须给子界面设置全局唯一的对象名作为路由键，否则后退功能会出问题，同时侧边栏看不到子界面对应的菜单项。
如果你在界面的左上角看到奇怪的东西，说明忘了调用 `addSubInterface()` 添加某个子界面
:::

下面是个简单的例子，更加复杂的多子界面示例见 [视频教程](/zh/pages/designer/#复杂示例)：

```python
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))


class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()

        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = Widget('Home Interface', self)
        self.musicInterface = Widget('Music Interface', self)
        self.videoInterface = Widget('Video Interface', self)
        self.settingInterface = Widget('Setting Interface', self)
        self.albumInterface = Widget('Album Interface', self)
        self.albumInterface1 = Widget('Album Interface 1', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')
        self.addSubInterface(self.musicInterface, FIF.MUSIC, 'Music library')
        self.addSubInterface(self.videoInterface, FIF.VIDEO, 'Video library')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.albumInterface, FIF.ALBUM, 'Albums', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.albumInterface1, FIF.ALBUM, 'Album 1', parent=self.albumInterface)

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
```


### 切换界面

`FluentWindow` 提供了切换当前界面的方法，`interface` 为待切换的子界面：
```python
def switchTo(self, interface: QWidget) -> None
```

`FluentWindow` 内部使用 `StackedWidget` 来存放子界面，切换当前界面时 `StackedWidget` 会发出 `currentChanged(index: int)` 信号：

```python
self.stackedWidget.currentChanged.connect(lambda: print(self.stackedWidget.currentWidget()))
```


### 定制化侧边栏
调整展开状态下侧边导航的宽度：
```python
self.navigationInterface.setExpandWidth(300)
```

默认情况下侧边导航为收缩状态，当窗口宽度超过阈值时才会展开，如果希望禁用收缩并一直保持展开状态：
```python
# 这行代码必须在 setExpandWidth() 后面调用
self.navigationInterface.setCollapsible(False)
```

如果不想禁用收缩，但是希望窗口创建之后侧边栏是展开的：
```python
self.resize(900, 700)

# 需要设置允许侧边导航展开的最小窗口宽度
self.navigationInterface.setMinimumExpandWidth(900)

# 展开导航栏
self.navigationInterface.expand(useAni=False)
```

### 定制化标题栏

`FluentWindow` 使用的是 `qframelesswindow` 库提供的自定义标题栏，对应 `titleBar` 属性。标题栏使用水平布局 `hBoxLayout`，内部组件如下：
* `minBtn`：最小化按钮
* `maxBtn`：最大化按钮
* `closeBtn`：关闭按钮
* `iconLabel`：图标标签
* `titleLabel`：标题标签

如需隐藏最大化按钮并禁用标题栏双击最大化功能：
```python
self.titleBar.maxBtn.hide()
self.titleBar.setDoubleClickEnabled(False)
```


### 自定义背景色
`FluentWindow` 在云母特效未启用的情况下，浅色模式的背景为淡蓝色，深色模式为深灰色。可调用 `setCustomBackgroundColor()` 来自定义背景色：

```python
self.setCustomBackgroundColor(QColor(242, 242, 242), QColor(25, 33, 42))
```


### 背景失效解决办法
在 Win11 系统下，`FluentWindow` 默认启用了云母特效，如果窗口中使用了 `QWebEngineView` 或者 `QOpenGLWidget`，会导致窗口背景特效失效，同时圆角和阴影也会消失。

下述例子演示了如何正确地在 `FluentWindow` 中使用 Web 引擎；
```python
from qfluentwidgets import SplitFluentWindow, FluentIcon
from qframelesswindow.webengine import FramelessWebEngineView


class Widget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("homeInterface")

        # 1. 将 QWebEngineView 替换成 FramelessWebEngineView
        self.webView = FramelessWebEngineView(self)
        self.webView.load(QUrl("https://www.baidu.com/"))

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.vBoxLayout.addWidget(self.webView)


class Window(SplitFluentWindow):

    def __init__(self):
        super().__init__()

        # 创建并添加子界面
        self.homeInterface = Widget(self)
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, "Home")

        # 初始化窗口
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()

    # 2. 重新启用云母特效
    w.setMicaEffectEnabled(True)

    app.exec()
```

对于 `QOpenGLWidget`，需要在主界面的构造函数中强制调用 `FluentWindow.updateFrameless()` 并在显示主界面后重新启用云母特效。

## [SplitFluentWindow](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/window/fluent_window/index.html#)



`SplitFluentWindow` 使用方式和 [FluentWindow](#fluentwindow) 完全相同。


## [MSFluentWindow](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/window/fluent_window/index.html#)



`MSFluentWindow` 对 `NavigationBar` 和层叠组件进行了封装，使用这个类可以十分方便地创建多界面窗口，使用方式和 [FluentWindow](#fluentwindow) 相似。

只需调用 `addSubInterface()` 方法就能完成子界面的添加（必须先给子界面设置对象名才能调用此方法）：

```python
def addSubInterface(
    self,
    interface: QWidget,
    icon: FluentIconBase | QIcon | str,
    text: str,
    selectedIcon: FluentIconBase | QIcon | str = None,
    position=NavigationItemPosition.TOP,
    isTransparent=False
)
```

各个参数解释如下：
* `interface`: 需要添加的子界面
* `icon`：侧边栏菜单项图标
* `text`：侧边栏菜单项文本
* `selectedIcon`：侧边栏菜单项选中状态下的图标
* `position`：侧边栏菜单项的位置
* `isTransparent`：是否使用透明背景

下面是个简单的例子，更加复杂的示例见 [卡片例子](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/view/card_widget/demo.py)：

```python
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont)
from qfluentwidgets import FluentIcon as FIF


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))



class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = Widget('Home Interface', self)
        self.appInterface = Widget('Application Interface', self)
        self.videoInterface = Widget('Video Interface', self)
        self.libraryInterface = Widget('library Interface', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL)
        self.addSubInterface(self.appInterface, FIF.APPLICATION, '应用')
        self.addSubInterface(self.videoInterface, FIF.VIDEO, '视频')

        self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, '库', FIF.LIBRARY_FILL, NavigationItemPosition.BOTTOM)

        # 添加自定义导航组件
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://qfluentwidgets.com/zh/price/"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
```

### [FilledFluentWindow](https://qfluentwidgets.com/zh/price)



`FilledFluentWindow` 提供了侧边导航功能。

### [TopFluentWindow](https://qfluentwidgets.com/zh/price)



`TopFluentWindow` 提供了顶部导航功能。




============================================================
# Components > Window > Splash Screen
============================================================
---
title: 启动页面
date: 2024-03-14 13:52:00
permalink: /zh/pages/components/splashscreen/
---

### [SplashScreen](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/window/splash_screen/index.html)



`SplashScreen` 可用作启动页面，显示 Logo 和标题栏。

使用方式如下：

```python
# coding:utf-8
from qfluentwidgets import SplashScreen
from qframelesswindow import FramelessWindow, StandardTitleBar


class Demo(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.resize(700, 600)
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))

        # 1. 创建启动页面
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))

        # 2. 在创建其他子页面前先显示主界面
        self.show()

        # 3. 创建子界面
        self.createSubInterface()

        # 4. 隐藏启动页面
        self.splashScreen.finish()

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)
        loop.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
```

默认情况下 `SplashScreen` 的标题栏不显示图标和标题，可通过更换标题栏来设置图标和标题：
```python
from qframelesswindow import StandardTitleBar

titleBar = StandardTitleBar(self.splashScreen)
titleBar.setIcon(self.windowIcon())
titleBar.setTitle(self.windowTitle())
splashScreen.setTitleBar(titleBar)
```



============================================================
# Components > Navigation > Navigation Bar
============================================================
---
title: 侧边导航
date: 2023-08-17 19:00:22
permalink: /zh/pages/components/navigationbar/
---

## [NavigationInterface](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/navigation/navigation_interface/index.html#qfluentwidgets.components.navigation.navigation_interface.NavigationInterface)

::: tip 提示
只有需要高度定制侧边栏时才推荐直接使用这个类，否则请使用 [FluentWindow](/zh/pages/components/fluentwindow/)。
:::

### 结构

QFluentWidgets 提供侧边导航类 `NavigationInterface`，可以将它和 `QStackWidget` 放在 `QHBoxLayout` 中，实现多子界面跳转，示例程序参见 [navigation2](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/master/examples/navigation/navigation2/demo.py)。



`NavigationInterface` 内部使用 `NavigationPanel` 来放置导航菜单项。所有导航菜单项都需要继承自 `NavigationWidget`，可以调用 `NavigationInterface.addWidget()` 或者 `NavigationPanel.addWidget()` 将导航项添加到导航界面中。

QFluentWidgets 实现了子类 `NavigationTreeWidget` ，同时提供了一个便捷的方法 `NavigationInterface.addItem()` 来创建多级菜单项并将其到导航界面上。

如果希望自定义一个导航项，可以创建 `NavigationWidget` 的子类并实现它的 `paintEvent()` 和 `setCompacted()`（可选） 方法。下面是一个简单例子，展示了如何定义头像导航项：

```python
from qfluentwidgets import NavigationWidget


class AvatarWidget(NavigationWidget):
    """ Avatar widget """

    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.avatar = QImage('resource/shoko.png').scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)

        # draw background
        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        # draw avatar
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
            font = QFont('Segoe UI')
            font.setPixelSize(14)
            painter.setFont(font)
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignVCenter, 'zhiyiYo')
```


现在让我们看看 `addWidget()` 方法的各个参数：


```python
def addWidget(
    self,
    routeKey: str,
    widget: NavigationWidget,
    onClick=None,
    position=NavigationItemPosition.TOP,
    tooltip: str = None,
    parentRouteKey: str = None
)
```


可以看到，这个方法需要四个参数：

- `routeKey`：路由键，被添加到导航界面上的 `widget` 的唯一标识。如果将 `QStackWidget` 里面的子界面视为网页，`routeKey` 就是这个子界面的 URL。当用户切换子界面时，`NavigationPanel` 会将一个路由键添加到导航历史中。导航界面上的后退按钮被点击时，位于导航历史栈顶的路由键会被弹出，如果此时导航历史不为空，就可以切换到栈顶的路由键对应的子界面，否则就切换到 `defaultRouteKey` 对应的子界面，因此在运行 app 之前需要调用 `NavigationInterface.setDefaultRouteKey()` 设置一下默认子界面。
- `widget`：被添加到导航界面上的导航项。
- `onClick`：点击导航项时触发的槽函数。如果想在点击导航项时切换子界面，一种推荐的写法是将槽函数写作：`lambda: self.stackWidget.setCurrentWidget(self.xxxInterface)`。
- `position`：导航项的位置。可以是下述值中的一种：
  - `NavigationItemPosition.TOP`：添加到导航面板的顶部
  - `NavigationItemPosition.SCROLL`：添加到导航面板的滚动区域。当导航菜单项太多时，滚动区域中导航项可以被滚动
  - `NavigationItemPosition.BOTTOM`: 添加到导航面板的底部
- `tooltip`：菜单项的工具提示
- `parentRouteKey`: 父菜单项的路由键，父菜单项对应的小部件必须是 `NavigationTreeWidgetBase` 子类的实例

### 显示模式

导航面板有以下四种显示模式：

- `NavigationDisplayMode.EXPAND`：左侧面板完全展开（当窗口的宽度大于等于 1008px 时可用）
- `NavigationDisplayMode.COMPACT`：只在导航面板上显示图标，所有导航项都处于折叠状态（当窗口宽度小于 1007px 时默认使用这种显示模式）。
- `NavigationDisplayMode.MENU`：展开的导航菜单（当窗口窗口小于 1007px 并点击菜单按钮时使用此显示模式）
- `NavigationDisplayMode.MINIMAL`：只显示一个菜单按钮。在这种显示模式下，应该自己创建并管理菜单按钮和 `NavigationPanel`，然后将菜单按钮的点击信号连接到 `NavigationPanel.toggle()` 函数上，具体写法可以参见 [navigation3](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/master/examples/navigation/navigation3)。

如果调用了 `NavigationInterface.setExpandWidth()`，上述的窗口宽度阈值（1008px）将相应进行调整。

### 更多示例

下面是另外一种风格的导航界面，对应的示例程序为 [navigation](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/master/examples/navigation/navigation1/demo.py)。



迷你导航界面如下图所示，可以在 [navigation3](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/master/examples/navigation/navigation3) 获取完整代码。





============================================================
# Components > Navigation > Breadcrumb Bar
============================================================
---
title: 面包屑导航
date: 2024-02-26 19:56:01
permalink: /zh/pages/components/breadcrumbbar/
---

### [BreadcrumbBar](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/navigation/breadcrumb/index.html#qfluentwidgets.components.navigation.breadcrumb.BreadcrumbBar)



`BreadcrumbBar` 是作为辅助和补充的导航方式，它能让用户知道在应用中所处的位置并能方便地回到原先的位置。

通过 `addItem()` 可在右侧追加一个节点，当节点过多以至于视口容纳不下时，左侧的节点将被折叠到菜单中：

```python
breadcrumb = BreadcrumbBar()
items = ["主页", "文档", "学习资料", "动作电影", "叶问"]
for item in items:
    # 第一个参数为 routeKey，必须全局唯一
    breadcrumb.addItem(item, item)
```

当选中的节点变化时会发送 `currentItemChanged(routeKey: str)` 和 `currentIndexChanged(index: int)` 信号：
```python
breadcrumbBar.currentItemChanged.connect(lambda key: print(key))
```

调整面包屑的布局和字体：
```python
qfluentwidgets.setFont(breadcrumbBar, 26)
breadcrumbBar.setSpacing(20)
```

面包屑导航栏通常与 `QStackedWidget` 一起使用：
```python
class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet('Demo{background:rgb(255,255,255)}')

        self.breadcrumbBar = BreadcrumbBar(self)
        self.stackedWidget = QStackedWidget(self)

        self.lineEdit = LineEdit(self)
        self.addButton = PrimaryToolButton(FluentIcon.SEND, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.lineEditLayout = QHBoxLayout()

        # 按下回车键或者点击按钮时添加一个新导航项和子界面
        self.addButton.clicked.connect(lambda: self.addInterface(self.lineEdit.text()))
        self.lineEdit.returnPressed.connect(lambda: self.addInterface(self.lineEdit.text()))
        self.breadcrumbBar.currentItemChanged.connect(self.switchInterface)

        # 调整面包屑导航的尺寸
        setFont(self.breadcrumbBar, 26)
        self.breadcrumbBar.setSpacing(20)
        self.lineEdit.setPlaceholderText('Enter the name of interface')

        # 添加两个导航项
        self.addInterface('Home')
        self.addInterface('Documents')

        # 初始化布局
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.addWidget(self.breadcrumbBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.addLayout(self.lineEditLayout)

        self.lineEditLayout.addWidget(self.lineEdit, 1)
        self.lineEditLayout.addWidget(self.addButton)
        self.resize(500, 500)

    def addInterface(self, text: str):
        if not text:
            return

        w = SubtitleLabel(text)
        w.setObjectName(uuid1().hex)    # 使用随机生成的路由键
        w.setAlignment(Qt.AlignCenter)

        self.lineEdit.clear()
        self.stackedWidget.addWidget(w)
        self.stackedWidget.setCurrentWidget(w)

        self.breadcrumbBar.addItem(w.objectName(), text)

    def switchInterface(self, objectName):
        self.stackedWidget.setCurrentWidget(self.findChild(SubtitleLabel, objectName))
```



============================================================
# Components > Navigation > Tab Bar
============================================================
---
title: 标签栏
date: 2025-01-24 19:00:22
permalink: /zh/pages/components/tabbar/
---

### [TabBar](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/tab_view/index.html#qfluentwidgets.components.widgets.tab_view.TabBar)



`TabBar` 控件支持在一组标签页之间进行切换，并支持动态删除和添加标签。

通过 `addTab()` 可添加标签项，每个标签项需绑定一个全局唯一的 `routeKey`，返回值为 [TabItem](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/tab_view/index.html#qfluentwidgets.components.widgets.tab_view.TabItem) 实例。

```python
tabBar = TabBar()

# 添加标签项
tabBar.addTab(
    routeKey="songInfterface",
    text="Song",
    icon="/path/to/icon.png",
    onClick=lambda: print("Click")
)

# 获取当前标签项
print(self.tabBar.currentTab())
```

标签栏常用的信号有：
* `currentChanged(index: int)`: 切换当前选中的标签页
* `tabAddRequested`: 点击右侧的 `+` 按钮时发出此信号，表示请求添加新的标签页
* `tabCloseRequested(index: int)`: 点击标签项的 `×` 按钮时发出此信号，表示请求移除标签页

`TabBar` 通常与 `QStackedWidget` 一同使用，当用户点击不同的标签项时会切换当前页面，下面是个简单的例子：

```python
class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.counter = 1

        self.songInterface = QLabel('Song Interface', self)
        self.albumInterface = QLabel('Album Interface', self)
        self.artistInterface = QLabel('Artist Interface', self)

        # 添加标签页
        self.addSubInterface(self.songInterface, 'songInterface', 'Song')
        self.addSubInterface(self.albumInterface, 'albumInterface', 'Album')
        self.addSubInterface(self.artistInterface, 'artistInterface', 'Artist')

        # 连接信号
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.songInterface)
        self.tabBar.tabAddRequested.connect(self.onAddNewTab)
        self.tabBar.tabCloseRequested.connect(self.onCloseTab)

        self.vBoxLayout.setContentsMargins(30, 0, 30, 30)
        self.vBoxLayout.addWidget(self.tabBar, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.resize(400, 400)

    def addSubInterface(self, widget: QLabel, objectName: str, text: str):
        widget.setObjectName(objectName)
        widget.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(widget)

        # 使用全局唯一的 objectName 作为路由键
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.tabBar.setCurrentTab(widget.objectName())

    def onAddNewTab(self):
        w = QLabel(f"Tab {self.counter}")
        self.addSubInterface(w, w.text(), w.text())
        self.counter += 1

    def onCloseTab(self, index: int):
        item = self.tabBar.tabItem(index)
        widget = self.findChild(QLabel, item.routeKey())
        self.stackedWidget.removeWidget(widget)
        self.tabBar.removeTab(index)
        widget.deleteLater()

```


### [RoundTabBar](https://qfluentwidgets.com/zh/price)



`RoundTabBar` 控件支持在一组标签页之间进行切换，并支持动态删除和添加标签。



============================================================
# Components > Navigation > Top Navigation
============================================================
---
title: 顶部导航栏
date: 2024-02-26 19:56:01
permalink: /zh/pages/components/topnavigationbar/
---

### [Pivot](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/navigation/pivot/index.html#qfluentwidgets.components.navigation.pivot.Pivot)



`Pivot` 控件支持在一组标签项之间进行切换，被选中的标签项下会显示下划线。

通过 `addItem()` 可添加标签项，每个标签项需绑定一个全局唯一的 `routeKey`，返回值为 [PivotItem](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/navigation/pivot/index.html#qfluentwidgets.components.navigation.pivot.PivotItem) 实例。
```python
pivot = Pivot()

# 添加标签项
pivot.addItem(routeKey="songInterface", text="Song", onClick=lambda: print("Song"))
pivot.addItem(routeKey="albumInterface", text="Album", onClick=lambda: print("Album"))
pivot.addItem(routeKey="artistInterface", text="Artist", onClick=lambda: print("Artist"))

# 设置当前标签项
pivot.setCurrentItem("albumInterface")

# 获取当前标签项
print(pivot.currentItem())
```

顶部导航栏通常与 `QStackedWidget` 一同使用，当用户点击不同的标签项时会切换当前页面。

```python
class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.songInterface = QLabel('Song Interface', self)
        self.albumInterface = QLabel('Album Interface', self)
        self.artistInterface = QLabel('Artist Interface', self)

        # 添加标签页
        self.addSubInterface(self.songInterface, 'songInterface', 'Song')
        self.addSubInterface(self.albumInterface, 'albumInterface', 'Album')
        self.addSubInterface(self.artistInterface, 'artistInterface', 'Artist')

        # 连接信号并初始化当前标签页
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.songInterface)
        self.pivot.setCurrentItem(self.songInterface.objectName())

        self.vBoxLayout.setContentsMargins(30, 0, 30, 30)
        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.resize(400, 400)

    def addSubInterface(self, widget: QLabel, objectName: str, text: str):
        widget.setObjectName(objectName)
        widget.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(widget)

        # 使用全局唯一的 objectName 作为路由键
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
```


### [SegmentedWidget](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/navigation/segmented_widget/index.html#qfluentwidgets.components.navigation.segmented_widget.SegmentedWidget)



`SegmentedWidget` 分段导航控件支持在一组标签项之间进行切换，使用方式和 [Pivot](#pivot) 完全相同，`addItem()` 返回值为 [SegmentedItem](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/navigation/segmented_widget/index.html#qfluentwidgets.components.navigation.segmented_widget.SegmentedWidgetItem) 实例。

### [SegmentedToolWidget](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/navigation/segmented_widget/index.html#qfluentwidgets.components.navigation.segmented_widget.SegmentedToolWidget)



`SegmentedToolWidget` 图标分段导航控件支持在一组图标标签项之间进行切换。

通过 `addItem()` 可添加标签项，每个标签项需绑定一个全局唯一的 `routeKey`，返回值为 [SegmentedToolItem](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/navigation/segmented_widget/index.html#qfluentwidgets.components.navigation.segmented_widget.SegmentedToolItem) 实例。
```python
sw = SegmentedToolWidget()

# 添加标签项
sw.addItem(routeKey="songInterface", icon=FluentIcon.TRANSPARENT, onClick=lambda: print("Song"))
sw.addItem(routeKey="albumInterface", icon=FluentIcon.CHECKBOX, onClick=lambda: print("Album"))
sw.addItem(routeKey="artistInterface", icon=FluentIcon.CONSTRACT, onClick=lambda: print("Artist"))

# 设置当前标签项
sw.setCurrentItem("albumInterface")

# 获取当前标签项
print(sw.currentItem())
```

### [SegmentedToggleToolWidget](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/navigation/segmented_widget/index.html#qfluentwidgets.components.navigation.segmented_widget.SegmentedToggleToolWidget)



`SegmentedToggleToolWidget` 使用方式和 [SegmentedToolWidget](#segmentedtoolwidget) 完全相同，`addItem()` 的返回值为 [SegmentedToolItem](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/navigation/segmented_widget/index.html#qfluentwidgets.components.navigation.segmented_widget.SegmentedToggleToolItem) 实例。

### [TopNavigationBar](https://qfluentwidgets.com/zh/price)



`TopNavigationBar` 提供了顶部导航功能。

### [MenuBar](https://qfluentwidgets.com/zh/price)



`MenuBar` 提供了顶部菜单导航功能。

### [GuideWindow](https://qfluentwidgets.com/zh/price)



`GuideWindow` 提供了分步向导功能。




============================================================
# Components > Basic Input > Button
============================================================
---
title: 按钮
date: 2024-02-25 19:15:01
permalink: /zh/pages/components/button/
---

## 普通按钮
### [PushButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.PushButton)



`PushButton` 可用于显示文本和图标，使用方式与 `QPushButton` 完全相同。

不带图标的按钮：
```python
PushButton('Standard push button')
```

带图标的按钮，为了跟随主题，`PushButton` 接受 `FluentIconBase` 类型的图标：
```python
PushButton(FluentIcon.FOLDER, 'Standard push button with icon')
PushButton(QIcon("/path/to/icon.png"), 'Standard push button with icon')
```

### [ToolButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.ToolButton)



`ToolButton` 只用于显示图标，使用方式与 `QToolButton` 完全相同。

```python
ToolButton(FluentIcon.SETTING)
ToolButton(QIcon("/path/to/icon.png"))
```

### [PrimaryPushButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.PrimaryPushButton)




`PrimaryPushButton` 用于显示文本和图标，使用方式与 `QPushButton` 完全相同，当你想要突出显示某种操作时可用此按钮。


不带图标的按钮：
```python
PrimaryPushButton('Accent style button')
```

带图标的按钮：
```python
PrimaryPushButton(FluentIcon.UPDATE, 'Accent style button')
PrimaryPushButton(QIcon("/path/to/icon.png"), 'Accent style button with icon')
```


### [PrimaryToolButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.PrimaryToolButton)



`PrimaryToolButton` 只用于显示图标，使用方式与 `QToolButton` 完全相同，当你想要突出显示某种操作时可用此按钮。

```python
PrimaryToolButton(FluentIcon.FOLDER)
PrimaryToolButton(QIcon("/path/to/icon.png"))
```

### [TransparentPushButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.TransparentPushButton)



`TransparentPushButton` 用于显示文本和图标，使用方式与 `QPushButton` 完全相同。


不带图标的按钮：
```python
TransparentPushButton('Transparent push button')
```

带图标的按钮：
```python
TransparentPushButton(FluentIcon.BOOK_SHELF, 'Transparent push button')
TransparentPushButton(QIcon("/path/to/icon.png"), 'Transparent push button')
```

### [TransparentToolButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.TransparentToolButton)



`TransparentToolButton` 只用于显示图标，使用方式与 `QToolButton` 完全相同。

```python
TransparentToolButton(FluentIcon.MAIL)
TransparentToolButton(QIcon("/path/to/icon.png"))
```

### [HyperlinkButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.HyperlinkButton)



`HyperlinkButton` 可用于实现链接跳转。

不带图标的按钮：
```python
HyperlinkButton("https://qfluentwidgets.com", 'Hyperlink button')
```

带图标的按钮：
```python
HyperlinkButton(FluentIcon.LINK, "https://qfluentwidgets.com", 'Hyperlink button')
HyperlinkButton(QIcon("/path/to/icon.png"), "https://qfluentwidgets.com", 'Hyperlink button')
```

设置超链接：
```python
button.setUrl("https://www.youtube.com/watch?v=65AuZQ7tlKE")
button.setUrl(QUrl("https://www.youtube.com/watch?v=S0bXDRY1DGM"))
print(button.url)
```

### [HyperlinkToolButton](https://qfluentwidgets.com/zh/price)



`HyperlinkToolButton` 只用于显示图标，点击时可跳转到指定链接。


### [FilledPushButton](https://qfluentwidgets.com/zh/price)



`FilledPushButton` 用于显示图标和文本，可根据信息级别显示不同的背景色，使用方式和 `QPushButton` 完全相同。


### [FilledToolButton](https://qfluentwidgets.com/zh/price)



`FilledToolButton` 只用于显示图标，可根据信息级别显示不同的背景色，使用方式和 `QToolButton` 完全相同。


### [TextPushButton](https://qfluentwidgets.com/zh/price)



`TextPushButton` 用于显示图标和文本，可根据信息级别显示不同的前景色，使用方式和 `QPushButton` 完全相同。


### [TextToolButton](https://qfluentwidgets.com/zh/price)



`TextToolButton` 只用于显示图标，可根据信息级别显示不同的前景色，使用方式和 `QToolButton` 完全相同。


### [LuminaPushButton](https://qfluentwidgets.com/zh/price)



`LuminaPushButton` 用于显示图标和文本，可显示辉光，使用方式与 `QPushButton` 完全相同。

### [OutlinedPushButton](https://qfluentwidgets.com/zh/price)



`OutlinedPushButton` 用于显示图标和文本，默认可选中，使用方式与 `QPushButton` 完全相同，通常与 `QButtonGroup` 组合使用。


### [OutlinedToolButton](https://qfluentwidgets.com/zh/price)



`OutlinedToolButton` 只用于显示图标，默认可选中，使用方式与 `QToolButton` 完全相同。


### [RoundPushButton](https://qfluentwidgets.com/zh/price)



`RoundPushButton` 用于显示图标和文本，默认不可选中，使用方式与 `QPushButton` 完全相同。


### [RoundToolButton](https://qfluentwidgets.com/zh/price)



`RoundToolButton` 只用于显示图标，默认不可选中，使用方式与 `QToolButton` 完全相同。


## 状态开关按钮

状态开关按钮可在 `Qt.Checked` 和 `Qt.Unchecked` 两种选中状态间切换，状态发生改变时会发出 `toggled(checked: bool)` 信号。


### [TogglePushButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.TogglePushButton)



`TogglePushButton` 用于显示文本和图标，使用方式与 `QPushButton` 完全相同。


不带图标的按钮：
```python
button = TogglePushButton('Toggle push button')
button.toggled.connect(lambda checked: print(f"Button is checked: {checked}"))
```

带图标的按钮：
```python
TogglePushButton(FluentIcon.SEND, 'Toggle push button')
TogglePushButton(QIcon("/path/to/icon.png"), 'Toggle push button')
```

### [ToggleToolButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.ToggleToolButton)



`ToggleToolButton` 只用于显示图标，使用方式与 `QToolButton` 完全相同。


```python
ToggleToolButton(FluentIcon.GITHUB)
ToggleToolButton(QIcon("/path/to/icon.png"))
```


### [TransparentTogglePushButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.TransparentTogglePushButton)



`TransparentTogglePushButton` 用于显示文本和图标，使用方式与 [TogglePushButton](#togglepushbutton) 完全相同。

不带图标的按钮：
```python
button = TransparentTogglePushButton('Transparent toggle button')
button.toggled.connect(lambda checked: print(f"Button is checked: {checked}"))
```

带图标的按钮：
```python
TransparentTogglePushButton(FluentIcon.BOOK_SHELF, 'Transparent toggle button')
TransparentTogglePushButton(QIcon("/path/to/icon.png"), 'Transparent toggle button')
```

### [TransparentToggleToolButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.TransparentToggleToolButton)



`TransparentToggleToolButton` 只用于显示图标，使用方式与 [ToggleToolButton](#toggletoolbutton) 完全相同。


```python
TransparentToggleToolButton(FluentIcon.GITHUB)
TransparentToggleToolButton(QIcon("/path/to/icon.png"))
```

### [PillPushButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.PillPushButton)



`PillPushButton` 用于显示文本和图标，可拿来作为标签或者过滤器，使用方式与 [TogglePushButton](#togglepushbutton) 完全相同。

不带图标的按钮：
```python
PillPushButton('Pill push button')
```

带图标的按钮：
```python
PillPushButton(FluentIcon.CALENDAR, 'Pill push button')
PillPushButton(QIcon("/path/to/icon.png"), 'Pill push button')
```


### [PillToolButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.PillToolButton)



`PillToolButton` 只用于显示图标，可拿来作为标签或者过滤器，使用方式与 [TogglePushButton](#togglepushbutton) 完全相同。


```python
PillToolButton(FluentIcon.GITHUB)
PillToolButton(QIcon("/path/to/icon.png"))
```



## 下拉菜单按钮
### [DropDownPushButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.DropDownPushButton)



`DropDownPushButton` 点击时可弹出下拉菜单，且下拉菜单必须是 `RoundMenu` 及其子类。

```python
button = DropDownPushButton(FluentIcon.MAIL, 'Email')

# 创建菜单
menu = RoundMenu(parent=button)
menu.addAction(Action(FluentIcon.BASKETBALL, 'Basketball', triggered=lambda: print("你干嘛~")))
menu.addAction(Action(FluentIcon.ALBUM, 'Sing', triggered=lambda: print("喜欢唱跳RAP")))
menu.addAction(Action(FluentIcon.MUSIC, 'Music', triggered=lambda: print("只因你太美")))

# 添加菜单
button.setMenu(menu)
```

### [DropDownToolButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.DropDownToolButton)



`DropDownToolButton` 点击时可弹出下拉菜单，且下拉菜单必须是 `RoundMenu` 及其子类。

```python
button = DropDownToolButton(FluentIcon.MAIL)

# 创建菜单
menu = RoundMenu(parent=button)
menu.addAction(Action(FluentIcon.SEND_FIL, 'Send', triggered=lambda: print("已发送")))
menu.addAction(Action(FluentIcon.SAVE, 'Save', triggered=lambda: print("已保存")))

# 添加菜单
button.setMenu(menu)
```


### [PrimaryDropDownPushButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.PrimaryDropDownPushButton)



`PrimaryDropDownPushButton` 点击时可弹出下拉菜单，且下拉菜单必须是 `RoundMenu` 及其子类。

```python
button = PrimaryDropDownPushButton(FluentIcon.MAIL, 'Email')

# 创建菜单
menu = RoundMenu(parent=button)
menu.addAction(Action(FluentIcon.BASKETBALL, 'Basketball', triggered=lambda: print("你干嘛~")))
menu.addAction(Action(FluentIcon.ALBUM, 'Sing', triggered=lambda: print("喜欢唱跳RAP")))
menu.addAction(Action(FluentIcon.MUSIC, 'Music', triggered=lambda: print("只因你太美")))

# 添加菜单
button.setMenu(menu)
```


### [PrimaryDropDownToolButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.PrimaryDropDownToolButton)



`PrimaryDropDownToolButton` 点击时可弹出下拉菜单，且下拉菜单必须是 `RoundMenu` 及其子类。

```python
button = PrimaryDropDownToolButton(FluentIcon.MAIL, 'Email')

# 创建菜单
menu = RoundMenu(parent=button)
menu.addAction(Action(FluentIcon.SEND_FIL, 'Send', triggered=lambda: print("已发送")))
menu.addAction(Action(FluentIcon.SAVE, 'Save', triggered=lambda: print("已保存")))

# 添加菜单
button.setMenu(menu)
```


### [TransparentDropDownPushButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.TransparentDropDownPushButton)



`TransparentDropDownPushButton` 点击时可弹出下拉菜单，且下拉菜单必须是 `RoundMenu` 及其子类。

```python
button = TransparentDropDownPushButton(FluentIcon.MAIL, 'Email')

# 创建菜单
menu = RoundMenu(parent=button)
menu.addAction(Action(FluentIcon.BASKETBALL, 'Basketball', triggered=lambda: print("你干嘛~")))
menu.addAction(Action(FluentIcon.ALBUM, 'Sing', triggered=lambda: print("喜欢唱跳RAP")))
menu.addAction(Action(FluentIcon.MUSIC, 'Music', triggered=lambda: print("只因你太美")))

# 添加菜单
button.setMenu(menu)
```

### [TransparentDropDownToolButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.TransparentDropDownToolButton)



`TransparentDropDownToolButton` 点击时可弹出下拉菜单，且下拉菜单必须是 `RoundMenu` 及其子类。

```python
button = TransparentDropDownToolButton(FluentIcon.MAIL, 'Email')

# 创建菜单
menu = RoundMenu(parent=button)
menu.addAction(Action(FluentIcon.SEND_FIL, 'Send', triggered=lambda: print("已发送")))
menu.addAction(Action(FluentIcon.SAVE, 'Save', triggered=lambda: print("已保存")))

# 添加菜单
button.setMenu(menu)
```

## 拆分按钮
### [SplitPushButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.SplitPushButton)



`SplitPushButton` 由两个按钮组成，点击左侧按钮会触发 `clicked` 信号，点击右侧按钮可弹出下拉菜单，且下拉菜单必须是 `RoundMenu` 及其子类。

```python
button = SplitPushButton(FluentIcon.GITHUB, 'Split push button')
button.clicked.connect(lambda: print("点击左侧按钮"))

# 创建菜单
menu = RoundMenu(parent=button)
menu.addAction(Action(FluentIcon.BASKETBALL, 'Basketball', triggered=lambda: print("你干嘛~")))
menu.addAction(Action(FluentIcon.ALBUM, 'Sing', triggered=lambda: print("喜欢唱跳RAP")))
menu.addAction(Action(FluentIcon.MUSIC, 'Music', triggered=lambda: print("只因你太美")))

# 添加菜单
button.setFlyout(menu)
```

### [SplitToolButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.SplitToolButton)



`SplitToolButton` 由两个按钮组成，点击左侧按钮会触发 `clicked` 信号，点击右侧按钮可弹出下拉菜单，且下拉菜单必须是 `RoundMenu` 及其子类。

```python
button = SplitToolButton(FluentIcon.MAIL)
button.clicked.connect(lambda: print("点击左侧按钮"))

# 创建菜单
menu = RoundMenu(parent=button)
menu.addAction(Action(FluentIcon.SEND_FIL, 'Send', triggered=lambda: print("已发送")))
menu.addAction(Action(FluentIcon.SAVE, 'Save', triggered=lambda: print("已保存")))

# 添加菜单
button.setFlyout(menu)
```

### [PrimarySplitPushButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.PrimarySplitPushButton)



`PrimarySplitPushButton` 由两个按钮组成，点击左侧按钮会触发 `clicked` 信号，点击右侧按钮可弹出下拉菜单，且下拉菜单必须是 `RoundMenu` 及其子类。

```python
button = PrimarySplitPushButton(FluentIcon.GITHUB, 'Split push button')
button.clicked.connect(lambda: print("点击左侧按钮"))

# 创建菜单
menu = RoundMenu(parent=button)
menu.addAction(Action(FluentIcon.BASKETBALL, 'Basketball', triggered=lambda: print("你干嘛~")))
menu.addAction(Action(FluentIcon.ALBUM, 'Sing', triggered=lambda: print("喜欢唱跳RAP")))
menu.addAction(Action(FluentIcon.MUSIC, 'Music', triggered=lambda: print("只因你太美")))

# 添加菜单
button.setFlyout(menu)
```

### [PrimarySplitToolButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.PrimarySplitToolButton)



`PrimarySplitToolButton` 由两个按钮组成，点击左侧按钮会触发 `clicked` 信号，点击右侧按钮可弹出下拉菜单，且下拉菜单必须是 `RoundMenu` 及其子类。

```python
button = PrimarySplitToolButton(FluentIcon.MAIL)
button.clicked.connect(lambda: print("点击左侧按钮"))

# 创建菜单
menu = RoundMenu(parent=button)
menu.addAction(Action(FluentIcon.SEND_FIL, 'Send', triggered=lambda: print("已发送")))
menu.addAction(Action(FluentIcon.SAVE, 'Save', triggered=lambda: print("已保存")))

# 添加菜单
button.setFlyout(menu)
```

## 标签

### [Chip](https://qfluentwidgets.com/zh/price)



`Chip` 用于显示图标和文本，带有删除按钮，可作为标签供用户选择，使用方式和 `QPushButton` 完全相同。

### [Tag](https://qfluentwidgets.com/zh/price)



`Tag` 用于显示图标和文本，根据信息级别可显示不同的背景色和前景色，使用方式和 `QPushButton` 完全相同。



============================================================
# Components > Basic Input > Check Box
============================================================
---
title: 复选框
date: 2024-02-25 19:15:01
permalink: /zh/pages/components/checkbox/
---

### [CheckBox](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/check_box/index.html#qfluentwidgets.components.widgets.check_box.CheckBox)



`CheckBox` 用于在一组备选项中进行多选，使用方式与 `QCheckBox` 相同。

```python
checkBox = CheckBox("Text")

# 选中复选框
checkBox.setChecked(True)

# 监听复选框状态改变信号
checkBox.stateChanged.connect(lambda: print(checkBox.isChecked()))
```

`CheckBox` 同样支持三态：

```python
checkBox.setTristate(True)
checkBox.setCheckState(Qt.PartiallyChecked)
```

### [SubtitleCheckBox](https://qfluentwidgets.com/zh/price)



`SubtitleCheckBox` 是带子标题的复选框，使用方式与 `QCheckBox` 相同。



============================================================
# Components > Basic Input > Combo Box
============================================================
---
title: 下拉框
date: 2024-02-25 19:15:01
permalink: /zh/pages/components/combobox/
---

## [ComboBox](https://pyqt-fluent-widgets.readthedocs.io/en/latest/autoapi/qfluentwidgets/components/widgets/combo_box/index.html#qfluentwidgets.components.widgets.combo_box.ComboBox)



当选项过多时，适合使用下拉框展示并选择内容。`ComboBox` 继承自 `PushButton`，重新实现了 `QComboBox` 的大部分接口。

```python
comboBox = ComboBox()

# 添加选项
items = ['shoko', '西宫硝子', '宝多六花', '小鸟游六花']
comboBox.addItems(items)

# 当前选项的索引改变信号
comboBox.currentIndexChanged.connect(lambda index: print(comboBox.currentText()))
```

每个选项都可以绑定数据：
```python
comboBox.addItem('leetcode', userData="剑指 Offer")

# "leetcode" 对应的索引为 4，返回值为 "剑指 Offer"
comboBox.itemData(4)
```

添加选项之后默认选中第一个选项，如需取消选中：
```python
# 设置提示文本
comboBox.setPlaceholderText("选择一个脑婆")

# 取消选中
comboBox.setCurrentIndex(-1)
```

## [ModelComboBox](https://pyqt-fluent-widgets.readthedocs.io/en/latest/autoapi/qfluentwidgets/components/widgets/combo_box/index.html#qfluentwidgets.components.widgets.model_combo_box.ModelComboBox)

`ModelComboBox` 用法与 `ComboBox` 完全相同，并支持设置自定义数据模型（需要是 `QAbstractItemModel` 的子类），从而实现数据与界面的双向绑定。

```python
comboBox = ModelComboBox()

# 创建数据模型
model = QStandardItemModel()
model.appendRow(QStandardItem("Item 1"))
model.appendRow(QStandardItem("Item 2"))
model.appendRow(QStandardItem("Item 3"))

# 使用数据模型
comboBox.setModel(model)
```


## [EditableComboBox](https://pyqt-fluent-widgets.readthedocs.io/en/latest/autoapi/qfluentwidgets/components/widgets/combo_box/index.html#qfluentwidgets.components.widgets.combo_box.EditableComboBox)



`EditableComboBox` 允许用户编辑当前选项，按下回车可添加新选项。这个类继承自 `LineEdit`，同样不能在 Designer 中添加选项。

```python
comboBox = EditableComboBox()

# 添加选项
items = ['shoko', '西宫硝子', '宝多六花', '小鸟游六花']
comboBox.addItems(items)

# 当前选项的索引改变信号
comboBox.currentIndexChanged.connect(lambda index: print(comboBox.currentText()))
```

设置补全提示：
```python
# 创建补全器
items = ['shoko', '西宫硝子', '宝多六花', '小鸟游六花']
completer = QCompleter(items, comboBox)

# 设置显示的选项数
completer.setMaxVisibleItems(10)

# 设置补全器
comboBox.setCompleter(completer)
```

## [EditableModelComboBox](https://pyqt-fluent-widgets.readthedocs.io/en/latest/autoapi/qfluentwidgets/components/widgets/combo_box/index.html#qfluentwidgets.components.widgets.model_combo_box.EditableModelComboBox)

`EditableModelComboBox` 用法与 `EditableComboBox` 完全相同，并支持设置自定义数据模型（需要是 `QAbstractItemModel` 的子类），从而实现数据与界面的双向绑定。

```python
comboBox = EditableModelComboBox()

# 创建数据模型
model = QStandardItemModel()
model.appendRow(QStandardItem("Item 1"))
model.appendRow(QStandardItem("Item 2"))
model.appendRow(QStandardItem("Item 3"))

# 使用数据模型
comboBox.setModel(model)
```

## [MultiSelectionComboBox](https://qfluentwidgets.com/zh/price)



`MultiSelectionComboBox` 用于同时选择多个选项，并以标签的形式展示在下拉框中。

## [TreeComboBox](https://qfluentwidgets.com/zh/price)



`TreeComboBox` 它允许用户以层级方式浏览和选择数据。

## [MultiSelectionTreeComboBox](https://qfluentwidgets.com/zh/price)



`MultiSelectionTreeComboBox` 它允许用户以层级方式浏览和同时选择多个数据，并以标签的形式展示在下拉框中。

## [TransparentComboBox](https://qfluentwidgets.com/zh/price)



`TransparentComboBox` 是透明背景的下拉框，可以自定义当前选项的颜色。

## [FontComboBox](https://qfluentwidgets.com/zh/price)



`FontComboBox` 列出了系统所有可用字体供用户选择。



============================================================
# Components > Basic Input > Radio Button
============================================================
---
title: 单选按钮
date: 2024-02-26 11:29:01
permalink: /zh/pages/components/radiobutton/
---

### [RadioButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/button/index.html#qfluentwidgets.components.widgets.button.RadioButton)



`RadioButton` 用于在一组备选项中进行单选，使用方式与 `QRadioButton` 相同，一般和 `QButtonGroup` 组合使用。

```python
w = QWidget()

button1 = RadioButton('Option 1')
button2 = RadioButton('Option 2')
button3 = RadioButton('Option 3')

# 将单选按钮添加到互斥的按钮组
buttonGroup = QButtonGroup(w)
buttonGroup.addButton(button1)
buttonGroup.addButton(button2)
buttonGroup.addButton(button3)

# 当前选中的按钮发生改变
buttonGroup.buttonToggled.connect(lambda button: print(button.text()))

# 选中第一个按钮
button1.setChecked(True)

# 将按钮添加到垂直布局
layout = QVBoxLayout(w)
layout.addWidget(button1, 0, Qt.AlignCenter)
layout.addWidget(button2, 0, Qt.AlignCenter)
layout.addWidget(button3, 0, Qt.AlignCenter)
```

### [SubtitleRadioButton](https://qfluentwidgets.com/zh/price)



`SubtitleRadioButton` 带有标题和子标题，用于在一组备选项中进行单选，使用方式与 `QRadioButton` 相同。



============================================================
# Components > Basic Input > Slider
============================================================
---
title: 滑动条
date: 2024-02-26 11:29:01
permalink: /zh/pages/components/slider/
---

### [Slider](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/slider/index.html#qfluentwidgets.components.widgets.slider.Slider)



`Slider` 用于在一个固定区间内进行选择，使用方式和 `QSlider` 完全相同。

水平滑动条：
```python
slider = Slider(Qt.Horizontal)
slider.setFixedWidth(200)

# 设置取值范围和当前值
slider.setRange(0, 50)
slider.setValue(20)

# 获取当前值
print(slider.value())
```

垂直滑动条：
```python
Slider(Qt.Vertical)
```

### [ToolTipSlider](https://qfluentwidgets.com/zh/price)



`ToolTipSlider` 是带工具提示的滑动条，使用方式和 [Slider](#slider) 完全相同。

### [RangeSlider](https://qfluentwidgets.com/zh/price)



`RangeSlider` 用于选择一个范围值。



============================================================
# Components > Basic Input > Switch Button
============================================================
---
title: 开关按钮
date: 2024-02-26 11:29:01
permalink: /zh/pages/components/switchbutton/
---

### [SwitchButton](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/switch_button/index.html#qfluentwidgets.components.widgets.switch_button.SwitchButton)



`SwitchButton` 表示两种相互对立的状态间的切换，多用于触发「开/关」，开关状态改变时会发送 `checkedChanged(checked: bool)` 信号。

```python
button = SwitchButton()

button.checkedChanged.connect(lambda checked: print("是否选中按钮：", checked))

# 更改按钮状态
button.setChecked(True)

# 获取按钮是否选中
print(button.isChecked())
```

默认情况下按钮文本为「关/开」，可按照下述操作修改：
```python
button.setOffText("关闭")
button.setOnText("开启")
```



============================================================
# Components > Basic Input > Icon Widget
============================================================
---
title: 图标组件
date: 2024-07-24 13:52:00
permalink: /zh/pages/components/iconwidget/
---

### [IconWidget](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/icon_widget/index.html#qfluentwidgets.components.widgets.icon_widget.IconWidget)



`IconWidget` 用于显示图标，支持传入 `FluentIconBase`、`QIcon` 和 `str` 类型的图标。

创建一个图标组件并调整图标大小：
```python
w = IconWidget(FluentIcon.AIRPLANE)
w.setFixedSize(20, 20)
```

更换图标：
```python
# 类型为 FluentIconBase 子类
w.setIcon(InfoBarIcon.SUCCESS)
w.setIcon(FluentIcon.AIRPLANE.colored(Qt.red, Qt.blue))

# 类型为 QIcon
w.setIcon(QIcon("/path/to/icon"))

# 类型为 str，代表图标路径
w.setIcon("/path/to/icon")
```




============================================================
# Components > Text > Label
============================================================
---
title: 标签
date: 2024-02-27 13:34:00
permalink: /zh/pages/components/label/
---

### [FluentLabelBase](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/label/index.html#qfluentwidgets.components.widgets.label.FluentLabelBase)



`FluentLabelBase` 用于显示文本，可以跟随主题切换文本颜色。这是个抽象类，通常使用它的子类：
* CaptionLabel
* BodyLabel
* StrongBodyLabel
* SubtitleLabel
* TitleLabel
* LargeTitleLabel
* DisplayLabel

可以自定义标签的颜色：
```python
label = BodyLabel("标签")
label.setTextColor(QColor(0, 255, 0), QColor(255, 0, 0))  # 浅色主题，深色主题
```

### [HyperlinkLabel](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/label/index.html#qfluentwidgets.components.widgets.label.HyperlinkLabel)



`HyperlinkLabel` 可在点击时自动跳转到指定链接。

```python
label = HyperlinkLabel(QUrl('https://github.com/'), 'GitHub')

# 显示下划线
hyperlinkLabel.setUnderlineVisible(True)

# 更换超链接
label.setUrl('https://github.com/zhiyiYo/')
print(label.url)
```

### [ImageLabel](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/label/index.html#qfluentwidgets.components.widgets.label.ImageLabel)




`ImageLabel` 用于显示图片或者 GIF，在高分屏下也能清晰显示图片而不出现锯齿。

```python
image = ImageLabel("/path/to/image.png")

# 按比例缩放到指定高度
image.scaledToHeight(300)

# 圆角
image.setBorderRadius(8, 8, 8, 8)
```

### [AvatarWidget](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/label/index.html#qfluentwidgets.components.widgets.label.AvatarWidget)




`AvatarWidget` 用于显示圆形头像，可以是静态图片或者 GIF。

```python
w = AvatarWidget("/path/to/image.png")

# 设置头像半径
w.setRadius(64)
```

如果不设置图片，头像组件也可以居中显示文本的首字母：



```python
w = AvatarWidget()
w.setRadius(64)

# 设置文本
w.setText("乔尼·乔斯达")
```

### [AvatarPicker](https://qfluentwidgets.com/zh/price)



`AvatarPicker` 用于显示圆形头像，可以是静态图片或者 GIF，并支持鼠标点击时选择经过裁剪的本地图片作为头像。



============================================================
# Components > Text > Line Edit
============================================================
---
title: 输入框
date: 2024-02-27 16:46:00
permalink: /zh/pages/components/lineedit/
---

### [LineEdit](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/line_edit/index.html#qfluentwidgets.components.widgets.line_edit.LineEdit)



`LineEdit` 用于编辑单行文本，使用方式和 `QLineEdit` 完全相同。

```python
lineEdit = LineEdit()

# 设置提示文本
lineEdit.setPlaceholderText("example@example.com")

# 设置文本
lineEdit.setText("shokokawaii@foxmail.com")
print(lineEdit.text())

# 启用清空按钮
lineEdit.setClearButtonEnabled(True)
```

设置补全菜单：
```python
stands = [
    "Star Platinum", "Hierophant Green", "Made in Haven",
    "King Crimson", "Silver Chariot", "Crazy diamond"
]
completer = QCompleter(stands, lineEdit)
completer.setCaseSensitivity(Qt.CaseInsensitive)
completer.setMaxVisibleItems(10)

lineEdit.setCompleter(completer)
```

自定义动作：
```python
from qfluentwidgets import Action, FluentIcon

# 在后面添加按钮
action1 = QAction(FluentIcon.CALENDAR.qicon(), "", triggered=lambda: print("action1 triggered"))
lineEdit.addAction(action1, QLineEdit.TrailingPosition)

# 在前面添加按钮
action2 = Action(FluentIcon.ADD, "", triggered=lambda: print("action2 triggered"))
lineEdit.addAction(action2, QLineEdit.LeadingPosition)
```

### [SearchLineEdit](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/line_edit/index.html#qfluentwidgets.components.widgets.line_edit.SearchLineEdit)



`SearchLineEdit` 在 [LineEdit](#lineedit) 右侧添加了搜索按钮，点击按钮或按下回车时会发送 `searchSignal(text: str)` 信号。

```python
lineEdit = SearchLineEdit()
lineEdit.searchSignal.connect(lambda text: print("搜索：" + text))
```

### [PasswordLineEdit](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/line_edit/index.html#qfluentwidgets.components.widgets.line_edit.PasswordLineEdit)



`PasswordLineEdit` 用于编辑密码，默认情况下按钮不可见。
```python
lineEdit = PasswordLineEdit()
lineEdit.setText("123456")

# 显示密码
lineEdit.setPasswordVisible(True)
```

### [PinBox](https://qfluentwidgets.com/zh/price)



`PinBox` 可用于需要用户输入特定格式或内容的场景，比如 PIN 码、验证码、密码等。


### [TokenLineEdit](https://qfluentwidgets.com/zh/price)



`TokenLineEdit` 可用于输入和管理标签。

### [LabelLineEdit](https://qfluentwidgets.com/zh/price)



`LabelLineEdit` 是带前后缀标签的输入框。


### [TextEdit](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/line_edit/index.html#qfluentwidgets.components.widgets.line_edit.TextEdit)



`TextEdit` 是富文本多行编辑框，可以渲染 HTML 和 Markdown 格式的文本，使用方式和 `QTextEdit` 完全相同。

```python
textEdit = TextEdit()
textEdit.setMarkdown("## Steel Ball Run \n * Johnny Joestar 🦄 \n * Gyro Zeppeli 🐴 ")

# 获取普通文本
print(textEdit.toPlainText())

# 获取富文本
print(textEdit.toHtml())
```


### [PlainTextEdit](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/line_edit/index.html#qfluentwidgets.components.widgets.line_edit.PlainTextEdit)



`PlainTextEdit` 是普通文本多行编辑框，使用方式和 `QPlainTextEdit` 完全相同。

```python
textEdit = PlainTextEdit()
textEdit.setPlainText("两岸猿声啼不住 \n 轻舟已过万重山 ")

# 获取普通文本
print(textEdit.toPlainText())
```

### [TextBrowser](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/line_edit/index.html#qfluentwidgets.components.widgets.line_edit.TextBrowser)



`TextBrowser` 是只读富文本多行编辑框，可以渲染 HTML 和 Markdown 格式的文本，使用方式和 `QTextBrowser` 完全相同。

```python
textBrowser = TextBrowser()
textBrowser.setMarkdown("## Steel Ball Run \n * Johnny Joestar 🦄 \n * Gyro Zeppeli 🐴 ")

# 获取普通文本
print(textBrowser.toPlainText())

# 获取富文本
print(textBrowser.toHtml())
```

### [CodeEdit](https://qfluentwidgets.com/zh/price)



`CodeEdit` 可用于显示和编辑代码，内置 20 种语言的语法高亮。



============================================================
# Components > Text > Spin Box
============================================================
---
title: 微调框
date: 2024-02-27 17:42:00
permalink: /zh/pages/components/spinbox/
---

### [SpinBox](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/spin_box/index.html#qfluentwidgets.components.widgets.spin_box.SpinBox)



`SpinBox` 用于让用户在一定范围内选择一个整数值，使用方法和 `QSpinBox` 完全相同。`CompactSpinBox` 是紧凑版本的 `SpinBox`。

```python
spinBox = SpinBox()

# 设置取值范围
spinBox.setRange(0, 100)

# 设置当前值
spinBox.setValue(30)

# 监听数值改变信号
spinBox.valueChanged.connect(lambda value: print("当前值：", value))

# 获取当前值
print(spinBox.value())
```

### [DoubleSpinBox](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/spin_box/index.html#qfluentwidgets.components.widgets.spin_box.DoubleSpinBox)



`DoubleSpinBox` 用于让用户在一定范围内选择一个整数值，使用方法和 `QDoubleSpinBox` 完全相同。`CompactDoubleSpinBox` 是紧凑版本的 `DoubleSpinBox`。

```python
spinBox = DoubleSpinBox()

# 设置取值范围
spinBox.setRange(-100, 100)

# 设置当前值
spinBox.setValue(30.5)

# 监听数值改变信号
spinBox.valueChanged.connect(lambda value: print("当前值：", value))

# 获取当前值
print(spinBox.value())
```


### [TimeEdit](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/spin_box/index.html#qfluentwidgets.components.widgets.spin_box.TimeEdit)



`TimeEdit` 用于让用户在一定时间范围内选择一个时间，使用方法和 `QTimeEdit` 完全相同。`CompactTimeEdit` 是紧凑版本的 `TimeEdit`。

```python
timeEdit = TimeEdit()

# 设置取值范围
timeEdit.setTimeRange(QTime(0, 0, 0), QTime(11, 59, 59))

# 设置当前值
timeEdit.setTime(QTime(1, 1, 1))

# 监听数值改变信号
timeEdit.timeChanged.connect(lambda time: print("当前时间：", time.toString()))

# 获取当前值
print(timeEdit.time())
```


### [DateEdit](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/spin_box/index.html#qfluentwidgets.components.widgets.spin_box.DateEdit)



`DateEdit` 用于让用户在一定日期范围内选择一个日期，使用方法和 `QDateEdit` 完全相同。`CompactDateEdit` 是紧凑版本的 `DateEdit`。

```python
dateEdit = DateEdit()

# 设置取值范围
dateEdit.setDateRange(QDate(2024, 1, 1), QDate(2024, 11, 11))

# 设置当前值
dateEdit.setDate(QDate(2024, 2, 2))

# 监听数值改变信号
dateEdit.dateChanged.connect(lambda date: print("当前日期：", date.toString()))

# 获取当前值
print(dateEdit.date())
```

### [DateTimeEdit](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/spin_box/index.html#qfluentwidgets.components.widgets.spin_box.DateTimeEdit)



`DateTimeEdit` 用于让用户在一定日期范围内选择一个日期，使用方法和 `QDateTimeEdit` 完全相同。`CompactDateTimeEdit` 是紧凑版本的 `DateTimeEdit`。

```python
dt = DateTimeEdit()

# 设置取值范围
dt.setDateTimeRange(QDate(2024, 1, 1, 0, 0, 0), QDate(2024, 11, 11, 11, 59, 59))

# 设置当前值
dt.setDateTime(QDateTime(2024, 2, 2, 12, 0, 0))

# 监听数值改变信号
dt.dateTimeChanged.connect(lambda dateTime: print("当前日期时间：", dateTime.toString()))

# 获取当前值
print(dt.dateTime())
```



============================================================
# Components > Dialog Flyout > Message Box
============================================================
---
title: 消息框
date: 2024-02-26 15:04:01
permalink: /zh/pages/components/messagebox/
---

### [Dialog](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/dialog_box/dialog/index.html#qfluentwidgets.components.dialog_box.dialog.Dialog)




`Dialog` 是模态无边框对话框，用于用于消息提示、确认消息和提交内容。该对话框会中断用户操作，直到用户确认知晓后才可关闭。

```python
w = Dialog("标题", "这是一条消息通知", window)

if w.exec():
    print('确认')
else:
    print('取消')
```

修改按钮文本：

```python
w.yesButton.setText("来啦老弟")
w.cancelButton.setText("但是我拒绝")
```

隐藏确定按钮：
```python
w.yesButton.hide()
w.buttonLayout.insertStretch(0, 1)
```

隐藏取消按钮：
```python
w.cancelButton.hide()
w.buttonLayout.insertStretch(1)
```

如果同时使用 `Dialog` 和 `FluentWindow`，可能导致窗口无法拉伸，解决方案如下：
```python
app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
```

### [MessageBox](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/dialog_box/dialog/index.html#qfluentwidgets.components.dialog_box.dialog.MessageBox)




`MessageBox` 是模态遮罩对话框，使用方式和 [Dialog](#dialog) 一样。

最好将对话框的父级设置为主窗口，这样遮罩的尺寸就能和主窗口保持一致。

```python
w = MessageBox("标题", "这是一条消息通知", window)

if w.exec():
    print('确认')
else:
    print('取消')
```

### [MessageBoxBase](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/dialog_box/message_box_base/index.html#qfluentwidgets.components.dialog_box.message_box_base.MessageBoxBase)

如果你想自定义对话框的内容，可继承 `MessageBoxBase` 并往 `viewLayout` 垂直布局中添加组件。下述代码创建了一个输入框对话框：
```python
class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('打开 URL')
        self.urlLineEdit = LineEdit()

        self.urlLineEdit.setPlaceholderText('输入文件、流或者播放列表的 URL')
        self.urlLineEdit.setClearButtonEnabled(True)

        # 将组件添加到布局中
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)

        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(350)


def showMessage(window):
    w = CustomMessageBox(window)
    if w.exec():
        print(w.urlLineEdit.text())
```

运行效果如下：


对话框提供了 `validate() -> bool` 方法，通过重写此方法，可在用户点击确定按钮时验证表单数据，返回 True 代表表单数据正确，对话框会自动关闭。下面是一个示例：

```python
class CustomMessageBox(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('打开 URL', self)
        self.urlLineEdit = LineEdit(self)

        self.urlLineEdit.setPlaceholderText('输入文件、流或者播放列表的 URL')
        self.urlLineEdit.setClearButtonEnabled(True)

        self.warningLabel = CaptionLabel("URL 不正确")
        self.warningLabel.setTextColor("#cf1010", QColor(255, 28, 32))

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)
        self.viewLayout.addWidget(self.warningLabel)
        self.warningLabel.hide()

        self.widget.setMinimumWidth(350)

    def validate(self):
        """ 重写验证表单数据的方法 """
        isValid = QUrl(self.urlLineEdit.text()).isValid()
        self.warningLabel.setHidden(isValid)
        return isValid

```




============================================================
# Components > Dialog Flyout > Flyout
============================================================
---
title: 弹出组件
date: 2024-02-26 16:55:01
permalink: /zh/pages/components/flyout/
---

### [Flyout](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/flyout/index.html#qfluentwidgets.components.widgets.flyout.Flyout)



`Flyout` 可以收集用户的输入、显示项目的更多详细信息或要求用户确认操作。与对话框不同的是，可以通过点击空白位置来轻松关闭弹出窗口。

下述示例创建了一个包含图标、标题、内容和关闭按钮的弹出窗口：
```python
class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.button = PushButton("Click Me", self)
        self.button.clicked.connect(self.showFlyout)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignCenter)
        self.resize(600, 500)

    def showFlyout(self):
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='Lesson 4',
            content="表达敬意吧，表达出敬意，然后迈向回旋的另一个全新阶段！",
            target=self.button,
            parent=self,
            isClosable=True,
            aniType=FlyoutAnimationType.PULL_UP
        )
```

也可以在弹出窗口中显示图片：

```python
Flyout.create(
    image="/path/to/image.png",
    title='Lesson 4',
    content="表达敬意吧，表达出敬意，然后迈向回旋的另一个全新阶段！",
    target=self.button,
    parent=self,
    isClosable=False
)
```

下述例子向弹出窗口中添加了自定义组件：

```python
view = FlyoutView(
    title='Lesson 5',
    content="最短的捷径就是绕远路，绕远路才是我的最短捷径。",
    image='/path/to/image.png',
    isClosable=True
)

# 添加按钮
button = PushButton('Action')
button.setFixedWidth(120)
view.addWidget(button, align=Qt.AlignRight)

# 调整布局
view.widgetLayout.insertSpacing(1, 5)
view.widgetLayout.addSpacing(5)

# 显示弹出窗口
w = Flyout.make(view, self.button, self)
view.closed.connect(w.close)
```

`Flyout` 在 macOS 下可能无法使用中文输入法，解决方案是在创建 `Flyout` 的时候将 `isMacInputMethodEnabled` 置为 `True`：
```python
Flyout.make(..., isMacInputMethodEnabled=True)
Flyout.create(..., isMacInputMethodEnabled=True)
```

### [FlyoutViewBase](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/flyout/index.html#qfluentwidgets.components.widgets.flyout.FlyoutViewBase)



`Flyout` 只是个容器，内部的 `view` 可被任何 `FlyoutViewBase` 的子类实例替换，从而自定义窗口内容。

```python
class CustomFlyoutView(FlyoutViewBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.label = BodyLabel('这是一场「试炼」，我认为这就是一场为了战胜过去的「试炼」，\n只有战胜了那些幼稚的过去，人才能有所成长。')
        self.button = PrimaryPushButton('Action')

        self.button.setFixedWidth(140)

        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(20, 16, 20, 16)
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self.button)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.button = PushButton("Click Me", self)
        self.button.clicked.connect(self.showFlyout)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignCenter)
        self.resize(600, 500)

    def showFlyout(self):
        Flyout.make(CustomFlyoutView(), self.button, self, aniType=FlyoutAnimationType.PULL_UP)
```


### [FlyoutDialog](https://qfluentwidgets.com/zh/price/)



`FlyoutDialog` 是个对话框容器，内部可被任何 `QWidget` 的子类实例替换，从而自定义对话框内容。



============================================================
# Components > Dialog Flyout > Color Dialog
============================================================
---
title: 颜色选择器
date: 2024-02-26 16:55:01
permalink: /zh/pages/components/colorpicker/
---

### [ColorDialog](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/dialog_box/color_dialog/index.html)



`ColorDialog` 用于选择颜色，选中的颜色发生变化时会发送 `colorChanged(color: QColor)` 信号。

```python
w = ColorDialog(QColor(0, 255, 255), "Choose Background Color", window, enableAlpha=False)
w.colorChanged.connect(lambda color: print(color.name()))
w.exec()
```


### [DropDownColorPalette](https://qfluentwidgets.com/zh/price)



`DropDownColorPalette` 提供了一系列颜色供用户选择。



### [DropDownColorPicker](https://qfluentwidgets.com/zh/price)



`DropDownColorPicker` 提供了弹出窗口供用户调整和挑选颜色。


### [CircleColorPicker](https://qfluentwidgets.com/zh/price)



`CircleColorPicker` 提供了一系列颜色供用户选择。

### [ScreenColorPicker](https://qfluentwidgets.com/zh/price)



`ScreenColorPicker` 用于选取屏幕任意位置的颜色。



============================================================
# Components > Dialog Flyout > Image Cropper
============================================================
---
title: 图片裁剪器
date: 2024-02-26 16:55:01
permalink: /zh/pages/components/imagecropper/
---


### [ImageCropper](https://qfluentwidgets.com/zh/price)



`ImageCropper` 用于裁剪用户指定的图像，内置长方形和圆形两种裁剪形状，并支持拓展自定义的裁剪形状。



============================================================
# Components > Dialog Flyout > Teaching Tip
============================================================
---
title: 气泡弹窗
date: 2024-02-26 19:00:01
permalink: /zh/pages/components/teachingtip/
---

### [TeachingTip](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/teaching_tip/index.html#qfluentwidgets.components.widgets.teaching_tip.TeachingTip)



`TeachingTip` 可以收集用户的输入、显示项目的更多详细信息或要求用户确认操作。

下述示例创建了一个包含图标、标题、内容和关闭按钮的气泡弹窗，并在 2s 后自动消失：
```python
class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.button = PushButton("Click Me", self)
        self.button.clicked.connect(self.showTeachingTip)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignCenter)
        self.resize(600, 500)

    def showTeachingTip(self):
        TeachingTip.create(
            target=self.button,
            icon=InfoBarIcon.SUCCESS,
            title='Lesson 4',
            content="表达敬意吧，表达出敬意，然后迈向回旋的另一个全新阶段！",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )
```

在气泡弹窗中显示图片：

```python
TeachingTip.create(
    target=self.button,
    image="/path/to/image.png",
    title='Lesson 4',
    content="表达敬意吧，表达出敬意，然后迈向回旋的另一个全新阶段！",
    isClosable=True,
    tailPosition=TeachingTipTailPosition.BOTTOM,
    duration=2000,
    parent=self
)
```

在气泡弹窗中添加自定义组件：

```python
position = TeachingTipTailPosition.BOTTOM
view = TeachingTipView(
    icon=None,
    title='Lesson 5',
    content="最短的捷径就是绕远路，绕远路才是我的最短捷径。",
    image='/path/to/image.png',
    isClosable=True,
    tailPosition=position,
)

# 添加组件
button = PushButton('Action')
button.setFixedWidth(120)
view.addWidget(button, align=Qt.AlignRight)

w = TeachingTip.make(
    target=self.button,
    view=view,
    duration=-1,    # 关闭自动消失
    tailPosition=position,
    parent=self
)
view.closed.connect(w.close)
```

`TeachingTip` 允许更换内部的 `bubble.view` 为 `FlyoutViewBase` 子类的实例，从而自定义窗口内容。



```python
class CustomFlyoutView(FlyoutViewBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.label = BodyLabel('这是一场「试炼」，我认为这就是一场为了战胜过去的「试炼」，\n只有战胜了那些幼稚的过去，人才能有所成长。')
        self.button = PrimaryPushButton('Action')

        self.button.setFixedWidth(140)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(20, 16, 20, 16)
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self.button)

    def paintEvent(self, e):
        # 不绘制边框和背景
        pass


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.button = PushButton("Click Me", self)
        self.button.clicked.connect(self.showTeachingTip)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignCenter)
        self.resize(600, 500)

    def showTeachingTip(self):
        TeachingTip.make(
            target=self.button,
            view=CustomFlyoutView(),
            tailPosition=TeachingTipTailPosition.RIGHT,
            duration=2000,
            parent=self
        )
```

### [PopupTeachingTip](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/teaching_tip/index.html#qfluentwidgets.components.widgets.teaching_tip.PopupTeachingTip)

`PopupTeachingTip` 是模态的，点击空白处可直接关闭，使用方法和 [TeachingTip](#teachingtip) 完全相同。



============================================================
# Components > Dialog Flyout > Shortcut Picker
============================================================
---
title: 快捷键选择器
date: 2024-02-26 16:55:01
permalink: /zh/pages/components/shortcutpicker/
---

### [ShortcutPicker](https://qfluentwidgets.com/zh/price)



`ShortcutPicker` 用于捕获用户按下的快捷键。



============================================================
# Components > Status Info > Info Bar
============================================================
---
title: 消息条
date: 2024-02-27 13:34:00
permalink: /zh/pages/components/infobar/
---

### [InfoBar](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/info_bar/index.html)



`InfoBar` 用于在应用程序中显示重要的、用户需要知道的信息。这个信息可以是一个错误消息，一个警告，或者一个提示，让用户知道他们需要采取行动。

组件库提供了便捷的类方法来创建不同类型的 `InfoBar`：

* 成功：
    ```python
    InfoBar.success(
        title='Lesson 4',
        content="表达敬意吧，表达出敬意，然后迈向回旋的另一个全新阶段！",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.TOP,
        duration=2000,
        parent=window
    )
    ```

* 警告：
    ```python
    InfoBar.warning(
        title='Lesson 3',
        content="相信回旋吧，只相信便是！",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.BOTTOM,
        duration=-1,    # 永不消失
        parent=window
    )
    ```

* 失败：
    ```python
    InfoBar.error(
        title='Lesson 5',
        content="最短的捷径就是绕远路，绕远路才是我的最短捷径。",
        orient=Qt.Vertical,  # 内容太长时可使用垂直布局
        isClosable=True,
        position=InfoBarPosition.BOTTOM_RIGHT,
        duration=-1,
        parent=window
    )
    ```

* 消息：
    ```python
    InfoBar.info(
        title='Lesson 5',
        content="最短的捷径就是绕远路，绕远路才是我的最短捷径。",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.BOTTOM_LEFT,
        duration=-1,
        parent=window
    )
    ```

* 自定义：
    ```python
    w = InfoBar.new(
        icon=FluentIcon.GITHUB,
        title='波纹疾走',
        content="人类的赞歌就是勇气的赞歌，人类的伟大就是勇气的伟大！",
        orient=Qt.Horizontal,
        isClosable=True,
        position=InfoBarPosition.BOTTOM,
        duration=2000,
        parent=window
    )
    w.setCustomBackgroundColor('white', '#202020')
    ```

也可以往消息条上添加按钮等自定义组件：
```python
w = InfoBar(
    icon=InfoBarIcon.SUCCESS,
    title='Title',
    content="我的名字是吉良吉影，年龄 33 岁，只想过平静的生活。",
    orient=Qt.Horizontal,
    isClosable=True,
    position=InfoBarPosition.TOP_RIGHT,
    duration=2000,
    parent=window
)

# 添加自定义组件
w.addWidget(PushButton('Action'))
w.show()
```

消息条的弹出位置由 `position` 参数指定：
```python
class InfoBarPosition(Enum):
    """ Info bar position """
    TOP = 0
    BOTTOM = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5
    NONE = 6
```

当 `InfoBarPosition` 为 `NONE` 时，可以将消息条放在任意位置，如果想进一步管理消息条位置，可继承 `InfoBarManager`：
```python
@InfoBarManager.register('Custom')
class CustomInfoBarManager(InfoBarManager):
    """ 自定义消息条管理器 """

    def _pos(self, infoBar: InfoBar, parentSize=None):
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        # 第一个消息条的位置
        x = (parentSize.width() - infoBar.width()) // 2
        y = (parentSize.height() - infoBar.height()) // 2

        # 计算当前 infoBar 的位置
        index = self.infoBars[p].index(infoBar)
        for bar in self.infoBars[p][0:index]:
            y += (bar.height() + self.spacing)

        return QPoint(x, y)

    def _slideStartPos(self, infoBar: InfoBar):
        pos = self._pos(infoBar)
        return QPoint(pos.x(), pos.y() - 16)



InfoBar.success(
    title='Lesson 4',
    content="表达敬意吧，表达出敬意，然后迈向回旋的另一个全新阶段！",
    orient=Qt.Horizontal,
    isClosable=True,
    position="Custom",  # 使用自定义管理器
    duration=2000,
    parent=window
)
```


### [Toast](https://qfluentwidgets.com/zh/price)



`Toast` 用于在应用程序中显示重要的、用户需要知道的信息。


### [ProgressInfoBar](https://qfluentwidgets.com/zh/price)



`ProgressInfoBar` 它不仅显示任务的完成进度，还可以显示额外的信息。这些信息通常包括任务的名称、描述、剩余时间等。这种组件非常适合用于需要同时展示任务进度和其他相关信息的场合。


### [ProgressToast](https://qfluentwidgets.com/zh/price)



`ProgressToast` 可以同时显示任务进度和提示信息。



============================================================
# Components > Status Info > Info Badge
============================================================
---
title: 徽章
date: 2024-02-27 11:25:00
permalink: /zh/pages/components/infobadge/
---

### [InfoBadge](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/info_badge/index.html#qfluentwidgets.components.widgets.info_badge.InfoBadge)



`InfoBadge` 是一个小型的通知标记，用于在应用的导航菜单或工具栏上显示未读消息、状态更新或其他重要通知。

徽章支持多种样式，并提供了便捷的类方法来创建实例：
```python
InfoBadge.info(1)
InfoBadge.success(10)
InfoBadge.attension(100)
InfoBadge.warning(1000)
InfoBadge.error(10000)
InfoBadge.custom('1w+', '#005fb8', '#60cdff')
```

徽章通常附着在其他组件上，通过设置 `target` 可指定附着对象：
```python
button = ToolButton(FIF.BASKETBALL, parent)
vBoxLayout.addWidget(button, 0, Qt.AlignHCenter)
InfoBadge.success(1, parent=parent, target=button, position=InfoBadgePosition.TOP_RIGHT)
```

`position` 参数用于设置徽章的位置，组件库内置了 7 种徽章位置：
```python
class InfoBadgePosition(Enum):
    """ Info badge position """
    TOP_RIGHT = 0
    BOTTOM_RIGHT = 1
    RIGHT = 2
    TOP_LEFT = 3
    BOTTOM_LEFT = 4
    LEFT = 5
    NAVIGATION_ITEM = 6
```

如果你想自定义徽章的位置，可继承 `InfoBadgeManager` 并重写 `position()` 方法：
```python
@InfoBadgeManager.register('Custom')
class CustomInfoBadgeManager(InfoBadgeManager):
    """ Custom info badge manager """

    def position(self):
        pos = self.target.geometry().center()
        x = pos.x() - self.badge.width() // 2
        y = self.target.y() - self.badge.height() // 2
        return QPoint(x, y)


# 使用自定义的徽章位置管理器
InfoBadge.success(1, parent=parent, target=button, position="Custom")
```


### [DotInfoBadge](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/info_badge/index.html#qfluentwidgets.components.widgets.info_badge.DotInfoBadge)



`DotInfoBadge` 不显示任何数字或图标，而是显示为一个小圆点，用于表示存在未处理的通知或更新。这个组件在需要提醒用户有新的信息或状态变化，但不需要显示具体数量或类型的情况下非常有用。

```python
DotInfoBadge.info()
DotInfoBadge.success()
DotInfoBadge.attension()
DotInfoBadge.warning()
DotInfoBadge.error()
DotInfoBadge.custom('#005fb8', '#60cdff')
```


### [IconInfoBadge](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/info_badge/index.html#qfluentwidgets.components.widgets.info_badge.IconInfoBadge)



`IconInfoBadge` 在其内部显示一个图标，而不是数字，这个图标可以用来表示特定类型的通知或状态。

```python
IconInfoBadge.info(FluentIcon.ACCEPT_MEDIUM)
IconInfoBadge.success(FluentIcon.ACCEPT_MEDIUM)
IconInfoBadge.attension(FluentIcon.ACCEPT_MEDIUM)
IconInfoBadge.warning(FluentIcon.CANCEL_MEDIUM)
IconInfoBadge.error(FluentIcon.CANCEL_MEDIUM)
```



============================================================
# Components > Status Info > Progress Bar
============================================================
---
title: 进度条
date: 2024-02-27 13:34:00
permalink: /zh/pages/components/progressbar/
---

### [ProgressBar](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/progress_bar/index.html)



`ProgressBar` 用于显示任务进度，用法和 `QProgressBar` 几乎完全相同，但是取消了文本显示功能。

```python
progressBar = ProgressBar()

# 设置取值范围
progressBar.setRange(0, 100)

# 设置当前值
progressBar.setValue(40)
```

`ProgressBar` 可以设置暂停和错误状态，不同状态下进度条的颜色不同：
```python
progressBar.pause()
progressBar.error()
```

恢复运行状态：
```python
bar.resume()
```

自定义进度条的颜色：
```python
progressBar.setCustomBarColor(QColor(255, 0, 0), QColor(0, 255, 110))
```

### [IndeterminateProgressBar](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/progress_bar/index.html#qfluentwidgets.components.widgets.progress_bar.IndeterminateProgressBar)

`IndeterminateProgressBar` 表示一个正在进行但其完成时间未知的长时间运行任务。这种进度条在没有明确的完成时间或进度信息的情况下非常有用，例如在加载或处理大量数据时。

```python
bar = IndeterminateProgressBar(start=True)
```

`IndeterminateProgressBar` 可以设置暂停和错误状态，不同状态下进度条的颜色不同：
```python
bar.pause()
bar.error()
```

恢复运行状态：
```python
bar.resume()
```

自定义进度条的颜色：
```python
progressBar.setCustomBarColor(QColor(255, 0, 0), QColor(0, 255, 110))
```


### [FilledProgressBar](https://qfluentwidgets.com/zh/price)



`FilledProgressBar` 用于显示任务进度。


### [StepProgressBar](https://qfluentwidgets.com/zh/price)



`StepProgressBar` 用于显示分步骤任务进度。


### [TimeLineWidget](https://qfluentwidgets.com/zh/price)



`TimeLineWidget` 用于显示时间线。



============================================================
# Components > Status Info > Progress Button
============================================================
---
title: 进度按钮
date: 2024-02-27 13:34:00
permalink: /zh/pages/components/progressbutton/
---


### [ProgressPushButton](https://qfluentwidgets.com/zh/price)



`ProgressPushButton` 在按钮的基础上增加了进度功能，可以直观地显示操作进度。这种控件常用于需要显示长时间操作进度的场景，如文件下载、数据处理等。



### [IndeterminateProgressPushButton](https://qfluentwidgets.com/zh/price)



`IndeterminateProgressPushButton` 在按钮基础上增加了不确定进度环的功能，适用于无法预知完成时间或进度无法精确计算的操作（如网络请求、后台处理等）。



============================================================
# Components > Status Info > Progress Ring
============================================================
---
title: 进度环
date: 2024-02-27 13:34:00
permalink: /zh/pages/components/progressring/
---

### [ProgressRing](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/progress_ring/index.html#qfluentwidgets.components.widgets.progress_ring.ProgressRing)



`ProgressRing` 是一个环形进度条，可以用来表示处理进度或者用作仪表盘，使用方式和 [ProgressBar](/zh/pages/components/progressbar) 相似。

```python
ring = ProgressRing()

# 设置进度环取值范围和当前值
ring.setRange(0, 100)
ring.setValue(30)

# 显示进度环内文本
ring.setTextVisible(True)

# 调整进度环大小
ring.setFixedSize(80, 80)

# 调整厚度
ring.setStrokeWidth(4)
```

调整进度环的文本格式，比如显示温度：
```python
ring.setFormat("%v℃")
```

### [IndeterminateProgressRing](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/progress_ring/index.html#qfluentwidgets.components.widgets.progress_ring.IndeterminateProgressRing)

`IndeterminateProgressRing` 用于表示应用程序正在进行某项操作，但该操作的完成时间未知。

```python
spinner = IndeterminateProgressRing()

# 调整大小
spinner.setFixedSize(50, 50)

# 调整厚度
spinner.setStrokeWidth(4)
```

### [MultiSegmentProgressRing](https://qfluentwidgets.com/zh/price)



`MultiSegmentProgressRing` 支持分段显示不同进度状态，适用于存储空间可视化等场景。

### [RadialGauge](https://qfluentwidgets.com/zh/price)



`RadialGauge` 可以用来显示一系列的数据，比如速度、进度或者其他可以用角度来表示的度量。



============================================================
# Components > Status Info > Tool Tip
============================================================
---
title: 工具提示
date: 2024-02-27 13:34:00
permalink: /zh/pages/components/tooltip/
---

### [ToolTipFilter](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/tool_tip/index.html#qfluentwidgets.components.widgets.tool_tip.ToolTipFilter)




`ToolTipFilter` 用来将 `QToolTip` 替换成组件库的 `ToolTip`，只要给组件安装上此过滤器即可完成替代。

```python
button = QPushButton('キラキラ')

button.setToolTip('aiko - キラキラ ✨')
button.setToolTipDuration(1000)

# 给按钮安装工具提示过滤器
button.installEventFilter(ToolTipFilter(button, showDelay=300, position=ToolTipPosition.TOP))
```



============================================================
# Components > Menu > Menu
============================================================
---
title: 菜单
date: 2024-02-26 19:56:01
permalink: /zh/pages/components/menu/
---

### [RoundMenu](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/menu/index.html#qfluentwidgets.components.widgets.menu.RoundMenu)



`RoundMenu` 用于提供一系列动作供用户选择，使用方式和 `QMenu` 类似。

::: tip 提示
PyQt/PySide 6.7.0 及以上版本的菜单阴影在 Win11 下显示异常，可将组件库升级到 v1.6.2 来修复此问题，详情参见 [Issue #848](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/848)。
:::

```python
menu = RoundMenu()

# 逐个添加动作，Action 继承自 QAction，接受 FluentIconBase 类型的图标
menu.addAction(Action(FluentIcon.COPY, '复制', triggered=lambda: print("复制成功")))
menu.addAction(Action(FluentIcon.CUT, '剪切', triggered=lambda: print("剪切成功")))

# 批量添加动作
menu.addActions([
    Action(FluentIcon.PASTE, '粘贴'),
    Action(FluentIcon.CANCEL, '撤销')
])

# 添加分割线
menu.addSeparator()

menu.addAction(QAction('全选', shortcut='Ctrl+A'))
```

添加子菜单：

```python
submenu = RoundMenu("添加到", self)

submenu.setIcon(FluentIcon.ADD)
submenu.addActions([
    Action(FluentIcon.VIDEO, '视频'),
    Action(FluentIcon.MUSIC, '音乐'),
])

menu.addMenu(submenu)
```

`RoundMenu` 支持添加自定义组件作为菜单项：



```python
class ProfileCard(QWidget):
    """ Profile card """

    def __init__(self, avatarPath: str, name: str, email: str, parent=None):
        super().__init__(parent=parent)
        self.avatar = AvatarWidget(avatarPath, self)
        self.nameLabel = BodyLabel(name, self)
        self.emailLabel = CaptionLabel(email, self)
        self.logoutButton = HyperlinkButton('https://qfluentwidgets.com/', '注销', self)

        self.emailLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))
        setFont(self.logoutButton, 13)

        self.setFixedSize(307, 82)
        self.avatar.setRadius(24)
        self.avatar.move(2, 6)
        self.nameLabel.move(64, 13)
        self.emailLabel.move(64, 32)
        self.logoutButton.move(52, 48)


class Demo(QWidget):

    def __init__(self):
        super().__init__()

    def contextMenuEvent(self, e) -> None:
        menu = RoundMenu(parent=self)

        # add custom widget
        card = ProfileCard('resource/shoko.png', '硝子酱', 'shokokawaii@outlook.com', menu)
        menu.addWidget(card, selectable=False)

        menu.addSeparator()
        menu.addActions([
            Action(FluentIcon.PEOPLE, '管理账户和设置'),
            Action(FluentIcon.SHOPPING_CART, '支付方式'),
            Action(FluentIcon.CODE, '兑换代码和礼品卡'),
        ])
        menu.addSeparator()
        menu.addAction(Action(FluentIcon.SETTING, '设置'))
        menu.exec(e.globalPos())
```

### [CheckableMenu](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/menu/index.html#qfluentwidgets.components.widgets.menu.CheckableMenu)



`CheckableMenu` 允许用户选中内部的动作，通常与 `QActionGroup` 一起使用。

```python
class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.createTimeAction = Action(FluentIcon.CALENDAR, "创建日期", checkable=True)
        self.shootTimeAction = Action(FluentIcon.CAMERA, "拍摄日期", checkable=True)
        self.modifiedTimeAction = Action(FluentIcon.EDIT, "修改日期", checkable=True)
        self.nameAction = Action(FluentIcon.FONT, "名字", checkable=True)

        self.ascendAction = Action(FluentIcon.UP, "升序", checkable=True)
        self.descendAction = Action(FluentIcon.DOWN, "降序", checkable=True)

        # 将动作添加到动作组
        self.actionGroup1 = QActionGroup(self)
        self.actionGroup1.addAction(self.createTimeAction)
        self.actionGroup1.addAction(self.shootTimeAction)
        self.actionGroup1.addAction(self.modifiedTimeAction)
        self.actionGroup1.addAction(self.nameAction)

        self.actionGroup2 = QActionGroup(self)
        self.actionGroup2.addAction(self.ascendAction)
        self.actionGroup2.addAction(self.descendAction)

        # 选中动作
        self.shootTimeAction.setChecked(True)
        self.ascendAction.setChecked(True)

    def contextMenuEvent(self, e):
        menu = CheckableMenu(parent=self, indicatorType=MenuIndicatorType.RADIO)

        menu.addActions([
            self.createTimeAction, self.shootTimeAction,
            self.modifiedTimeAction, self.nameAction
        ])
        menu.addSeparator()
        menu.addActions([self.ascendAction, self.descendAction])

        menu.exec(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)
```

### [SystemTrayMenu](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/menu/index.html#qfluentwidgets.components.widgets.menu.SystemTrayMenu)

`SystemTrayMenu` 用作系统托盘菜单，与 `QSystemTrayIcon` 一起使用。

```python
class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())

        self.menu = SystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action('🎤   唱'),
            Action('🕺   跳'),
            Action('🤘🏼   RAP'),
            Action('🎶   Music'),
            Action('🏀   篮球', triggered=self.ikun),
        ])
        self.setContextMenu(self.menu)

    def ikun(self):
        print("""巅峰产生虚伪的拥护，黄昏见证真正的使徒 🏀

                       ⠰⢷⢿⠄
                   ⠀⠀⠀⠀⠀⣼⣷⣄
                   ⠀⠀⣤⣿⣇⣿⣿⣧⣿⡄
                   ⢴⠾⠋⠀⠀⠻⣿⣷⣿⣿⡀
                   ⠀⢀⣿⣿⡿⢿⠈⣿
                   ⠀⠀⠀⢠⣿⡿⠁⠀⡊⠀⠙
                   ⠀⠀⠀⢿⣿⠀⠀⠹⣿
                   ⠀⠀⠀⠀⠹⣷⡀⠀⣿⡄
                   ⠀⠀⠀⠀⣀⣼⣿⠀⢈⣧
        """)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.label = QLabel('Right-click system tray icon', self)
        self.layout().addWidget(self.label)

        self.resize(500, 500)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))

        self.systemTrayIcon = SystemTrayIcon(self)
        self.systemTrayIcon.show()

```



============================================================
# Components > Menu > Command Bar
============================================================
---
title: 命令栏
date: 2024-02-26 21:00:00
permalink: /zh/pages/components/commandbar/
---

### [CommandBar](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/command_bar/index.html#qfluentwidgets.components.widgets.command_bar.CommandBar)



`CommandBar` 用于提供水平排列的动作供用户选择，当动作过多以至于视口容纳不下时，`CommandBar` 会自动隐藏超出视口的动作到下拉菜单中。

```python
commandBar = CommandBar()

# 逐个添加动作
commandBar.addAction(Action(FluentIcon.ADD, '添加', triggered=lambda: print("添加")))

# 添加分隔符
commandBar.addSeparator()

# 批量添加动作
commandBar.addActions([
    Action(FluentIcon.EDIT, '编辑', checkable=True, triggered=lambda: print("编辑")),
    Action(FluentIcon.COPY, '复制'),
    Action(FluentIcon.SHARE, '分享'),
])

# 添加始终隐藏的动作
commandBar.addHiddenAction(Action(FluentIcon.SCROLL, '排序', triggered=lambda: print('排序')))
commandBar.addHiddenAction(Action(FluentIcon.SETTING, '设置', shortcut='Ctrl+S'))
```

命令行可以添加自定义组件：

```python
# 创建透明下拉菜单按钮
button = TransparentDropDownPushButton(FluentIcon.MENU, 'Menu')
button.setFixedHeight(34)
setFont(button, 12)

menu = RoundMenu(parent=self)
menu.addActions([
    Action(FluentIcon.COPY, 'Copy'),
    Action(FluentIcon.CUT, 'Cut'),
    Action(FluentIcon.PASTE, 'Paste'),
    Action(FluentIcon.CANCEL, 'Cancel'),
    Action('Select all'),
])
button.setMenu(menu)

# 添加自定义组件
commandBar.addWidget(button)
```

默认情况下 `CommandBar` 只显示动作的图标，如需修改显示模式：
```python
# 图标右侧显示文本
commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

# 图标底部显示文本
commandBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
```

### [CommandBarView](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/command_bar/index.html#qfluentwidgets.components.widgets.command_bar.CommandBarView)




`CommandBarView` 搭配 `Flyout` 一起使用，使用方法和 [CommandBar](#commandbar) 几乎相同。

```python
commandBar = CommandBarView()

commandBar.addAction(Action(FluentIcon.SHARE, 'Share'))
commandBar.addAction(Action(FluentIcon.SAVE, 'Save'))
commandBar.addAction(Action(FluentIcon.DELETE, 'Delete'))

commandBar.addHiddenAction(Action(FluentIcon.APPLICATION, 'App', shortcut='Ctrl+A'))
commandBar.addHiddenAction(Action(FluentIcon.SETTING, 'Settings', shortcut='Ctrl+S'))
commandBar.resizeToSuitableWidth()

target = PushButton("Click Me")
Flyout.make(commandBar, target=target, parent=target, aniType=FlyoutAnimationType.FADE_IN)
```



============================================================
# Components > Layout > Card Widget
============================================================
---
title: 卡片组件
date: 2024-07-24 14:22:00
permalink: /zh/pages/components/cardwidget/
---

### [CardWidget](https://pyqt-fluent-widgets.readthedocs.io/zh_CN/latest/autoapi/qfluentwidgets/components/widgets/card_widget/index.html#qfluentwidgets.components.widgets.card_widget.CardWidget)



`CardWidget` 是一种非常灵活和实用的 UI 设计模式,能够帮助开发者以一种结构化和美观的方式展示各种类型的信息和内容。

卡片组件是一个容器，可用于放置任意组件:

```python
class AppCard(CardWidget):

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.openButton = PushButton('Open', self)
        self.moreButton = TransparentToolButton(FluentIcon.MORE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.openButton.setFixedWidth(120)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignRight)

        self.moreButton.setFixedSize(32, 32)
```

点击 `CardWidget` 会发送 `clicked` 信号:
```python
card = AppCard(
    icon=":/qfluentwidgets/images/logo.png",
    title="PyQt-Fluent-Widgets",
    content="Shokokawaii Inc."
)
card.clicked.connect(lambda: print("点击卡片"))
```

默认圆角大小为 5px，下述代码调整为 8px:
```python
card.setBorderRadius(8)
```

### [SimpleCardWidget](https://pyqt-fluent-widgets.readthedocs.io/zh_CN/latest/autoapi/qfluentwidgets/components/widgets/card_widget/index.html#qfluentwidgets.components.widgets.card_widget.SimpleCardWidget)

`SimpleCardWidget` 是 `CardWidget` 子类，二者之间唯一的区别就是 `SimpleCardWidget` 的背景不会随着鼠标进入进出而变化。

### [ElevatedCardWidget](https://pyqt-fluent-widgets.readthedocs.io/zh_CN/latest/autoapi/qfluentwidgets/components/widgets/card_widget/index.html#qfluentwidgets.components.widgets.card_widget.ElevatedCardWidget)



`ElevatedCardWidget` 是带阴影的卡片组件，鼠标移入时会显示阴影和上移动画。

```python
class EmojiCard(ElevatedCardWidget):

    def __init__(self, iconPath: str, name: str, parent=None):
        super().__init__(parent)
        self.iconWidget = ImageLabel(iconPath, self)
        self.label = CaptionLabel(name, self)

        self.iconWidget.scaledToHeight(68)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignHCenter | Qt.AlignBottom)

        self.setFixedSize(168, 176)
```


### [HeaderCardWidget](https://pyqt-fluent-widgets.readthedocs.io/zh_CN/latest/autoapi/qfluentwidgets/components/widgets/card_widget/index.html#qfluentwidgets.components.widgets.card_widget.HeaderCardWidget)



`HeaderCardWidget` 是带标题的卡片组件，可用于替代 `QGroupBox`。它的内部已有布局，只需将组件添加到水平布局 `viewLayout` 中即可。

```python
class SystemRequirementCard(HeaderCardWidget):
    """ System requirements card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('系统要求')

        self.infoLabel = BodyLabel('此产品适用于你的设备。具有复选标记的项目符合开发人员的系统要求。', self)
        self.successIcon = IconWidget(InfoBarIcon.SUCCESS, self)
        self.detailButton = HyperlinkLabel('详细信息', self)

        self.vBoxLayout = QVBoxLayout()
        self.hBoxLayout = QHBoxLayout()

        self.successIcon.setFixedSize(16, 16)
        self.hBoxLayout.setSpacing(10)
        self.vBoxLayout.setSpacing(16)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.hBoxLayout.addWidget(self.successIcon)
        self.hBoxLayout.addWidget(self.infoLabel)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.detailButton)

        self.viewLayout.addLayout(self.vBoxLayout)
```

### [GroupHeaderCardWidget](https://pyqt-fluent-widgets.readthedocs.io/zh_CN/latest/autoapi/qfluentwidgets/components/widgets/card_widget/index.html#qfluentwidgets.components.widgets.card_widget.GroupHeaderCardWidget)



`GroupHeaderCardWidget` 可用于创建上下分组布局的卡片。可通过 `addGroup()` 添加组件到新分组中，分组存放在垂直布局  `vBoxLayout` 中。

```python
class SettinsCard(GroupHeaderCardWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("基本设置")
        self.setBorderRadius(8)

        self.chooseButton = PushButton("选择")
        self.comboBox = ComboBox()
        self.lineEdit = SearchLineEdit()

        self.hintIcon = IconWidget(InfoBarIcon.INFORMATION)
        self.hintLabel = BodyLabel("点击编译按钮以开始打包 👉")
        self.compileButton = PrimaryPushButton(FluentIcon.PLAY_SOLID, "编译")
        self.openButton = PushButton(FluentIcon.VIEW, "打开")
        self.bottomLayout = QHBoxLayout()

        self.chooseButton.setFixedWidth(120)
        self.lineEdit.setFixedWidth(320)
        self.comboBox.setFixedWidth(320)
        self.comboBox.addItems(["始终显示（首次打包时建议启用）", "始终隐藏"])
        self.lineEdit.setPlaceholderText("输入入口脚本的路径")

        # 设置底部工具栏布局
        self.hintIcon.setFixedSize(16, 16)
        self.bottomLayout.setSpacing(10)
        self.bottomLayout.setContentsMargins(24, 15, 24, 20)
        self.bottomLayout.addWidget(self.hintIcon, 0, Qt.AlignLeft)
        self.bottomLayout.addWidget(self.hintLabel, 0, Qt.AlignLeft)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.openButton, 0, Qt.AlignRight)
        self.bottomLayout.addWidget(self.compileButton, 0, Qt.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignVCenter)

        # 添加组件到分组中
        self.addGroup("resource/Rocket.svg", "构建目录", "选择 Nuitka 的输出目录", self.chooseButton)
        self.addGroup("resource/Joystick.svg", "运行终端", "设置是否显示命令行终端", self.comboBox)
        group = self.addGroup("resource/Python.svg", "入口脚本", "选择软件的入口脚本", self.lineEdit)
        group.setSeparatorVisible(True)

        # 添加底部工具栏
        self.vBoxLayout.addLayout(self.bottomLayout)
```



============================================================
# Components > Layout > Flow Layout
============================================================
---
title: 流式布局
date: 2024-02-26 19:40:01
permalink: /zh/pages/components/flowlayout/
---

### [FlowLayout](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/layout/flow_layout/index.html)



`FlowLayout` 能够自适应视口宽度，在内部组件超出视口宽度时自动换行。

```python
class Demo(QWidget):

    def __init__(self):
        super().__init__()
        layout = FlowLayout(self, needAni=True)  # 启用动画

        # 自定义动画参数
        layout.setAnimation(250, QEasingCurve.OutQuad)

        layout.setContentsMargins(30, 30, 30, 30)
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)

        layout.addWidget(QPushButton('aiko'))
        layout.addWidget(QPushButton('刘静爱'))
        layout.addWidget(QPushButton('柳井爱子'))
        layout.addWidget(QPushButton('aiko 赛高'))
        layout.addWidget(QPushButton('aiko 太爱啦😘'))

        self.resize(250, 300)
```

在某些情况下，流式布局中的组件可能发生重叠，可使用下述方法强制刷新布局：
```python
# 移除全部组件
flowLayout.removeAllWidgets()

# 重新添加组件
for w in widgets:
    flowLayout.addWidget(w)
```


### [WaterfallLayout](https://qfluentwidgets.com/zh/price)



`WaterfallLayout` 一种多列等宽不等高的页面布局方式。



============================================================
# Components > Settings > Setting Card
============================================================
---
title: 设置卡
date: 2024-03-21 23:31:00
permalink: /zh/pages/components/settingcard/
---

QFluentWidgets 将每个配置项表示为界面的一个设置卡。用户在设置卡上的交互行为将会改变相应配置项的值。

### [SettingCard](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/settings/setting_card/index.html#qfluentwidgets.components.settings.setting_card.SettingCard)

设置卡基类，内部包含图标、标题和内容，可在 `hBoxLayout` 中插入组件来自定义设置卡。

设置卡子类都实现了 `setValue(value)` 函数来改变配置项的值。


### [ComboBoxSettingCard](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/settings/setting_card/index.html#qfluentwidgets.components.settings.setting_card.ComboBoxSettingCard)



下拉选项设置卡，用于操作列表选项类型的配置项。

```python
class Config(QConfig):
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)

cfg = Config()
qconfig.load("config.json", cfg)

card = ComboBoxSettingCard(
    configItem=cfg.dpiScale,
    icon=FluentIcon.ZOOM,
    title="界面缩放",
    content="调整组件和字体的大小",
    texts=["100%", "125%", "150%", "175%", "200%", "跟随系统设置"]
)

cfg.dpiScale.valueChanged.connect(print)
```

### [OptionsSettingCard](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/settings/setting_card/index.html#qfluentwidgets.components.settings.setting_card.OptionsSettingCard)



选项设置卡，用于操作列表选项类型的配置项，当前选项改变时发出 `optionChanged(item: OptionsConfigItem)` 信号。

```python
card = OptionsSettingCard(
    qconfig.themeMode,
    FluentIcon.BRUSH,
    "应用主题",
    "调整你的应用外观",
    texts=["浅色", "深色", "跟随系统设置"]
)
```

### [FolderListSettingCard](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/settings/folder_list_setting_card/index.html)



文件夹列表设置卡，用于操作文件夹列表配置项，当选中的文件夹改变时发出 `folderChanged(folders: List[str])` 信号。

```python
class Config(QConfig):
    ConfigItem("Folders", "LocalMusic", [], FolderListValidator())

cfg = Config()
qconfig.load("config.json", cfg)

card = FolderListSettingCard(
    cfg.musicFolders,
    "本地音乐库",
    directory=QStandardPaths.writableLocation(QStandardPaths.MusicLocation),
    parent=self.musicInThisPCGroup
)
```


### [RangeSettingCard](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/settings/setting_card/index.html#qfluentwidgets.components.settings.setting_card.RangeSettingCard)



范围设置卡，用于操作数值范围的配置项，当前选项改变时发出 `valueChanged(value: int)` 信号。

```python
class Config(QConfig):
    onlinePageSize = RangeConfigItem("Online", "PageSize", 30, RangeValidator(0, 50))

cfg = Config()
qconfig.load("config.json", cfg)

card = RangeSettingCard(
    cfg.onlinePageSize,
    Fluent.MUSIC,
    title="分页大小",
    content="每页显示的在线歌曲数量"
)
```


### [SwitchSettingCard](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/settings/setting_card/index.html#qfluentwidgets.components.settings.setting_card.SwitchSettingCard)



开关设置卡，用于操作布尔类型的配置项，选择状态改变时发出 `checkedChanged(isChecked: bool)` 信号。

```python
class Config(QConfig):
    enableAcrylicBackground = ConfigItem("MainWindow", "EnableAcrylicBackground", False, BoolValidator())

cfg = Config()
qconfig.load("config.json", cfg)

card = SwitchSettingCard(
    icon=FluentIcon.TRANSPARENT,
    title="启用亚克力效果",
    content="亚克力效果的视觉体验更好，但是可能导致窗口卡顿",
    configItem=cfg.enableAcrylicBackground
)
```


### [HyperlinkCard](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/settings/setting_card/index.html#qfluentwidgets.components.settings.setting_card.HyperlinkCard)



超链接设置卡，点击右侧按钮时可自动跳转到指定 URL。

```python
card = HyperlinkCard(
    url="https://qfluentwidgets.com",
    text="打开帮助页面",
    icon=FluentIcon.HELP,
    title="帮助",
    content="发现 PyQt-Fluent-Widgets 的最佳实践"
)
```


### [PushSettingCard](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/settings/setting_card/index.html#qfluentwidgets.components.settings.setting_card.PushSettingCard)



按钮设置卡，点击右侧按钮时会发送 `clicked()` 信号。

```python
card = PushSettingCard(
    text="选择文件夹",
    icon=FluentIcon.DOWNLOAD,
    title="下载目录",
    content="D:/Users/下载"
)
```


### [PrimaryPushSettingCard](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/settings/setting_card/index.html#qfluentwidgets.components.settings.setting_card.PrimaryPushSettingCard)



主题色按钮设置卡，点击右侧按钮时会发送 `clicked()` 信号。

```python
card = PrimaryPushSettingCard(
    text="选择文件夹",
    icon=FluentIcon.DOWNLOAD,
    title="下载目录",
    content="D:/Users/下载"
)
```

### [ExpandGroupSettingCard](https://pyqt-fluent-widgets.readthedocs.io/en/latest/autoapi/qfluentwidgets/components/settings/expand_setting_card/index.html#qfluentwidgets.components.settings.expand_setting_card.ExpandGroupSettingCard)



手风琴设置组卡片，可添加多组配置项，每组用分隔符隔开，调用 `addGroupWidget(widget)` 即可添加一组配置项到卡片中。

```python
class PowerSettingCard(ExpandGroupSettingCard):

    def __init__(self, parent=None):
        super().__init__(FluentIcon.SPEED_OFF, "节电模式", "通过限制某些通知和后台活动降低电池消耗", parent)

        # 第一组
        self.modeButton = PushButton("立即启用")
        self.modeButton.setFixedWidth(135)

        # 第二组
        self.autoComboBox = ComboBox()
        self.autoComboBox.addItems(["10%", "20%", "30%"])
        self.autoComboBox.setFixedWidth(135)

        # 第三组
        self.lightnessSwitchButton = SwitchButton("关", self, IndicatorPosition.RIGHT)
        self.lightnessSwitchButton.setOnText("开")

        # 调整内部布局
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(0)

        # 添加各组到设置卡中
        self.addGroup(FluentIcon.POWER_BUTTON, "节电模式", "延长电脑续航时间", self.modeButton)
        self.addGroup(FluentIcon.RINGER, "自动开启节电模式", "电量较低时自动开启此模式", self.autoComboBox)
        self.addGroup(FluentIcon.BRIGHTNESS, "使用节电模式时屏幕亮度较低", "", self.lightnessSwitchButton)
```

下面是一个动态删减手风琴设置卡内部组件的例子：

```python
class ServerCard(ExpandGroupSettingCard):

    def __init__(self, parent=None):
        super().__init__(FluentIcon.SHARE, "服务器", "配置流媒体服务器", parent)
        self.addButton = PrimaryPushButton(FluentIcon.ADD, "添加服务器")
        self.addWidget(self.addButton)
        self.addButton.clicked.connect(self.addServerCard)

    def addServerCard(self):
        item = ServerItem(self)
        item.removeButton.clicked.connect(lambda: self.removeServerCard(item))
        self.addGroupWidget(item)

    def removeServerCard(self, card):
        self.removeGroupWidget(card)
        card.hide()
        card.deleteLater()


class ServerItem(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.addButton = PrimaryToolButton(FluentIcon.EDIT, self)
        self.removeButton = ToolButton(FluentIcon.DELETE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(BodyLabel("服务器"))
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.addButton)
        self.hBoxLayout.addWidget(self.removeButton)

        self.hBoxLayout.setContentsMargins(20, 12, 20, 12)

```

如果无法正常展开手风琴设置卡，请换成 `SimpleExpandGroupSettingCard`。


### [SettingCardGroup](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/settings/setting_card_group/index.html)

可以通过 `SettingCardGroup.addSettingCard()` 将多个设置卡添加到同一个组中，`SettingCardGroup` 会根据设置卡的高度自动调整自己的布局。



============================================================
# Components > Settings > Config
============================================================
---
title: 配置类
date: 2024-03-21 23:31:00
permalink: /zh/pages/components/config/
---


## 设计原理
`ConfigItem` 类表示一个配置项，配置类 `QConfig` 类用于读写配置项的值。当 `ConfigItem` 的值发生改变时会发送 `valueChanged(value: object)` 信号，`QConfig` 类也会自动将配置值同步到 json 配置文件中。

配置文件可能被用户篡改，导致配置项的值非法，所以 QFluentWidgets 使用 `ConfigValidator` 类及其子类来验证和修正配置项的值。

json 文件只支持字符串、布尔值、列表和字典，对于枚举类或者 `QColor`，无法直接将它们的值写入 json 文件中。为了解决这个问题，QFluentWidgets 提供了 `ConfigSerializer` 类及其子类来序列化和反序列化配置项。举个栗子，可以使用 `ColorSerializer` 来序列化值类型为 `QColor` 的配置项。

`ConfigItem` 的属性如下表所示，各个子类的构造函数见 [API 文档](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/common/config/index.html#qfluentwidgets.common.config.ConfigItem)：

| 属性         | 数据类型           | 描述                                         |
| ------------ | ------------------ | -------------------------------------------- |
| `group`      | `str`              | 配置项所属的组别                             |
| `name`       | `str`              | 配置项的名字                                 |
| `default`    | `Any`              | 配置项的默认值，当配置值非法时将被默认值替代 |
| `validator`  | `ConfigValidator`  | 配置校验器                                   |
| `serializer` | `ConfigSerializer` | 配置序列化器                                 |
| `restart`    | `bool`             | 配置更新后是否重启应用                       |


## 使用方式
可通过下述步骤创建并使用自定义配置类 `MyConfig`：

1. 继承 `QConfig`
2. 将 `ConfigItem` 实例添加到 `MyConfig` 的类属性中
3. 创建全局唯一的 `MyConfig` 单例 `cfg`
4. 调用 `qconfig.load("/path/to/config.json", cfg)` 加载配置文件
5. 使用 `cfg.get(cfg.xxx)` 读取配置值，`cfg.set(cfg.xxx, value)` 写入配置值

下面是一个简单的例子：

```python
from enum import Enum

from qfluentwidgets import *


class MvQuality(Enum):
    """ MV quality enumeration class """

    FULL_HD = "Full HD"
    HD = "HD"
    SD = "SD"
    LD = "LD"

    @staticmethod
    def values():
        return [q.value for q in MvQuality]


class MyConfig(QConfig):
    """ Config of application """

    # main window
    enableAcrylic = ConfigItem("MainWindow", "EnableAcrylic", False, BoolValidator())
    playBarColor = ColorConfigItem("MainWindow", "PlayBarColor", "#225C7F")
    themeMode = OptionsConfigItem("MainWindow", "ThemeMode", "Light", OptionsValidator(["Light", "Dark", "Auto"]), restart=True)
    recentPlaysNumber = RangeConfigItem("MainWindow", "RecentPlayNumbers", 300, RangeValidator(10, 300))

    # online
    onlineMvQuality = OptionsConfigItem("Online", "MvQuality", MvQuality.FULL_HD, OptionsValidator(MvQuality), EnumSerializer(MvQuality))


# 创建配置实例并使用配置文件来初始化它
cfg = MyConfig()
qconfig.load('config/config.json', cfg)
```



============================================================
# Components > Date Time > Date Picker
============================================================
---
title: 日期选择器
date: 2024-02-26 12:32:01
permalink: /zh/pages/components/datepicker/
---

### [DatePicker](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/date_time/date_picker/index.html#qfluentwidgets.components.date_time.date_picker.DatePicker)



`DatePicker` 用于选择日期，当选择的日期发生改变时会发送 `dateChanged` 信号。

```python
datePicker = DatePicker()

# 设置当前日期
datePicker.setDate(QDate(2024, 2, 26))

# 获取当前日期
print(datePicker.date)

# 日期发生改变
datePicker.dateChanged.connect(lambda date: print(date.toString()))
```

可通过继承 `PickerColumnFormatter` 的方式来修改 `DatePicker` 每一列的格式：
```python
class MonthFormatter(PickerColumnFormatter):
    """ Month formatter """

    def encode(self, value):
        # 此处 value 的取值范围为 1-12
        return str(value) + "😊"

    def decode(self, value: str):
        return int(value[:-1])


# 使用自定义的月格式（第一列）
datePicker.setColumnFormatter(0, MonthFormatter())
```

### [ZhDatePicker](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/date_time/date_picker/index.html#qfluentwidgets.components.date_time.date_picker.ZhDatePicker)



`ZhDatePicker` 用于选择中文格式的日期，使用方法与 [DatePicker](#datepicker) 相同。



============================================================
# Components > Date Time > Time Picker
============================================================
---
title: 时间选择器
date: 2024-02-26 13:45:01
permalink: /zh/pages/components/timepicker/
---

### [TimePicker](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/date_time/time_picker/index.html#qfluentwidgets.components.date_time.time_picker.TimePicker)



`TimePicker` 用于选择 24 小时制的时间，当选择的时间发生改变时会发送 `timeChanged` 信号。

```python
timePicker = TimePicker()

# 设置当前时间
timePicker.setTime(QTime(13, 53, 26))

# 获取当前时间
print(timePicker.time)

# 时间发生改变
timePicker.timeChanged.connect(lambda time: print(time.toString()))
```

可通过继承 `PickerColumnFormatter` 的方式来修改 `TimePicker` 每一列的格式：
```python
class SecondsFormatter(PickerColumnFormatter):
    """ Seconds formatter """

    def encode(self, value):
        return str(value) + "秒"

    def decode(self, value: str):
        return int(value[:-1])


# 使用自定义的秒格式（第三列）
timePicker.setColumnFormatter(2, SecondsFormatter())
```

如果想显示或隐藏某一列：
```python
timePicker.setColumnVisible(0, False)   # 隐藏小时
timePicker.setColumnVisible(1, False)   # 隐藏分钟
timePicker.setColumnVisible(2, True)    # 显示秒
```

### [AMTimePicker](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/date_time/time_picker/index.html#qfluentwidgets.components.date_time.time_picker.AMTimePicker)



`AMTimePicker` 用于选择 AM/PM 小时制的时间，使用方式和 [TimePicker](#timepicker) 相同。



============================================================
# Components > Date Time > Calandar Picker
============================================================
---
title: 日历选择器
date: 2024-02-26 14:08:01
permalink: /zh/pages/components/calendarpicker/
---

### [CalendarPicker](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/date_time/calendar_picker/index.html#qfluentwidgets.components.date_time.calendar_picker.CalendarPicker)



`CalendarPicker` 用于选择日期，当选择的日期发生改变时会发送 `dateChanged` 信号。

```python
calendarPicker = CalendarPicker()

# 设置当前日期
calendarPicker.setDate(QDate(2024, 2, 26))

# 获取当前日期
print(calendarPicker.date)

# 日期发生改变
calendarPicker.dateChanged.connect(lambda date: print(date.toString()))
```

设置日期格式：

```python
calendarPicker.setDateFormat(Qt.TextDate)
calendarPicker.setDateFormat('yyyy-M-d')
```

### [FastCalendarPicker](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/date_time/calendar_picker/index.html#qfluentwidgets.components.date_time.calendar_picker.FastCalendarPicker)



`FastCalendarPicker` 用法和 [CalendarPicker](#calendarpicker) 完全一致，但是弹出速度更快，内存占用更小。

### [RangeCalendarPicker](https://qfluentwidgets.com/zh/price)



`RangeCalendarPicker` 用于选择日期范围。



============================================================
# Components > View > List View
============================================================
---
title: 列表控件
date: 2024-02-27 20:23:00
permalink: /zh/pages/components/listview/
---

### [ListWidget](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/list_view/index.html#qfluentwidgets.components.widgets.list_view.ListWidget)



`ListWidget` 提供了一个列表，用户可以在这个列表中选择一个或多个项，这个类的用法和 `QListWidget` 完全相同。

```python
listWidget = ListWidget()

stands = [
    '白金之星', '绿色法皇', "天堂制造", "绯红之王",
    '银色战车', '疯狂钻石', "壮烈成仁", "败者食尘",
    "隐者之紫", "黄金体验", "虚无之王", "纸月之王",
    "骇人恶兽", "男子领域", "华丽挚爱", "牙 Act 4",
    "铁球破坏者", "性感手枪", 'D4C • 爱之列车', "天生完美",
    "软又湿", "佩斯利公园", "奇迹于你", "行走的心",
    "护霜旅行者", "十一月雨", "调情圣手", "片刻静候"
]

# 添加列表项
for stand in stands:
    item = QListWidgetItem(stand)
    item.setIcon(QIcon(':/qfluentwidgets/images/logo.png'))
    listWidget.addItem(item)
```

默认情况下，右键单击某个列表项时不会更新该列的选中状态，如需立即选中可调用下述方法：
```python
listWidget.setSelectRightClickedRow(True)
```

### [ListView](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/list_view/index.html#qfluentwidgets.components.widgets.list_view.ListView)

`ListView` 用于展示模型中的数据，使用方法和 `QListView` 完全相同。


### [RoundListWidget](https://qfluentwidgets.com/zh/price)



`RoundListWidget` 用法和 `QListWidget` 完全相同。


### [RoundListView](https://qfluentwidgets.com/zh/price)

`RoundListView` 用法和 `QListWidget` 完全相同。



============================================================
# Components > View > Table View
============================================================
---
title: 表格控件
date: 2024-02-27 20:23:00
permalink: /zh/pages/components/tableview/
---

### [TableWidget](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/table_view/index.html#qfluentwidgets.components.widgets.table_view.TableWidget)



`TableWidget` 提供了一个表格视图，用户可以在这个表格中查看和编辑数据。这个组件通常用于展示和编辑结构化的数据，例如一个电子表格或者一个数据库的查询结果。这个类的使用方式和 `QTableWidget` 完全相同。

```python
table = TableWidget(self)

# 启用边框并设置圆角
table.setBorderVisible(True)
table.setBorderRadius(8)

table.setWordWrap(False)
table.setRowCount(3)
table.setColumnCount(5)

# 添加表格数据
songInfos = [
    ['シアワセ', 'aiko', '秘密', '2008', '5:25'],
    ['なんでもないや', 'RADWIMPS', '君の名は。', '2016', '3:16'],
    ['恋をしたのは', 'aiko', '恋をしたのは', '2016', '6:02'],
]
for i, songInfo in enumerate(songInfos):
    for j in range(5):
        table.setItem(i, j, QTableWidgetItem(songInfo[j]))

# 设置水平表头并隐藏垂直表头
table.setHorizontalHeaderLabels(['Title', 'Artist', 'Album', 'Year', 'Duration'])
table.verticalHeader().hide()
```

默认情况下，右键单击某个列表项时不会更新该列的选中状态，如需立即选中可调用下述方法：
```python
table.setSelectRightClickedRow(True)
```

当显示器的分辨率较高时，平滑滚动可能导致表格卡顿，这时候可以禁用平滑滚动：

```python
table.scrollDelagate.verticalSmoothScroll.setSmoothMode(SmoothMode.NO_SMOOTH)
```



### [TableView](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/table_view/index.html#qfluentwidgets.components.widgets.table_view.TableView)

`TableView` 使用方法和 `QTableView` 完全相同。


### [RoundTableWidget](https://qfluentwidgets.com/zh/price)



`RoundTableWidget` 用法和 `QTableWidget` 完全相同。


### [RoundTableView](https://qfluentwidgets.com/zh/price)

`RoundTableView` 用法和 `QTabelView` 完全相同。


### [LineTableWidget](https://qfluentwidgets.com/zh/price)



`LineTableWidget` 用法和 `QTableWidget` 完全相同。


### [LineTableView](https://qfluentwidgets.com/zh/price)

`LineTableView` 用法和 `QTabelView` 完全相同。



============================================================
# Components > View > Tree View
============================================================
---
title: 树状控件
date: 2024-02-27 21:07:00
permalink: /zh/pages/components/treeview/
---

### [TreeWidget](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/tree_view/index.html#qfluentwidgets.components.widgets.tree_view.TreeWidget)



`TreeWidget` 用于展示具有父子关系的数据，使用方法和 `QTreeWidget` 完全相同。

```python
tree = TreeWidget()

# 添加子树
item1 = QTreeWidgetItem(['JoJo 1 - Phantom Blood'])
item1.addChildren([
    QTreeWidgetItem(['Jonathan Joestar']),
    QTreeWidgetItem(['Dio Brando']),
])
tree.addTopLevelItem(item1)

# 添加子树
item2 = QTreeWidgetItem(['JoJo 3 - Stardust Crusaders'])
item21 = QTreeWidgetItem(['Jotaro Kujo'])
item21.addChildren([
    QTreeWidgetItem(['空条承太郎']),
    QTreeWidgetItem(['空条蕉太狼']),
])
item2.addChild(item21)
tree.addTopLevelItem(item2)

# 隐藏表头
tree.setHeaderHidden(True)
tree.setFixedSize(300, 380)
```

当显示器的分辨率较高时，平滑滚动可能导致卡顿，这时候可以禁用平滑滚动：

```python
tree.scrollDelagate.verticalSmoothScroll.setSmoothMode(SmoothMode.NO_SMOOTH)
```


### [TreeView](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/tree_view/index.html#qfluentwidgets.components.widgets.tree_view.TreeView)

`TreeView` 用于展示具有父子关系的数据，使用方法和 `QTreeView` 完全相同。



============================================================
# Components > View > Flip View
============================================================
---
title: 翻转视图
date: 2024-02-27 19:35:00
permalink: /zh/pages/components/flipview/
---

### [FlipView](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/flip_view/index.html#qfluentwidgets.components.widgets.flip_view.FlipView)



`FlipView` 组件非常适合在需要展示一组图片的场景中使用，可以用于实现一个图片查看器，用户可以通过翻页来查看每一张图片。

```python
flipView = HorizontalFlipView()

# 添加图片
flipView.addImages(["image1.png", "image2.png"])

# 监听当前页码改变信号
flipView.currentIndexChanged.connect(lambda index: print("当前页面：", index))
```

默认情况下 `FlipView` 通过拉伸强制所有图片统一大小，可以设置缩放策略来保持图片的宽高比：
```python
flipView.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
```

`FlipView` 的视口和图片的默认大小为 480×270，调整大小的方式如下：
```python
flipView.setItemSize(QSize(320, 180))
flipView.setFixedSize(QSize(320, 180))
```

通过添加图片间距和调整视口宽度，可以实现下述效果的翻转视图：



```python
flipView.setFixedSize(QSize(710, 270))
flipView.setSpacing(15)

# 启用圆角
flipView.setBorderRadius(15)
```


### [FlipImageDelegate](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/flip_view/index.html#qfluentwidgets.components.widgets.flip_view.FlipImageDelegate)



`FlipImageDelegate` 用于控制 `FlipView` 的绘制结果：

```python
class CustomFlipItemDelegate(FlipImageDelegate):
    """ Custom flip item delegate """

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        super().paint(painter, option, index)
        painter.save()

        # draw mask
        painter.setBrush(QColor(255, 255, 255, 200))
        painter.setPen(Qt.NoPen)
        rect = option.rect
        rect = QRect(rect.x(), rect.y(), 200, rect.height())
        painter.drawRect(rect)

        # draw text
        painter.setPen(Qt.black)
        painter.setFont(getFont(16, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, '🥰\n硝子酱一级棒卡哇伊')

        painter.restore()


# 使用自定义代理
flipView.setItemDelegate(CustomFlipItemDelegate(flipView))
```



============================================================
# Components > Scroll > Scroll Area
============================================================
---
title: 滚动区域
date: 2024-02-27 10:45:00
permalink: /zh/pages/components/scrollarea/
---

### [SingleDirectionScrollArea](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/scroll_area/index.html#qfluentwidgets.components.widgets.scroll_area.SingleDirectionScrollArea)

`SingleDirectionScrollArea` 实现了单方向的平滑滚动，当竖直方向或者水平方向有太多数据需要展示时，可使用此组件。

竖直方向：
```python
scrollArea = SingleDirectionScrollArea(orient=Qt.Vertical)
scrollArea.resize(200, 400)

# 竖直方向有很多组件
view = QWidget()
layout = QVBoxLayout(view)
for i in range(1, 100):
    layout.addWidget(QPushButton(f"按钮 {i}"))

scrollArea.setWidget(view)
```

水平方向：
```python
scrollArea = SingleDirectionScrollArea(orient=Qt.Horizontal)
scrollArea.resize(400, 150)

# 水平方向有很多组件
view = QWidget()
layout = QHBoxLayout(view)
for i in range(1, 100):
    layout.addWidget(QPushButton(f"按钮 {i}"))

scrollArea.setWidget(view)
```

默认情况下滚动区域的背景和边框不透明，如需改为透明背景并移除边框：
```python
scrollArea.setStyleSheet("QScrollArea{background: transparent; border: none}")

# 必须给内部的视图也加上透明背景样式
view.setStyleSheet("QWidget{background: transparent}")
```

也可以调用内置方法修改为透明背景，注意此方法需要在 `scrollArea.setWidget(view)` 之后调用才会生效：

```python
scrollArea.enableTransparentBackground()
```

### [ScrollArea](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/scroll_area/index.html#qfluentwidgets.components.widgets.scroll_area.ScrollArea)

`ScrollArea` 实现了水平和竖直方向的平滑滚动，使用方式和 `QScrollArea` 完全相同。

### [ScrollArea](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/scroll_area/index.html#qfluentwidgets.components.widgets.scroll_area.ScrollArea)

`ScrollArea` 实现了水平和竖直方向的平滑滚动，使用方式和 `QScrollArea` 完全相同。

在某些情况下平滑滚动可能导致界面卡顿，取消平滑滚动的方法如下：
```python
scrollArea.setSmoothMode(SmoothMode.NO_SMOOTH)
```

### [SmoothScrollArea](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/scroll_area/index.html#qfluentwidgets.components.widgets.scroll_area.SmoothScrollArea)

`SmoothScrollArea` 使用 `QPropertyAnimation` 实现了水平和竖直方向的平滑滚动，使用方式和 `QScrollArea` 完全相同。

```python
class Demo(SmoothScrollArea):

    def __init__(self):
        super().__init__()
        # 加载一张分辨率很高的图片
        self.label = ImageLabel("path/to/image.png")

        # 自定义平滑滚动动画
        self.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.setScrollAnimation(Qt.Horizontal, 400, QEasingCurve.OutQuint)

        # 滚动到指定区域
        self.horizontalScrollBar().setValue(1900)

        self.setWidget(self.label)
        self.resize(1200, 800)
```



============================================================
# Components > Scroll > Pager
============================================================
---
title: 分页器
date: 2024-02-27 11:25:00
permalink: /zh/pages/components/pager/
---

### [PipsPager](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/components/widgets/pips_pager/index.html#qfluentwidgets.components.widgets.pips_pager.PipsPager)



`PipsPager` 是一种轻量的分页组件，控件上的每个圆点代表一个页面。这个控件在一些需要页面切换的场景下非常有用，例如图片轮播器或用户向导界面。

```python
pager = PipsPager(Qt.Horizontal)

# 设置页数
pager.setPageNumber(15)

# 设置圆点数量
pager.setVisibleNumber(8)

# 始终显示前进和后退按钮
pager.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)
pager.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)

# 设置当前页码
pager.setCurrentIndex(3)
```

当前页码发生改变时会发出信号 `currentIndexChanged(index: int)`：
```python
pager.currentIndexChanged.connect(lambda index: print(index, pager.currentIndex()))
```

### [Pager](https://qfluentwidgets.com/zh/price)



`Pager` 提供了分页功能，当数据量过多时，使用分页分解数据。




============================================================
# Components > Media > Media Play Bar
============================================================
---
title: 媒体播放栏
date: 2024-03-31 14:08:00
permalink: /zh/pages/components/mediaplaybar/
---

## [SimpleMediaPlayBar](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/multimedia/index.html#qfluentwidgets.multimedia.SimpleMediaPlayBar)



简易媒体播放栏，包含播放按钮、进度条和音量按钮，。

::: tip 提示
PyQt/PySide 6.5.0 及以上版本不需要额外安装解码器，低版本需要安装 LAV Filters（Windows）或者 GStreamer（Linux）。
:::

### 播放音乐
媒体播放栏支持本地和在线音乐，下面是一个简单的例子：

```python
from qfluentwidgets.multimedia import SimpleMediaPlayBar

bar = SimpleMediaPlayBar()

# 在线音乐
url = QUrl("https://files.cnblogs.com/files/blogs/677826/beat.zip?t=1693900324")
bar.player.setSource(url)

# 本地音乐
url = QUrl.fromLocalFile(str(Path("resource/aiko - beat.flac").absolute()))
bar.player.setSource(url)
```

调用下述方法可以改变播放状态：
* `pause()`：暂停播放
* `play()`：继续播放
* `stop()`：结束播放
* `togglePlayState()`：开始/暂停播放
* `setPosition()`：设置播放进度
* `setVolume()`：设置音量

这些方法只是对内部播放器 `player` 的封装，更细粒度的控制方法请查阅 [MediaPlayer](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/multimedia/media_player/index.html#) 的 API 文档。

### 自定义布局
简易媒体播放栏内部为水平布局 `hBoxLayout`，可添加自定义按钮：
```python
from qfluentwidgets import FluentIcon
from qfluentwidgets.multimedia import MediaPlayBarButton

bar.hBoxLayout.addWidget(MediaPlayBarButton(FluentIcon.FULL_SCREEN))
```

## [StandardMediaPlayBar](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/multimedia/index.html#qfluentwidgets.multimedia.StandardMediaPlayBar)



标准媒体播放栏，包含播放按钮、前进后退按钮、进度条和音量按钮，使用方式和 [SimpleMediaPlayBar](#simplemediaplaybar) 几乎一致。

下面是一个简单的例子：

```python
from qfluentwidgets.multimedia import StandardMediaPlayBar

bar = StandardMediaPlayBar()

# 在线音乐
url = QUrl("https://files.cnblogs.com/files/blogs/677826/beat.zip?t=1693900324")
bar.player.setSource(url)

# 本地音乐
url = QUrl.fromLocalFile(str(Path("resource/aiko - beat.flac").absolute()))
bar.player.setSource(url)
```

`StandardMediaPlayBar` 的布局如下图所示：



总布局为垂直布局 `vBoxLayout`，内部包含三个按钮布局，可在各个布局中添加自定义按钮或组件。



============================================================
# Components > Media > Video Widget
============================================================
---
title: 视频播放器
date: 2024-03-31 14:08:00
permalink: /zh/pages/components/videowidget/
---

### [VideoWidget](https://pyqt-fluent-widgets.readthedocs.io/zh-cn/latest/autoapi/qfluentwidgets/multimedia/video_widget/index.html#qfluentwidgets.multimedia.video_widget.VideoWidget)



`VideoWidget` 用于播放本地或者在线视频，自带播放栏。

::: tip 提示
PyQt/PySide 6.5.0 及以上版本不需要额外安装解码器，低版本需要安装 LAV Filters（Windows）或者 GStreamer（Linux）。
:::

使用方式较为简单：

```python
from qfluentwidgets.multimedia import VideoWidget

videoWidget = VideoWidget(self)

videoWidget.setVideo(QUrl.fromLocalFile("D:/Video/aiko - シアワセ.mp4"))
videoWidget.play()
```



============================================================
# Components > System > File Picker
============================================================
---
title: 文件选择器
date: 2024-03-05 23:14:01
permalink: /zh/pages/components/filepicker/
---

### [DropSingleFileWidget](https://qfluentwidgets.com/zh/price)



`DropSingleFileWidget` 可拖拽或打开文件对话框来选择指定格式的文件。


### [DropMultiFilesWidget](https://qfluentwidgets.com/zh/price)



`DropMultiFilesWidget` 可拖拽或打开文件对话框来选择指定格式的多个文件。



============================================================
# Components > System > Folder Picker
============================================================
---
title: 文件夹选择器
date: 2024-03-05 23:14:01
permalink: /zh/pages/components/folderpicker/
---

### [DropSingleFolderWidget](https://qfluentwidgets.com/zh/price)



`DropSingleFolderWidget` 可拖拽或打开文件对话框来选择一个文件夹。


### [DropMultiFoldersWidget](https://qfluentwidgets.com/zh/price)



`DropMultiFoldersWidget` 可拖拽或打开文件对话框来选择多个文件夹。



============================================================
# Components > Chart > Chart Widget
============================================================
---
title: 图表组件
date: 2024-03-13 13:25:01
permalink: /zh/pages/components/chartwidget/
---

### [ChartWidget](https://qfluentwidgets.com/zh/price)



`ChartWidget` 无缝衔接 ECharts 图表库，提供开箱即用的 20 多种图表，并且支持各种图表的任意组合。既可以直接传入图表配置，也可以使用 pyecharts 面向对象的写法来创建图表，十分方便。

