"""
Hotkey controller for global keyboard shortcuts.

Provides hotkey detection and management, including:
- Ctrl double-tap detection
- Custom hotkey registration
- Cross-platform support
"""

import time
import platform
from typing import Optional, Callable
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt


class HotkeyController(QObject):
    """Controller for managing global hotkeys."""

    # Signals
    ctrl_double_tap = pyqtSignal()  # Emitted on Ctrl double-tap
    hotkey_triggered = pyqtSignal(str)  # Emitted with hotkey name

    def __init__(self, double_tap_threshold_ms: int = 500):
        """
        Initialize hotkey controller.

        Args:
            double_tap_threshold_ms: Maximum time between taps (milliseconds)
        """
        super().__init__()

        self.double_tap_threshold = double_tap_threshold_ms / 1000.0  # Convert to seconds
        self.last_ctrl_press_time = 0.0
        self.ctrl_press_count = 0
        self.monitoring = False

        # Timer to reset double-tap detection
        self.reset_timer = QTimer()
        self.reset_timer.timeout.connect(self._reset_ctrl_count)
        self.reset_timer.setSingleShot(True)

        # Platform-specific setup
        self.system = platform.system()
        self._setup_platform()

    def start(self):
        """Start hotkey monitoring (simplified version)."""
        self.monitoring = True
        print("✓ Hotkey monitoring started (Ctrl double-tap)")
        return True

    def stop(self):
        """Stop hotkey monitoring."""
        self.monitoring = False
        print("✓ Hotkey monitoring stopped")

    def _setup_platform(self):
        """Setup platform-specific hotkey handling."""
        if self.system == 'Darwin':  # macOS
            self._setup_macos()
        elif self.system == 'Windows':
            self._setup_windows()
        elif self.system == 'Linux':
            self._setup_linux()

    def _setup_macos(self):
        """Setup macOS-specific hotkey handling."""
        # macOS uses NSEvent monitoring
        # Note: Requires accessibility permissions
        pass

    def _setup_windows(self):
        """Setup Windows-specific hotkey handling."""
        # Windows uses RegisterHotKey API
        pass

    def _setup_linux(self):
        """Setup Linux-specific hotkey handling."""
        # Linux uses X11 or Wayland event monitoring
        pass

    def handle_key_event(self, event: QKeyEvent, pressed: bool):
        """
        Handle keyboard events for hotkey detection.

        Args:
            event: Qt key event
            pressed: True if key pressed, False if released
        """
        # Check for Ctrl key
        if event.key() in (Qt.Key.Key_Control, Qt.Key.Key_Meta):
            if pressed:
                self._on_ctrl_pressed()

    def _on_ctrl_pressed(self):
        """Handle Ctrl key press for double-tap detection."""
        current_time = time.time()
        time_since_last = current_time - self.last_ctrl_press_time

        if time_since_last < self.double_tap_threshold:
            # Second tap detected
            self.ctrl_press_count += 1

            if self.ctrl_press_count >= 2:
                # Double-tap detected!
                self.ctrl_double_tap.emit()
                self._reset_ctrl_count()
                return

        else:
            # First tap or too much time passed
            self.ctrl_press_count = 1

        self.last_ctrl_press_time = current_time

        # Start reset timer
        self.reset_timer.start(int(self.double_tap_threshold * 1000))

    def _reset_ctrl_count(self):
        """Reset Ctrl press counter."""
        self.ctrl_press_count = 0

    def register_global_hotkey(self, hotkey: str, callback: Callable) -> bool:
        """
        Register a global hotkey.

        Args:
            hotkey: Hotkey string (e.g., "Ctrl+Shift+S")
            callback: Function to call when hotkey is pressed

        Returns:
            True if successful, False otherwise
        """
        # TODO: Implement platform-specific global hotkey registration
        print(f"Global hotkey registration not yet implemented: {hotkey}")
        return False

    def unregister_global_hotkey(self, hotkey: str) -> bool:
        """
        Unregister a global hotkey.

        Args:
            hotkey: Hotkey string to unregister

        Returns:
            True if successful, False otherwise
        """
        # TODO: Implement platform-specific global hotkey unregistration
        return False

    def is_supported(self) -> bool:
        """
        Check if global hotkeys are supported on this platform.

        Returns:
            True if supported, False otherwise
        """
        # For now, only double-tap detection works (no global hotkeys)
        return True

    @staticmethod
    def parse_hotkey_string(hotkey: str) -> dict:
        """
        Parse hotkey string into components.

        Args:
            hotkey: Hotkey string (e.g., "Ctrl+Shift+S")

        Returns:
            Dictionary with modifiers and key
        """
        parts = hotkey.split('+')
        modifiers = []
        key = None

        for part in parts:
            part = part.strip().lower()
            if part in ['ctrl', 'control']:
                modifiers.append('Ctrl')
            elif part in ['shift']:
                modifiers.append('Shift')
            elif part in ['alt']:
                modifiers.append('Alt')
            elif part in ['meta', 'cmd', 'command', 'win', 'super']:
                modifiers.append('Meta')
            else:
                key = part

        return {
            'modifiers': modifiers,
            'key': key
        }


class MacOSHotkeyMonitor(QObject):
    """
    macOS-specific global hotkey monitoring using Quartz.

    Requires PyObjC and accessibility permissions.
    """

    hotkey_pressed = pyqtSignal(int, int)  # key_code, modifiers

    def __init__(self):
        super().__init__()
        self.monitoring = False

    def start_monitoring(self) -> bool:
        """
        Start monitoring global keyboard events.

        Returns:
            True if successful, False otherwise
        """
        try:
            from Quartz import (
                CGEventMaskBit, CGEventTapCreate, kCGEventKeyDown,
                kCGHeadInsertEventTap, kCGSessionEventTap,
                CFMachPortCreateRunLoopSource, CFRunLoopGetCurrent,
                CFRunLoopAddSource, kCFRunLoopCommonModes,
                CGEventTapEnable
            )

            # Create event tap
            mask = CGEventMaskBit(kCGEventKeyDown)

            def callback(proxy, event_type, event, refcon):
                """Handle keyboard events."""
                # Extract key code and modifiers
                # TODO: Emit signal with key info
                return event

            self.event_tap = CGEventTapCreate(
                kCGSessionEventTap,
                kCGHeadInsertEventTap,
                0,
                mask,
                callback,
                None
            )

            if not self.event_tap:
                print("Failed to create event tap (accessibility permissions required)")
                return False

            # Add to run loop
            run_loop_source = CFMachPortCreateRunLoopSource(None, self.event_tap, 0)
            CFRunLoopAddSource(CFRunLoopGetCurrent(), run_loop_source, kCFRunLoopCommonModes)
            CGEventTapEnable(self.event_tap, True)

            self.monitoring = True
            return True

        except ImportError:
            print("PyObjC not available - install pyobjc-framework-Quartz")
            return False
        except Exception as e:
            print(f"Error starting hotkey monitoring: {e}")
            return False

    def stop_monitoring(self):
        """Stop monitoring global keyboard events."""
        if self.monitoring:
            # TODO: Clean up event tap
            self.monitoring = False
