"""
Qt-based syntax highlighter for QTextEdit widgets.

Provides real-time syntax highlighting using Pygments
integrated with PyQt6's QSyntaxHighlighter.
"""

from PyQt6.QtGui import (
    QSyntaxHighlighter, QTextCharFormat, QFont, QColor
)
from PyQt6.QtCore import Qt, QRegularExpression

from pygments import lex
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.token import Token
from pygments.styles import get_style_by_name


class CodeHighlighter(QSyntaxHighlighter):
    """
    Syntax highlighter for QTextEdit using Pygments.

    Provides real-time highlighting as user types.
    """

    # Token type to color mapping for dark theme
    DARK_THEME_COLORS = {
        Token.Keyword: '#F92672',           # Pink/Magenta
        Token.Keyword.Namespace: '#F92672',
        Token.Keyword.Type: '#66D9EF',      # Cyan
        Token.Name.Class: '#A6E22E',        # Green
        Token.Name.Function: '#A6E22E',
        Token.Name.Builtin: '#66D9EF',
        Token.Name.Decorator: '#F92672',
        Token.String: '#E6DB74',            # Yellow
        Token.String.Doc: '#75715E',        # Gray (docstring)
        Token.Number: '#AE81FF',            # Purple
        Token.Comment: '#75715E',           # Gray
        Token.Comment.Single: '#75715E',
        Token.Comment.Multiline: '#75715E',
        Token.Operator: '#F92672',
        Token.Punctuation: '#F8F8F2',       # White
        Token.Name: '#F8F8F2',
        Token.Literal: '#AE81FF',
        Token.Error: '#960050',             # Red
    }

    # Token type to color mapping for light theme
    LIGHT_THEME_COLORS = {
        Token.Keyword: '#0000FF',           # Blue
        Token.Keyword.Namespace: '#0000FF',
        Token.Keyword.Type: '#2B91AF',      # Teal
        Token.Name.Class: '#2B91AF',
        Token.Name.Function: '#000000',
        Token.Name.Builtin: '#0000FF',
        Token.Name.Decorator: '#A31515',    # Red
        Token.String: '#A31515',            # Red
        Token.String.Doc: '#008000',        # Green (docstring)
        Token.Number: '#09885A',            # Dark green
        Token.Comment: '#008000',           # Green
        Token.Comment.Single: '#008000',
        Token.Comment.Multiline: '#008000',
        Token.Operator: '#000000',
        Token.Punctuation: '#000000',
        Token.Name: '#000000',
        Token.Literal: '#09885A',
        Token.Error: '#FF0000',             # Red
    }

    def __init__(self, parent=None, language: str = 'python', theme: str = 'dark'):
        """
        Initialize code highlighter.

        Args:
            parent: Parent QTextDocument
            language: Programming language
            theme: 'dark' or 'light'
        """
        super().__init__(parent)
        self.language = language
        self.theme = theme
        self._setup_lexer()
        self._setup_formats()

    def _setup_lexer(self):
        """Setup Pygments lexer for the language."""
        try:
            self.lexer = get_lexer_by_name(self.language, stripall=True)
        except Exception:
            self.lexer = TextLexer()

    def _setup_formats(self):
        """Setup text formats for each token type."""
        self.formats = {}

        # Choose color scheme based on theme
        colors = (self.DARK_THEME_COLORS if self.theme == 'dark'
                 else self.LIGHT_THEME_COLORS)

        # Create QTextCharFormat for each token type
        for token_type, color in colors.items():
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))

            # Bold for keywords
            if token_type in [Token.Keyword, Token.Keyword.Namespace]:
                fmt.setFontWeight(QFont.Weight.Bold)

            # Italic for comments
            if token_type in [Token.Comment, Token.Comment.Single,
                            Token.Comment.Multiline, Token.String.Doc]:
                fmt.setFontItalic(True)

            self.formats[token_type] = fmt

    def highlightBlock(self, text: str):
        """
        Highlight a block of text.

        This method is called automatically by Qt when text changes.

        Args:
            text: Text block to highlight
        """
        if not text:
            return

        # Tokenize the text
        try:
            tokens = list(lex(text, self.lexer))
        except Exception:
            return

        # Apply formatting to each token
        position = 0
        for token_type, token_value in tokens:
            length = len(token_value)

            # Find matching format (check parent types if exact match not found)
            fmt = None
            check_type = token_type
            while check_type and not fmt:
                fmt = self.formats.get(check_type)
                check_type = check_type.parent

            # Apply format if found
            if fmt:
                self.setFormat(position, length, fmt)

            position += length

    def set_language(self, language: str):
        """
        Change programming language.

        Args:
            language: New programming language
        """
        self.language = language
        self._setup_lexer()
        self.rehighlight()

    def set_theme(self, theme: str):
        """
        Change color theme.

        Args:
            theme: 'dark' or 'light'
        """
        self.theme = theme
        self._setup_formats()
        self.rehighlight()


def apply_highlighter(text_edit, language: str = 'python', theme: str = 'dark') -> CodeHighlighter:
    """
    Apply syntax highlighting to a QTextEdit widget.

    Args:
        text_edit: QTextEdit or QPlainTextEdit widget
        language: Programming language
        theme: 'dark' or 'light'

    Returns:
        CodeHighlighter instance
    """
    highlighter = CodeHighlighter(text_edit.document(), language, theme)
    return highlighter


# Language name mapping (same as syntax_highlighter.py)
LANGUAGE_ALIASES = {
    'js': 'javascript',
    'ts': 'typescript',
    'py': 'python',
    'c++': 'cpp',
    'c#': 'csharp',
    'cs': 'csharp',
    'rb': 'ruby',
    'sh': 'bash',
    'shell': 'bash',
    'yml': 'yaml',
    'md': 'markdown',
}


def normalize_language(language: str) -> str:
    """
    Normalize language name.

    Args:
        language: Language name

    Returns:
        Normalized language name
    """
    if not language:
        return 'text'

    language = language.lower().strip()
    return LANGUAGE_ALIASES.get(language, language)
