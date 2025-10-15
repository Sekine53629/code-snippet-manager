"""
Auto-insert utility for pasting code into active windows.

Provides cross-platform automatic text insertion using keyboard
simulation to paste code snippets into the previously active window.
"""

import time
import platform
from typing import Optional
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer


class AutoInsertManager:
    """Manager for automatic code insertion."""

    @staticmethod
    def get_active_window_info() -> Optional[dict]:
        """
        Get information about the currently active window.

        Returns:
            Dictionary with window info (title, process, etc.) or None
        """
        system = platform.system()

        if system == 'Darwin':  # macOS
            try:
                from AppKit import NSWorkspace
                active_app = NSWorkspace.sharedWorkspace().activeApplication()
                return {
                    'name': active_app.get('NSApplicationName', ''),
                    'pid': active_app.get('NSApplicationProcessIdentifier', 0),
                    'bundle': active_app.get('NSApplicationBundleIdentifier', ''),
                }
            except ImportError:
                print("PyObjC not available - install pyobjc-framework-Cocoa")
                return None
            except Exception as e:
                print(f"Error getting active window: {e}")
                return None

        elif system == 'Windows':
            try:
                import win32gui
                import win32process
                hwnd = win32gui.GetForegroundWindow()
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                title = win32gui.GetWindowText(hwnd)
                return {
                    'hwnd': hwnd,
                    'pid': pid,
                    'title': title,
                }
            except ImportError:
                print("pywin32 not available - install pywin32")
                return None
            except Exception as e:
                print(f"Error getting active window: {e}")
                return None

        elif system == 'Linux':
            try:
                import subprocess
                # Try using xdotool
                result = subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return {
                        'title': result.stdout.strip(),
                    }
                return None
            except FileNotFoundError:
                print("xdotool not available - install xdotool")
                return None
            except Exception as e:
                print(f"Error getting active window: {e}")
                return None

        return None

    @staticmethod
    def insert_text(text: str, delay_ms: int = 100) -> bool:
        """
        Insert text into the active window using keyboard simulation.

        Args:
            text: Text to insert
            delay_ms: Delay in milliseconds before insertion

        Returns:
            True if successful, False otherwise
        """
        system = platform.system()

        # Use QTimer to delay insertion, allowing user to switch windows
        def do_insert():
            if system == 'Darwin':  # macOS
                return AutoInsertManager._insert_macos(text)
            elif system == 'Windows':
                return AutoInsertManager._insert_windows(text)
            elif system == 'Linux':
                return AutoInsertManager._insert_linux(text)
            return False

        # Schedule insertion after delay
        QTimer.singleShot(delay_ms, do_insert)
        return True

    @staticmethod
    def _insert_macos(text: str) -> bool:
        """Insert text on macOS using AppleScript."""
        try:
            import subprocess
            # Use AppleScript to type text
            # Note: This simulates keystrokes, which may be slow for long text
            # Better approach: Use pasteboard + Cmd+V
            script = f'''
                set the clipboard to "{text}"
                tell application "System Events"
                    keystroke "v" using command down
                end tell
            '''
            subprocess.run(['osascript', '-e', script], check=True)
            return True
        except Exception as e:
            print(f"macOS insert error: {e}")
            return False

    @staticmethod
    def _insert_windows(text: str) -> bool:
        """Insert text on Windows using SendKeys."""
        try:
            import win32clipboard
            import win32con

            # Use clipboard approach (faster and more reliable)
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()

            # Simulate Ctrl+V
            import win32api
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            win32api.keybd_event(ord('V'), 0, 0, 0)
            win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

            return True
        except ImportError:
            print("pywin32 not available - install pywin32")
            return False
        except Exception as e:
            print(f"Windows insert error: {e}")
            return False

    @staticmethod
    def _insert_linux(text: str) -> bool:
        """Insert text on Linux using xdotool."""
        try:
            import subprocess

            # Use xdotool to type text
            # Alternative: Use xclip + Ctrl+V
            subprocess.run(['xdotool', 'type', '--', text], check=True)
            return True
        except FileNotFoundError:
            print("xdotool not available - install xdotool")
            return False
        except Exception as e:
            print(f"Linux insert error: {e}")
            return False

    @staticmethod
    def insert_snippet(snippet: dict, delay_ms: int = 200,
                      replace_placeholders: bool = False) -> bool:
        """
        Insert code snippet with optional placeholder replacement.

        Args:
            snippet: Snippet dictionary with code
            delay_ms: Delay before insertion
            replace_placeholders: Whether to handle placeholders (TODO)

        Returns:
            True if scheduled successfully, False otherwise
        """
        code = snippet.get('code', '')

        if replace_placeholders:
            # TODO: Implement placeholder replacement
            # For now, just insert as-is
            pass

        return AutoInsertManager.insert_text(code, delay_ms)

    @staticmethod
    def is_supported() -> bool:
        """
        Check if auto-insert is supported on this platform.

        Returns:
            True if supported, False otherwise
        """
        system = platform.system()

        if system == 'Darwin':
            # Check for PyObjC
            try:
                import AppKit
                return True
            except ImportError:
                return False

        elif system == 'Windows':
            # Check for pywin32
            try:
                import win32gui
                return True
            except ImportError:
                return False

        elif system == 'Linux':
            # Check for xdotool
            try:
                import subprocess
                result = subprocess.run(['which', 'xdotool'],
                                      capture_output=True)
                return result.returncode == 0
            except Exception:
                return False

        return False
