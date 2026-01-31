"""
对话框模块导出
"""
from .icon_picker import IconPickerDialog
from .category_manager import CategoryEditDialog, CategoryManagerDialog
from .template_edit import TemplateEditDialog
from .template_preview import TemplatePreviewDialog
from .batch_move import BatchMoveDialog
from .export_dialog import ExportDialog
from .import_dialog import ImportDialog  # 注意：这里我们避开 Python 关键字 import
from .add_link import AddLinkDialog
from .edit_link import EditLinkDialog
from .scan_wizard import ScanWizardDialog, ScanFlowDialog

# 导出映射，方便直接使用 import 和 export 名称但不冲突
# 在外部使用：from src.gui.dialogs import ImportDialog, ExportDialog
# 这里手动做一个别名处理（虽然类名本身就是 ImportDialog）

__all__ = [
    'IconPickerDialog',
    'CategoryEditDialog',
    'CategoryManagerDialog',
    'TemplateEditDialog',
    'TemplatePreviewDialog',
    'BatchMoveDialog',
    'ExportDialog',
    'ImportDialog',
    'AddLinkDialog',
    'EditLinkDialog',
    'ScanWizardDialog',
    'ScanFlowDialog',
]
