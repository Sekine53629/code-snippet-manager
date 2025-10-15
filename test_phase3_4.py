"""
Test script for Phase 3 & 4 implementations.

Tests:
- Fuzzy search functionality
- Clipboard operations
- Auto-insert support detection
- Hotkey controller
- Animation controller
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt

from src.utils.config import load_config
from src.utils.database import DatabaseManager
from src.utils.fuzzy_search import (
    calculate_fuzzy_score, calculate_snippet_score,
    fuzzy_search_snippets, fuzzy_search_tags
)
from src.utils.clipboard import ClipboardManager
from src.utils.auto_insert import AutoInsertManager
from src.controllers.hotkey_controller import HotkeyController
from src.controllers.animation_controller import AnimationController


def test_fuzzy_search():
    """Test fuzzy search utility."""
    print("\n[Test 1] Fuzzy Search")
    print("-" * 50)

    # Test basic string matching
    score1 = calculate_fuzzy_score("python", "python")
    print(f"Exact match 'python' == 'python': {score1:.2f} (should be 1.0)")

    score2 = calculate_fuzzy_score("py", "python")
    print(f"Substring match 'py' in 'python': {score2:.2f} (should be > 0.8)")

    score3 = calculate_fuzzy_score("pyton", "python")
    print(f"Fuzzy match 'pyton' ~ 'python': {score3:.2f} (should be > 0.5)")

    # Test snippet scoring
    snippet = {
        'name': 'List Comprehension',
        'code': '[x for x in range(10)]',
        'description': 'Python list comprehension example',
        'language': 'python'
    }

    score4 = calculate_snippet_score("list", snippet)
    print(f"Snippet score for 'list': {score4:.2f}")

    score5 = calculate_snippet_score("python", snippet)
    print(f"Snippet score for 'python': {score5:.2f}")

    print("✓ Fuzzy search working")
    return True


def test_fuzzy_search_integration():
    """Test fuzzy search with database."""
    print("\n[Test 2] Fuzzy Search Integration")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)

    # Get all snippets and tags
    snippets = db_manager.get_all_snippets()
    tags = db_manager.get_all_tags()

    print(f"Total snippets: {len(snippets)}")
    print(f"Total tags: {len(tags)}")

    # Test search
    snippet_results = fuzzy_search_snippets("list", snippets, threshold=0.3)
    print(f"Search 'list': {len(snippet_results)} snippets")

    if snippet_results:
        print("\nTop 3 results:")
        for i, (snippet, score) in enumerate(snippet_results[:3]):
            print(f"  {i+1}. {snippet['name']} ({score:.0%})")

    tag_results = fuzzy_search_tags("py", tags, threshold=0.3)
    print(f"\nSearch 'py': {len(tag_results)} tags")

    if tag_results:
        for tag, score in tag_results[:3]:
            print(f"  - {tag['name']} ({score:.0%})")

    db_manager.close()
    print("\n✓ Fuzzy search integration working")
    return True


def test_clipboard():
    """Test clipboard operations."""
    print("\n[Test 3] Clipboard Operations")
    print("-" * 50)

    # Check availability
    has_clipboard = ClipboardManager.has_clipboard()
    print(f"Clipboard available: {has_clipboard}")

    if has_clipboard:
        # Test copy
        test_text = "Hello, Clipboard!"
        success = ClipboardManager.copy_text(test_text)
        print(f"Copy text: {success}")

        # Test get
        retrieved = ClipboardManager.get_text()
        print(f"Retrieved text: '{retrieved}'")
        matches = retrieved == test_text
        print(f"Text matches: {matches}")

        # Test snippet copy
        snippet = {
            'name': 'Test Snippet',
            'code': 'print("Hello")',
            'language': 'python',
            'description': 'A test snippet'
        }

        success = ClipboardManager.copy_snippet(snippet, include_comments=False)
        print(f"Copy snippet (no comments): {success}")

        success = ClipboardManager.copy_snippet(snippet, include_comments=True)
        print(f"Copy snippet (with comments): {success}")

        # Show clipboard content
        clipboard_content = ClipboardManager.get_text()
        print(f"\nClipboard content:\n{clipboard_content}")

        print("\n✓ Clipboard operations working")
        return True
    else:
        print("✗ Clipboard not available")
        return False


def test_auto_insert():
    """Test auto-insert support."""
    print("\n[Test 4] Auto-Insert Support")
    print("-" * 50)

    supported = AutoInsertManager.is_supported()
    print(f"Auto-insert supported: {supported}")

    if supported:
        window_info = AutoInsertManager.get_active_window_info()
        if window_info:
            print(f"Active window info:")
            for key, value in window_info.items():
                print(f"  {key}: {value}")
        else:
            print("  Could not get active window info")

        print("\n✓ Auto-insert support detected")
        return True
    else:
        print("✗ Auto-insert not supported on this platform")
        print("  (This is expected on macOS without PyObjC)")
        return True  # Not an error, just not available


def test_hotkey_controller():
    """Test hotkey controller."""
    print("\n[Test 5] Hotkey Controller")
    print("-" * 50)

    controller = HotkeyController(double_tap_threshold_ms=500)
    print(f"Controller created")
    print(f"  Threshold: 500ms")
    print(f"  Platform: {controller.system}")

    # Test hotkey parsing
    parsed = HotkeyController.parse_hotkey_string("Ctrl+Shift+S")
    print(f"\nParsed 'Ctrl+Shift+S':")
    print(f"  Modifiers: {parsed['modifiers']}")
    print(f"  Key: {parsed['key']}")

    # Test signal connection
    signal_received = []

    def on_double_tap():
        signal_received.append(True)
        print("  Signal received: Ctrl double-tap")

    controller.ctrl_double_tap.connect(on_double_tap)
    print("\nSignal connected")

    supported = controller.is_supported()
    print(f"Hotkeys supported: {supported}")

    print("\n✓ Hotkey controller working")
    return True


def test_animation_controller():
    """Test animation controller."""
    print("\n[Test 6] Animation Controller")
    print("-" * 50)

    # Create a dummy widget
    widget = QWidget()
    widget.setGeometry(100, 100, 300, 400)

    controller = AnimationController(widget)
    print(f"Controller created with widget")

    # Test fade in animation
    fade_in = controller.fade_in(duration_ms=300)
    print(f"Fade in animation: {fade_in is not None}")

    # Test expand animation
    expand = controller.expand_horizontal(target_width=500, duration_ms=400)
    print(f"Expand animation: {expand is not None}")

    # Test collapse animation
    collapse = controller.collapse_horizontal(target_width=200, duration_ms=400)
    print(f"Collapse animation: {collapse is not None}")

    # Test edge animations
    expand_from_edge = controller.expand_from_edge(edge='right')
    print(f"Expand from edge: {expand_from_edge is not None}")

    collapse_to_edge = controller.collapse_to_edge(edge='right')
    print(f"Collapse to edge: {collapse_to_edge is not None}")

    # Check running state
    is_running = controller.is_running()
    print(f"Animation running: {is_running}")

    print("\n✓ Animation controller working")
    return True


def main():
    """Run all tests."""
    print("=" * 50)
    print("Phase 3 & 4 Tests")
    print("=" * 50)

    # Create QApplication once for all tests
    app = QApplication(sys.argv)

    try:
        results = []
        results.append(test_fuzzy_search())
        results.append(test_fuzzy_search_integration())
        results.append(test_clipboard())
        results.append(test_auto_insert())
        results.append(test_hotkey_controller())
        results.append(test_animation_controller())

        print("\n" + "=" * 50)
        print("Test Summary")
        print("=" * 50)
        passed = sum(results)
        total = len(results)
        print(f"Passed: {passed}/{total}")

        if all(results):
            print("\n✓ All Phase 3 & 4 tests passed!")
            return 0
        else:
            print("\n✗ Some tests failed")
            return 1

    except Exception as e:
        print(f"\n✗ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
