#!/usr/bin/env python3
"""
Real-world test: Check if window actually stays on top or goes behind.
This test will show if the WindowStaysOnTopHint is actually working.
"""

import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

sys.path.insert(0, '/Users/yoshipc/Documents/GitHub/GitHub_Sekine53629/code-snippet-manager')

from main import CodeSnippetApp


def test_real_world_behavior():
    """Test actual window behavior in real-world scenario."""
    print("=" * 70)
    print("REAL-WORLD BEHAVIOR TEST")
    print("=" * 70)
    print("\nThis test will:")
    print("1. Show the snippet manager window")
    print("2. Show a large test window that covers the snippet manager")
    print("3. Check if snippet manager stays on top (it should)")
    print("4. Toggle always-on-top OFF")
    print("5. Check if test window now covers snippet manager (it should)")
    print("=" * 70)

    # Create main application
    app = CodeSnippetApp()
    app.initialize()
    snippet_window = app.gadget_window

    # Position snippet window at a visible location
    snippet_window.move(500, 300)
    snippet_window.show()
    QApplication.processEvents()
    time.sleep(0.5)

    # Create a large test window that will definitely overlap
    test_window = QMainWindow()
    test_window.setWindowTitle("Test Window - Should NOT cover snippet manager (initially)")
    test_window.setGeometry(400, 200, 600, 500)

    central = QWidget()
    layout = QVBoxLayout(central)

    label = QLabel("INSTRUCTION:\nLook at the snippet manager window.\n\n"
                   "Phase 1: Snippet manager should be ON TOP of this window\n"
                   "(green button should be BRIGHT)\n\n"
                   "Phase 2 (in 5 seconds): We'll click the green button\n"
                   "Then snippet manager should go BEHIND this window\n"
                   "(green button should be DIM)")
    label.setFont(QFont("Arial", 16))
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("background-color: yellow; padding: 20px;")
    layout.addWidget(label)

    test_window.setCentralWidget(central)

    print("\n✓ Showing test window...")
    test_window.show()
    test_window.raise_()
    test_window.activateWindow()
    QApplication.processEvents()
    time.sleep(0.5)

    # Check initial state
    print("\n" + "=" * 70)
    print("PHASE 1: Initial state (always-on-top should be ON)")
    print("=" * 70)
    print(f"✓ snippet_window.is_always_on_top = {snippet_window.is_always_on_top}")
    print(f"✓ WindowStaysOnTopHint flag = {bool(snippet_window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)}")

    has_hint = bool(snippet_window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)
    if has_hint:
        print("✓ Expected behavior: Snippet manager should be VISIBLE on top of yellow window")
    else:
        print("❌ ERROR: WindowStaysOnTopHint is NOT set but should be!")

    print("\nWaiting 5 seconds for visual confirmation...")
    time.sleep(5)

    # Toggle OFF
    print("\n" + "=" * 70)
    print("PHASE 2: Clicking green button to toggle OFF")
    print("=" * 70)

    # Update label
    label.setText("WATCH THE SNIPPET MANAGER!\n\n"
                  "The green button was just clicked.\n\n"
                  "Snippet manager should now be BEHIND this yellow window\n"
                  "(green button should be DIM)")
    QApplication.processEvents()

    # Simulate clicking by directly calling the method
    print("✓ Calling toggle_always_on_top()...")
    snippet_window.toggle_always_on_top()
    QApplication.processEvents()
    time.sleep(0.5)

    print(f"✓ snippet_window.is_always_on_top = {snippet_window.is_always_on_top}")
    print(f"✓ WindowStaysOnTopHint flag = {bool(snippet_window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)}")

    has_hint_after = bool(snippet_window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)
    if not has_hint_after:
        print("✓ Expected behavior: Snippet manager should now be BEHIND yellow window")
    else:
        print("❌ ERROR: WindowStaysOnTopHint is still set but should be OFF!")

    # Make sure test window is on top
    test_window.raise_()
    test_window.activateWindow()
    QApplication.processEvents()

    print("\nWaiting 5 seconds for visual confirmation...")
    time.sleep(5)

    # Toggle back ON
    print("\n" + "=" * 70)
    print("PHASE 3: Clicking green button again to toggle ON")
    print("=" * 70)

    label.setText("FINAL CHECK!\n\n"
                  "The green button was clicked again.\n\n"
                  "Snippet manager should be BACK ON TOP\n"
                  "(green button should be BRIGHT again)")
    QApplication.processEvents()

    print("✓ Calling toggle_always_on_top()...")
    snippet_window.toggle_always_on_top()
    QApplication.processEvents()
    time.sleep(0.5)

    print(f"✓ snippet_window.is_always_on_top = {snippet_window.is_always_on_top}")
    print(f"✓ WindowStaysOnTopHint flag = {bool(snippet_window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)}")

    has_hint_final = bool(snippet_window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint)
    if has_hint_final:
        print("✓ Expected behavior: Snippet manager should be ON TOP again")
    else:
        print("❌ ERROR: WindowStaysOnTopHint should be ON but is OFF!")

    print("\nWaiting 5 seconds for final visual confirmation...")
    time.sleep(5)

    # Final summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    phase1_correct = has_hint == True
    phase2_correct = has_hint_after == False
    phase3_correct = has_hint_final == True

    print(f"Phase 1 (ON):  Flag={has_hint} Expected=True  {'✅ PASS' if phase1_correct else '❌ FAIL'}")
    print(f"Phase 2 (OFF): Flag={has_hint_after} Expected=False {'✅ PASS' if phase2_correct else '❌ FAIL'}")
    print(f"Phase 3 (ON):  Flag={has_hint_final} Expected=True  {'✅ PASS' if phase3_correct else '❌ FAIL'}")

    if phase1_correct and phase2_correct and phase3_correct:
        print("\n✅ ALL PHASES PASSED - Flag toggling works correctly")
        print("\n❓ VISUAL QUESTION:")
        print("   Did you actually SEE the snippet manager move between")
        print("   being on top and behind the yellow window?")
        print("   If NO, then there's a deeper macOS issue.")
    else:
        print("\n❌ SOME PHASES FAILED - Flag toggling has issues")

    print("\nClosing in 3 seconds...")
    QTimer.singleShot(3000, app.app.quit)

    return app.run()


if __name__ == "__main__":
    sys.exit(test_real_world_behavior())
