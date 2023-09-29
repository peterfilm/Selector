# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['selector.py'],
    pathex=[],
    binaries=[
        ('libs/exiv2.dll', '.'),
        ('venv/Lib/site-packages/pyexiv2/lib/py3.11-win/exiv2api.pyd', '.')
    ],
    datas=[('style.qss', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='selector',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['img\\icon.ico'],
)
