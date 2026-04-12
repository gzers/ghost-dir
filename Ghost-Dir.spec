# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# 显式收集 shiboken6 和 PySide6 的全部内容（包含 Shiboken.pyd 等 C 扩展）
# PyInstaller 静态分析无法自动发现这些依赖，必须手动声明
shiboken6_datas, shiboken6_binaries, shiboken6_hiddenimports = collect_all('shiboken6')
pyside6_datas, pyside6_binaries, pyside6_hiddenimports = collect_all('PySide6')

a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[] + shiboken6_binaries + pyside6_binaries,
    datas=[
        ('assets', 'assets'),
        ('config', 'config'),
    ] + shiboken6_datas + pyside6_datas,
    hiddenimports=[
        'src.gui.views.links',
        'src.gui.views.wizard',
        'src.gui.views.library',
        'src.gui.views.help',
        'src.gui.views.settings',
        'src.drivers.usn_journal',
    ] + shiboken6_hiddenimports + pyside6_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Ghost-Dir',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Ghost-Dir',
)
