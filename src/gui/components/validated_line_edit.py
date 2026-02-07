# coding:utf-8
from typing import Optional, List
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import LineEdit, InfoBar
from src.common.validators.base import BaseValidator


class ValidatedLineEdit(LineEdit):
    """
    集成校验逻辑的增强型 LineEdit
    """

    # 校验状态改变信号 (is_valid, error_message)
    validationChanged = Signal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.validators: List[BaseValidator] = []
        self._is_valid = True
        self._error_message = ""
        self._auto_normalize = True

        # 连接信号
        self.textChanged.connect(self._on_text_changed)
        self.editingFinished.connect(self._on_editing_finished)

    def addValidator(self, validator: BaseValidator):
        """ 添加校验器 """
        self.validators.append(validator)
        return self

    def setAutoNormalize(self, auto: bool):
        """ 设置是否在失焦时自动标准化 """
        self._auto_normalize = auto
        return self

    def _on_text_changed(self, text: str):
        """ 文本改变时进行实时验证 (轻量级验证) """
        self.validate(silent=True)

    def _on_editing_finished(self):
        """ 结束编辑时进行完整验证和标准化 """
        if self._auto_normalize:
            text = self.text()
            normalized_text = text
            for v in self.validators:
                normalized_text = v.normalize(normalized_text)

            if normalized_text != text:
                self.setText(normalized_text)

        self.validate(silent=False)

    def validate(self, silent: bool = False) -> bool:
        """
        执行验证

        Args:
            silent: 是否静默验证 (不弹出提示)
        """
        text = self.text()
        is_valid = True
        error_msg = ""

        for v in self.validators:
            valid, msg = v.validate(text)
            if not valid:
                is_valid = False
                error_msg = msg
                break

        self._is_valid = is_valid
        self._error_message = error_msg

        # 更新 UI 状态 - 使用 QFluentWidgets 官方方法
        self.setError(not is_valid)

        # 发送信号
        self.validationChanged.emit(is_valid, error_msg)

        # 如果不是静默模式且验证失败，显示提示
        if not silent and not is_valid:
            self._show_error_tip(error_msg)

        return is_valid

    def _show_error_tip(self, message: str):
        """ 显示错误提示 """
        InfoBar.warning(
            title='输入验证',
            content=message,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position='TopCenter',
            duration=2000,
            parent=self.window()
        )

    def get_validated_value(self) -> str:
        """ 获取标准化后的值 """
        text = self.text()
        for v in self.validators:
            text = v.normalize(text)
        return text

    def is_valid(self) -> bool:
        """ 返回当前是否有效 """
        return self._is_valid
