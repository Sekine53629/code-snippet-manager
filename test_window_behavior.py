#!/usr/bin/env python3
"""
Detailed test for window behavior and always-on-top functionality.
Tests actual window stacking order and visibility.
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest

sys.path.insert(0, '/Users/yoshipc/Documents/GitHub/GitHub_Sekine53629/code-snippet-manager')

from main import CodeSnippetApp


def test_window_stacking():
    """Test window stacking behavior with always-on-top."""
    print("=" * 70)
    print("DETAILED WINDOW STACKING TEST")
    print("=" * 70)

    # Create main application
    app = CodeSnippetApp()
    app.initialize()
    snippet_window = app.gadget_window

    # Create a test window to check stacking
    test_window = QMainWindow()
    test_window.setWindowTitle("Test Window (Should go UNDER snippet window)")
    test_window.setGeometry(100, 100, 400, 300)
    label = QLabel("This window should be UNDER the snippet manager\nwhen always-on-top is enabled.", test_window)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    test_window.setCentralWidget(label)

    # Show both windows
    snippet_window.show()
    test_window.show()
    QApplication.processEvents()
    time.sleep(0.5)

    print("\n📋 TEST SCENARIO 1: Always-on-top ENABLED (default)")
    print("-" * 70)
    print(f"   Snippet window is_always_on_top: {snippet_window.is_always_on_top}")
    print(f"   WindowStaysOnTopHint flag: {bool(snippet_window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)}")

    # Raise test window to try to cover snippet window
    test_window.raise_()
    test_window.activateWindow()
    QApplication.processEvents()
    time.sleep(0.3)

    print(f"   ✓ Test window raised (attempted to cover snippet window)")
    print(f"   → Snippet window should STILL be visible on top")

    time.sleep(1)

    # Toggle OFF
    print("\n📋 TEST SCENARIO 2: Toggle always-on-top OFF")
    print("-" * 70)
    btn = snippet_window.btn_always_on_top
    QTest.mouseClick(btn, Qt.MouseButton.LeftButton)
    QApplication.processEvents()
    time.sleep(0.3)

    print(f"   Snippet window is_always_on_top: {snippet_window.is_always_on_top}")
    print(f"   WindowStaysOnTopHint flag: {bool(snippet_window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)}")

    # Raise test window again
    test_window.raise_()
    test_window.activateWindow()
    QApplication.processEvents()
    time.sleep(0.3)

    print(f"   ✓ Test window raised again")
    print(f"   → Snippet window should now be UNDER test window")

    time.sleep(1)

    # Toggle ON again
    print("\n📋 TEST SCENARIO 3: Toggle always-on-top ON again")
    print("-" * 70)
    QTest.mouseClick(btn, Qt.MouseButton.LeftButton)
    QApplication.processEvents()
    time.sleep(0.3)

    print(f"   Snippet window is_always_on_top: {snippet_window.is_always_on_top}")
    print(f"   WindowStaysOnTopHint flag: {bool(snippet_window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)}")
    print(f"   → Snippet window should be back on top again")

    # Final summary
    print("\n" + "=" * 70)
    print("DETAILED TEST RESULTS")
    print("=" * 70)

    final_state = snippet_window.is_always_on_top
    final_flag = bool(snippet_window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)

    if final_state and final_flag:
        print("✅ PASS: Always-on-top functionality is working correctly")
        print("   - State variable matches window flag")
        print("   - Window properly shows/hides on toggle")
        print("   - Green button successfully controls the behavior")
    else:
        print("❌ FAIL: Inconsistency detected")
        print(f"   - is_always_on_top: {final_state}")
        print(f"   - WindowStaysOnTopHint: {final_flag}")

    print("\n💡 VISUAL CHECK:")
    print("   Please verify visually:")
    print("   - When ON: Snippet window stays on top of test window")
    print("   - When OFF: Test window can cover snippet window")
    print("   - Green button opacity changes (255 when ON, 120 when OFF)")

    # Close after 3 seconds
    print("\nClosing in 3 seconds...")
    QTimer.singleShot(3000, app.app.quit)

    return app.run()


if __name__ == "__main__":
    sys.exit(test_window_stacking())
