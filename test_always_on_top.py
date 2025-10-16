#!/usr/bin/env python3
"""
Test script for always-on-top functionality.
This script will launch the application and test the green button.
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest

# Add src to path
sys.path.insert(0, '/Users/yoshipc/Documents/GitHub/GitHub_Sekine53629/code-snippet-manager')

from main import CodeSnippetApp


def test_always_on_top():
    """Test always-on-top toggle functionality."""
    print("=" * 60)
    print("Testing Always-On-Top Functionality")
    print("=" * 60)

    # Create application
    app = CodeSnippetApp()
    app.initialize()  # Need to initialize first
    window = app.gadget_window

    # Show window
    window.show()
    QApplication.processEvents()
    time.sleep(0.5)

    print("\n1. Initial State Check:")
    print(f"   is_always_on_top: {window.is_always_on_top}")
    print(f"   WindowStaysOnTopHint in flags: {bool(window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)}")
    print(f"   Green button exists: {hasattr(window, 'btn_always_on_top')}")

    if hasattr(window, 'btn_always_on_top'):
        btn = window.btn_always_on_top
        print(f"   Button enabled: {btn.isEnabled()}")
        print(f"   Button visible: {btn.isVisible()}")
        print(f"   Button size: {btn.size().width()}x{btn.size().height()}")

        # Test clicking the button
        print("\n2. Clicking green button (toggle OFF)...")
        initial_state = window.is_always_on_top

        # Click the button
        QTest.mouseClick(btn, Qt.MouseButton.LeftButton)
        QApplication.processEvents()
        time.sleep(0.3)

        print(f"   Before click: is_always_on_top = {initial_state}")
        print(f"   After click:  is_always_on_top = {window.is_always_on_top}")
        print(f"   WindowStaysOnTopHint in flags: {bool(window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)}")
        print(f"   State changed: {initial_state != window.is_always_on_top}")

        # Click again to toggle ON
        print("\n3. Clicking green button again (toggle ON)...")
        state_before_second_click = window.is_always_on_top

        QTest.mouseClick(btn, Qt.MouseButton.LeftButton)
        QApplication.processEvents()
        time.sleep(0.3)

        print(f"   Before click: is_always_on_top = {state_before_second_click}")
        print(f"   After click:  is_always_on_top = {window.is_always_on_top}")
        print(f"   WindowStaysOnTopHint in flags: {bool(window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)}")
        print(f"   State changed: {state_before_second_click != window.is_always_on_top}")

        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)

        # Check if toggle worked correctly
        first_toggle_worked = (initial_state != state_before_second_click)
        second_toggle_worked = (state_before_second_click != window.is_always_on_top)
        returned_to_initial = (window.is_always_on_top == initial_state)

        if first_toggle_worked and second_toggle_worked and returned_to_initial:
            print("✅ PASS: Always-on-top toggle is working correctly")
            print(f"   - Initial state: {initial_state}")
            print(f"   - After 1st click: {state_before_second_click} (toggled)")
            print(f"   - After 2nd click: {window.is_always_on_top} (toggled back)")
        else:
            print("❌ FAIL: Always-on-top toggle is NOT working")
            print("\nDEBUG INFO:")
            print(f"   Initial: {initial_state}")
            print(f"   After 1st click: {state_before_second_click}")
            print(f"   After 2nd click: {window.is_always_on_top}")
            print(f"   First toggle worked: {first_toggle_worked}")
            print(f"   Second toggle worked: {second_toggle_worked}")
    else:
        print("\n❌ ERROR: Green button (btn_always_on_top) not found!")

    # Close after 2 seconds
    print("\nClosing application in 2 seconds...")
    QTimer.singleShot(2000, app.app.quit)

    return app.run()


if __name__ == "__main__":
    sys.exit(test_always_on_top())
