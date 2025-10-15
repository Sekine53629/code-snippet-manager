# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Build Specification for Code Snippet Manager

This file defines how to build the executable for the application.

Usage:
    pyinstaller build.spec
"""

import sys
from pathlib import Path

block_cipher = None

# Project root
project_root = Path('.').absolute()
src_path = project_root / 'src'

# Analysis: Collect all Python files and dependencies
a = Analysis(
    ['main.py'],
    pathex=[str(project_root), str(src_path)],
    binaries=[],
    datas=[
        # Include config directory
        ('config', 'config'),
        # Include requirements for reference
        ('requirements.txt', '.'),
        # Include documentation
        ('README.md', '.'),
        ('REQUIREMENTS.md', '.'),
        ('TECHNICAL_DESIGN.md', '.'),
    ],
    hiddenimports=[
        # Core modules
        'src',
        'src.models',
        'src.models.models',
        'src.utils',
        'src.utils.config',
        'src.utils.database',
        'src.utils.fuzzy_search',
        'src.utils.clipboard',
        'src.utils.auto_insert',
        'src.utils.syntax_highlighter',
        'src.utils.import_export',
        'src.views',
        'src.views.gadget_window',
        'src.views.snippet_dialog',
        'src.views.settings_dialog',
        'src.views.statistics_dialog',
        'src.views.code_highlighter',
        'src.controllers',
        'src.controllers.hotkey_controller',
        'src.controllers.animation_controller',
        # PyQt6
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        # SQLAlchemy
        'sqlalchemy',
        'sqlalchemy.orm',
        'sqlalchemy.ext',
        'sqlalchemy.ext.declarative',
        # Pydantic
        'pydantic',
        'pydantic_core',
        # Pygments
        'pygments',
        'pygments.lexers',
        'pygments.formatters',
        'pygments.styles',
        # Other dependencies
        'pyperclip',
        'fuzzywuzzy',
        'rapidfuzz',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude test files
        'pytest',
        'unittest',
        # Exclude development tools
        'black',
        'pylint',
        'mypy',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ: Python archive
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# EXE: Executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CodeSnippetManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one: 'icon.ico' or 'icon.icns'
)

# COLLECT: Collect all files
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CodeSnippetManager'
)

# macOS App Bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='CodeSnippetManager.app',
        icon=None,  # Add icon path here: 'icon.icns'
        bundle_identifier='com.sekine53629.codesnippetmanager',
        info_plist={
            'CFBundleName': 'Code Snippet Manager',
            'CFBundleDisplayName': 'Code Snippet Manager',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': 'True',
            'LSMinimumSystemVersion': '10.13.0',
            'NSAppleEventsUsageDescription': 'Code Snippet Manager needs access to control other applications for code insertion.',
            'NSAppleScriptEnabled': 'True',
        },
    )
