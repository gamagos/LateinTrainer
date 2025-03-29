# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/logic', 'logic'), ('src/data', 'data'), ('src/assets', 'assets')],
    hiddenimports=['tkinter.font', 'tkinter.ttk', 'tkinter.messagebox', 'win32api', 'win32con', 'json', 'numpy', 'secrets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["PyQt5", "PySide2", "django", "email", "pytest", "asyncio", "cryptography", "sqlite3", "xml", "ssl", "numpy.testing",
    "numpy.f2py",
    "numpy.distutils",
    "numpy.matlib"],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Latein Trainer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src\\assets\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    upx=True,
    upx_exclude=[],
    name='Latein Trainer',
)
