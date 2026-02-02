"""
对话框模块导出
"""
from src.gui.dialogs.icon_picker import IconPickerDialog
from src.gui.dialogs.category_manager import CategoryEditDialog, CategoryManagerDialog
from src.gui.dialogs.template_edit import TemplateEditDialog
from src.gui.dialogs.template_preview import TemplatePreviewDialog
from src.gui.dialogs.batch_move import BatchMoveDialog
from src.gui.dialogs.export_dialog import ExportDialog
from src.gui.dialogs.import_dialog import ImportDialog
from src.gui.dialogs.add_link import AddLinkDialog
from src.gui.dialogs.edit_link import EditLinkDialog
from src.gui.dialogs.scan_wizard import ScanWizardDialog, ScanFlowDialog

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
