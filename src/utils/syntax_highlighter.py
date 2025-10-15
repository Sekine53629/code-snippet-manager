"""
Syntax highlighter utility using Pygments.

Provides syntax highlighting for code snippets with:
- Multiple language support
- HTML output with CSS styling
- Dark/light theme support
- Line number support
"""

from typing import Optional
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name, get_all_styles


class SyntaxHighlighter:
    """Manager for syntax highlighting using Pygments."""

    # Language name mappings (common variations)
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

    def __init__(self, style: str = 'monokai', line_numbers: bool = False):
        """
        Initialize syntax highlighter.

        Args:
            style: Pygments style name (e.g., 'monokai', 'github', 'solarized-dark')
            line_numbers: Whether to show line numbers
        """
        self.style = style
        self.line_numbers = line_numbers

    @staticmethod
    def get_available_styles() -> list:
        """
        Get list of available Pygments styles.

        Returns:
            List of style names
        """
        return list(get_all_styles())

    @staticmethod
    def normalize_language(language: str) -> str:
        """
        Normalize language name to Pygments lexer name.

        Args:
            language: Language name (may be alias or common variation)

        Returns:
            Normalized lexer name
        """
        if not language:
            return 'text'

        language = language.lower().strip()

        # Check if it's an alias
        if language in SyntaxHighlighter.LANGUAGE_ALIASES:
            return SyntaxHighlighter.LANGUAGE_ALIASES[language]

        return language

    def highlight_code(self, code: str, language: Optional[str] = None) -> str:
        """
        Highlight code and return HTML.

        Args:
            code: Source code to highlight
            language: Programming language (None for auto-detection)

        Returns:
            HTML string with syntax highlighting
        """
        if not code:
            return ""

        # Get lexer
        try:
            if language:
                # Normalize language name
                language = self.normalize_language(language)
                lexer = get_lexer_by_name(language, stripall=True)
            else:
                # Auto-detect language
                lexer = guess_lexer(code)
        except Exception:
            # Fallback to plain text
            lexer = TextLexer()

        # Configure formatter
        formatter = HtmlFormatter(
            style=self.style,
            linenos='table' if self.line_numbers else False,
            cssclass='highlight',
            wrapcode=True,
        )

        # Generate highlighted HTML
        html = highlight(code, lexer, formatter)

        return html

    def get_css(self) -> str:
        """
        Get CSS for the current style.

        Returns:
            CSS string
        """
        formatter = HtmlFormatter(
            style=self.style,
            linenos='table' if self.line_numbers else False,
            cssclass='highlight'
        )
        return formatter.get_style_defs('.highlight')

    def set_style(self, style: str):
        """
        Change highlighting style.

        Args:
            style: Pygments style name
        """
        # Validate style
        try:
            get_style_by_name(style)
            self.style = style
        except Exception:
            print(f"Invalid style: {style}, keeping current style: {self.style}")

    def set_line_numbers(self, enabled: bool):
        """
        Enable or disable line numbers.

        Args:
            enabled: Whether to show line numbers
        """
        self.line_numbers = enabled

    @staticmethod
    def detect_language(code: str) -> str:
        """
        Detect programming language from code.

        Args:
            code: Source code

        Returns:
            Detected language name
        """
        try:
            lexer = guess_lexer(code)
            return lexer.name
        except Exception:
            return 'Text'


# Predefined style configurations
DARK_STYLES = [
    'monokai',
    'native',
    'fruity',
    'vim',
    'dracula',
    'gruvbox-dark',
    'nord',
    'one-dark',
]

LIGHT_STYLES = [
    'default',
    'emacs',
    'friendly',
    'colorful',
    'autumn',
    'vs',
    'github-dark',  # Actually light despite name
]


def get_recommended_style(theme: str = 'dark') -> str:
    """
    Get recommended style for theme.

    Args:
        theme: 'dark' or 'light'

    Returns:
        Style name
    """
    if theme == 'dark':
        return 'monokai'
    else:
        return 'friendly'


def create_highlighter(theme: str = 'dark', line_numbers: bool = False) -> SyntaxHighlighter:
    """
    Create syntax highlighter with recommended settings.

    Args:
        theme: 'dark' or 'light'
        line_numbers: Whether to show line numbers

    Returns:
        SyntaxHighlighter instance
    """
    style = get_recommended_style(theme)
    return SyntaxHighlighter(style=style, line_numbers=line_numbers)
