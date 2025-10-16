#!/usr/bin/env python3
"""
Diagnose macOS-specific window flag issues.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt

sys.path.insert(0, '/Users/yoshipc/Documents/GitHub/GitHub_Sekine53629/code-snippet-manager')

from main import CodeSnippetApp


def test_window_flags():
    """Test different window flag combinations on macOS."""
    print("=" * 70)
    print("macOS WINDOW FLAGS DIAGNOSTIC TEST")
    print("=" * 70)

    app = CodeSnippetApp()
    app.initialize()
    window = app.gadget_window

    print("\n1. CURRENT FLAG CONFIGURATION")
    print("-" * 70)
    flags = window.windowFlags()
    print(f"   Window flags value: {int(flags)}")
    print(f"   FramelessWindowHint: {bool(flags & Qt.WindowType.FramelessWindowHint)}")
    print(f"   WindowStaysOnTopHint: {bool(flags & Qt.WindowType.WindowStaysOnTopHint)}")
    print(f"   Tool: {bool(flags & Qt.WindowType.Tool)}")

    print("\n2. OPACITY SETTINGS")
    print("-" * 70)
    print(f"   Current windowOpacity: {window.windowOpacity()}")
    print(f"   Config opacity_active: {window.config.appearance.opacity_active}")
    print(f"   Config opacity_inactive: {window.config.appearance.opacity_inactive}")

    print("\n3. macOS-SPECIFIC ISSUES")
    print("-" * 70)
    print("   Known issue: Qt.WindowType.Tool may interfere with")
    print("   WindowStaysOnTopHint on macOS.")
    print("")
    print("   Problem 1: Tool flag can prevent proper window stacking")
    print("   Problem 2: opacity_inactive (0.3) makes everything 70% transparent")

    print("\n4. RECOMMENDED FIXES")
    print("-" * 70)
    print("   Fix 1: Remove Qt.WindowType.Tool flag")
    print("   Fix 2: Don't call setWindowOpacity in toggle_always_on_top()")
    print("   Fix 3: Use opacity_active (0.95) or 1.0 for normal operation")

    # Test without Tool flag
    print("\n5. TESTING WITHOUT Tool FLAG")
    print("-" * 70)

    new_flags = (Qt.WindowType.FramelessWindowHint |
                 Qt.WindowType.WindowStaysOnTopHint)

    print(f"   New flags: {int(new_flags)}")
    print(f"   Setting new flags...")

    window.setWindowFlags(new_flags)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    window.setWindowOpacity(1.0)  # Full opacity for test
    window.show()
    window.raise_()

    print(f"   ✓ Window reshown with new flags")
    print(f"   WindowStaysOnTopHint: {bool(window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)}")
    print(f"   Tool: {bool(window.windowFlags() & Qt.WindowType.Tool)}")
    print(f"   Window opacity: {window.windowOpacity()}")

    # Show test window
    test_win = QMainWindow()
    test_win.setWindowTitle("Test Window - Try to cover snippet manager")
    test_win.setGeometry(400, 200, 600, 400)
    label = QLabel("If snippet manager stays ON TOP of this window,\nthe fix works!", test_win)
    label.setStyleSheet("background: yellow; font-size: 20px; padding: 40px;")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    test_win.setCentralWidget(label)
    test_win.show()
    test_win.raise_()
    test_win.activateWindow()

    print("\n   VISUAL CHECK: Is snippet manager on top of yellow window?")
    print("   If YES -> Fix works! Remove Tool flag permanently.")
    print("   If NO -> There's a deeper macOS issue.")

    print("\n" + "=" * 70)
    print("Waiting 10 seconds for visual inspection...")
    print("=" * 70)

    from PyQt6.QtCore import QTimer
    QTimer.singleShot(10000, app.app.quit)

    return app.run()


if __name__ == "__main__":
    sys.exit(test_window_flags())
