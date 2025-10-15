"""View components for Code Snippet Manager GUI."""

from .gadget_window import GadgetWindow
from .snippet_dialog import SnippetDialog
from .settings_dialog import SettingsDialog
from .code_highlighter import CodeHighlighter, apply_highlighter

__all__ = [
    'GadgetWindow',
    'SnippetDialog',
    'SettingsDialog',
    'CodeHighlighter',
    'apply_highlighter',
]
