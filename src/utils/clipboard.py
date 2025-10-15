"""
Clipboard utility for copying code snippets.

Provides cross-platform clipboard operations with optional
formatting and history tracking.
"""

from typing import Optional
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QClipboard


class ClipboardManager:
    """Manager for clipboard operations."""

    @staticmethod
    def copy_text(text: str, mode: QClipboard.Mode = QClipboard.Mode.Clipboard) -> bool:
        """
        Copy text to clipboard.

        Args:
            text: Text to copy
            mode: Clipboard mode (Clipboard or Selection)

        Returns:
            True if successful, False otherwise
        """
        try:
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText(text, mode)
                return True
            return False
        except Exception as e:
            print(f"Clipboard copy error: {e}")
            return False

    @staticmethod
    def get_text(mode: QClipboard.Mode = QClipboard.Mode.Clipboard) -> Optional[str]:
        """
        Get text from clipboard.

        Args:
            mode: Clipboard mode (Clipboard or Selection)

        Returns:
            Clipboard text or None if unavailable
        """
        try:
            clipboard = QApplication.clipboard()
            if clipboard:
                return clipboard.text(mode)
            return None
        except Exception as e:
            print(f"Clipboard read error: {e}")
            return None

    @staticmethod
    def clear(mode: QClipboard.Mode = QClipboard.Mode.Clipboard) -> bool:
        """
        Clear clipboard content.

        Args:
            mode: Clipboard mode (Clipboard or Selection)

        Returns:
            True if successful, False otherwise
        """
        try:
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.clear(mode)
                return True
            return False
        except Exception as e:
            print(f"Clipboard clear error: {e}")
            return False

    @staticmethod
    def copy_snippet(snippet: dict, include_comments: bool = False) -> bool:
        """
        Copy code snippet to clipboard with optional metadata.

        Args:
            snippet: Snippet dictionary with code, name, language, description
            include_comments: Whether to include metadata as comments

        Returns:
            True if successful, False otherwise
        """
        code = snippet.get('code', '')

        if include_comments:
            # Add metadata as comments
            language = snippet.get('language', 'text')
            name = snippet.get('name', 'Unnamed')
            description = snippet.get('description', '')

            # Determine comment style based on language
            if language in ['python', 'ruby', 'bash', 'shell', 'perl']:
                comment_prefix = '# '
            elif language in ['javascript', 'typescript', 'java', 'cpp', 'c',
                            'csharp', 'go', 'rust', 'php', 'kotlin', 'swift']:
                comment_prefix = '// '
            elif language in ['sql']:
                comment_prefix = '-- '
            elif language in ['html', 'xml']:
                # Multi-line comment for HTML/XML
                header = f"<!-- Snippet: {name}"
                if description:
                    header += f"\n     {description}"
                header += " -->\n"
                code = header + code
                return ClipboardManager.copy_text(code)
            else:
                # Default to # for unknown languages
                comment_prefix = '# '

            # Build header
            header = f"{comment_prefix}Snippet: {name}\n"
            if description:
                header += f"{comment_prefix}{description}\n"
            header += "\n"

            code = header + code

        return ClipboardManager.copy_text(code)

    @staticmethod
    def has_clipboard() -> bool:
        """
        Check if clipboard is available.

        Returns:
            True if clipboard is available, False otherwise
        """
        try:
            clipboard = QApplication.clipboard()
            return clipboard is not None
        except Exception:
            return False
