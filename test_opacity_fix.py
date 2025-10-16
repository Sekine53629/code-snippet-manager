#!/usr/bin/env python3
"""
Test that opacity remains consistent after toggling always-on-top.
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest

sys.path.insert(0, '/Users/yoshipc/Documents/GitHub/GitHub_Sekine53629/code-snippet-manager')

from main import CodeSnippetApp


def test_opacity_consistency():
    """Test that text opacity doesn't change when toggling always-on-top."""
    print("=" * 70)
    print("OPACITY CONSISTENCY TEST")
    print("=" * 70)

    app = CodeSnippetApp()
    app.initialize()
    window = app.gadget_window

    window.show()
    QApplication.processEvents()
    time.sleep(0.5)

    print("\n1. INITIAL STATE")
    print("-" * 70)
    initial_opacity = window.windowOpacity()
    print(f"   Window opacity: {initial_opacity}")
    print(f"   Config opacity_active: {window.config.appearance.opacity_active}")
    print(f"   Config opacity_inactive: {window.config.appearance.opacity_inactive}")
    print(f"   Expected: opacity should be {window.config.appearance.opacity_active} (active)")

    if abs(initial_opacity - window.config.appearance.opacity_active) < 0.01:
        print("   ✅ PASS: Using opacity_active (good readability)")
    else:
        print(f"   ❌ FAIL: Opacity is {initial_opacity}, expected {window.config.appearance.opacity_active}")

    # Toggle OFF
    print("\n2. TOGGLE ALWAYS-ON-TOP OFF")
    print("-" * 70)
    QTest.mouseClick(window.btn_always_on_top, Qt.MouseButton.LeftButton)
    QApplication.processEvents()
    time.sleep(0.3)

    opacity_after_toggle_off = window.windowOpacity()
    print(f"   Window opacity: {opacity_after_toggle_off}")
    print(f"   is_always_on_top: {window.is_always_on_top}")

    if abs(opacity_after_toggle_off - initial_opacity) < 0.01:
        print("   ✅ PASS: Opacity unchanged (text still readable)")
    else:
        print(f"   ❌ FAIL: Opacity changed from {initial_opacity} to {opacity_after_toggle_off}")
        print("          This makes text hard to read!")

    # Toggle ON
    print("\n3. TOGGLE ALWAYS-ON-TOP ON AGAIN")
    print("-" * 70)
    QTest.mouseClick(window.btn_always_on_top, Qt.MouseButton.LeftButton)
    QApplication.processEvents()
    time.sleep(0.3)

    opacity_after_toggle_on = window.windowOpacity()
    print(f"   Window opacity: {opacity_after_toggle_on}")
    print(f"   is_always_on_top: {window.is_always_on_top}")

    if abs(opacity_after_toggle_on - initial_opacity) < 0.01:
        print("   ✅ PASS: Opacity unchanged (text still readable)")
    else:
        print(f"   ❌ FAIL: Opacity changed from {initial_opacity} to {opacity_after_toggle_on}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    opacity_consistent = (
        abs(initial_opacity - opacity_after_toggle_off) < 0.01 and
        abs(initial_opacity - opacity_after_toggle_on) < 0.01
    )

    uses_active_opacity = abs(initial_opacity - window.config.appearance.opacity_active) < 0.01

    if opacity_consistent and uses_active_opacity:
        print("✅ ALL TESTS PASSED")
        print("   - Opacity remains consistent during toggles")
        print("   - Uses opacity_active (0.95) for good readability")
        print("   - Text should be clearly visible at all times")
    else:
        print("❌ SOME TESTS FAILED")
        if not opacity_consistent:
            print("   - Opacity changes during toggle (BAD)")
        if not uses_active_opacity:
            print("   - Using wrong opacity value (BAD)")

    print("\nClosing in 2 seconds...")
    QTimer.singleShot(2000, app.app.quit)

    return app.run()


if __name__ == "__main__":
    sys.exit(test_opacity_consistency())
