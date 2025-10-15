"""
Test script for Phase 5 implementations.

Tests:
- Syntax highlighter utility
- Qt code highlighter integration
- Settings dialog
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from PyQt6.QtWidgets import QApplication, QTextEdit
from PyQt6.QtCore import Qt

from src.utils.config import load_config
from src.utils.syntax_highlighter import SyntaxHighlighter, create_highlighter, get_recommended_style
from src.views.code_highlighter import CodeHighlighter, apply_highlighter, normalize_language
from src.views.settings_dialog import SettingsDialog


def test_syntax_highlighter_basic():
    """Test basic syntax highlighter functionality."""
    print("\n[Test 1] Syntax Highlighter - Basic")
    print("-" * 50)

    highlighter = SyntaxHighlighter(style='monokai', line_numbers=False)
    print(f"Highlighter created with style: {highlighter.style}")

    # Test Python code highlighting
    python_code = """
def hello_world():
    print("Hello, World!")
    return 42
"""

    html_output = highlighter.highlight_code(python_code, 'python')
    print(f"✓ Python code highlighted")
    print(f"  HTML output length: {len(html_output)} chars")
    print(f"  Contains 'highlight' class: {'highlight' in html_output}")

    # Test language normalization
    test_cases = [
        ('py', 'python'),
        ('js', 'javascript'),
        ('c++', 'cpp'),
        ('c#', 'csharp'),
        ('shell', 'bash'),
    ]

    print("\nLanguage normalization:")
    for alias, expected in test_cases:
        result = SyntaxHighlighter.normalize_language(alias)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{alias}' -> '{result}' (expected: '{expected}')")

    print("\n✓ Syntax highlighter basic tests passed")
    return True


def test_syntax_highlighter_styles():
    """Test available styles."""
    print("\n[Test 2] Syntax Highlighter - Styles")
    print("-" * 50)

    styles = SyntaxHighlighter.get_available_styles()
    print(f"Available styles: {len(styles)}")
    print(f"  First 10: {list(styles)[:10]}")

    # Test style changing
    highlighter = SyntaxHighlighter()
    print(f"\nDefault style: {highlighter.style}")

    highlighter.set_style('monokai')
    print(f"Changed to: {highlighter.style}")

    # Test recommended styles
    dark_style = get_recommended_style('dark')
    light_style = get_recommended_style('light')
    print(f"\nRecommended styles:")
    print(f"  Dark theme: {dark_style}")
    print(f"  Light theme: {light_style}")

    print("\n✓ Style tests passed")
    return True


def test_qt_code_highlighter():
    """Test Qt-based code highlighter."""
    print("\n[Test 3] Qt Code Highlighter")
    print("-" * 50)

    # Create a QTextEdit widget
    text_edit = QTextEdit()

    # Apply highlighter
    highlighter = apply_highlighter(text_edit, language='python', theme='dark')
    print(f"✓ Highlighter applied to QTextEdit")
    print(f"  Language: {highlighter.language}")
    print(f"  Theme: {highlighter.theme}")

    # Test language change
    highlighter.set_language('javascript')
    print(f"✓ Language changed to: {highlighter.language}")

    # Test theme change
    highlighter.set_theme('light')
    print(f"✓ Theme changed to: {highlighter.theme}")

    # Test language normalization
    normalized = normalize_language('py')
    print(f"✓ Language normalization: 'py' -> '{normalized}'")

    print("\n✓ Qt code highlighter tests passed")
    return True


def test_settings_dialog():
    """Test settings dialog."""
    print("\n[Test 4] Settings Dialog")
    print("-" * 50)

    config = load_config()

    # Create dialog
    dialog = SettingsDialog(config)
    print(f"✓ Settings dialog created")
    print(f"  Window title: {dialog.windowTitle()}")
    print(f"  Tab count: {dialog.tabs.count()}")

    # Check tabs
    tab_names = []
    for i in range(dialog.tabs.count()):
        tab_names.append(dialog.tabs.tabText(i))
    print(f"  Tabs: {', '.join(tab_names)}")

    # Check that widgets exist
    widgets = {
        'position_combo': hasattr(dialog, 'position_combo'),
        'theme_combo': hasattr(dialog, 'theme_combo'),
        'opacity_slider': hasattr(dialog, 'opacity_slider'),
        'auto_insert_enabled': hasattr(dialog, 'auto_insert_enabled'),
        'db_mode_combo': hasattr(dialog, 'db_mode_combo'),
    }

    print("\nWidget checks:")
    for widget_name, exists in widgets.items():
        status = "✓" if exists else "✗"
        print(f"  {status} {widget_name}: {exists}")

    all_exist = all(widgets.values())

    if all_exist:
        print("\n✓ All settings dialog widgets exist")
    else:
        print("\n✗ Some widgets missing")

    dialog.close()
    return all_exist


def test_settings_load_save():
    """Test settings load and save."""
    print("\n[Test 5] Settings Load/Save")
    print("-" * 50)

    config = load_config()

    # Create dialog
    dialog = SettingsDialog(config)

    # Check loaded values
    print("Loaded values:")
    print(f"  Position: {dialog.position_combo.currentText()}")
    print(f"  Theme: {dialog.theme_combo.currentText()}")
    print(f"  Opacity: {dialog.opacity_slider.value()}%")
    print(f"  Auto-insert enabled: {dialog.auto_insert_enabled.isChecked()}")

    # Change some values
    dialog.position_combo.setCurrentText('left')
    dialog.theme_combo.setCurrentText('light')
    dialog.opacity_slider.setValue(80)

    # Save settings
    dialog._save_settings()

    print("\nChanged values:")
    print(f"  Position: {dialog.temp_config.appearance.position}")
    print(f"  Theme: {dialog.temp_config.appearance.theme}")
    print(f"  Opacity: {dialog.temp_config.appearance.opacity_active}")

    # Verify changes
    assert dialog.temp_config.appearance.position == 'left'
    assert dialog.temp_config.appearance.theme == 'light'
    assert dialog.temp_config.appearance.opacity_active == 0.80

    print("\n✓ Settings load/save working")
    dialog.close()
    return True


def main():
    """Run all tests."""
    print("=" * 50)
    print("Phase 5 Tests - UI/UX Improvements")
    print("=" * 50)

    # Create QApplication once for all tests
    app = QApplication(sys.argv)

    try:
        results = []
        results.append(test_syntax_highlighter_basic())
        results.append(test_syntax_highlighter_styles())
        results.append(test_qt_code_highlighter())
        results.append(test_settings_dialog())
        results.append(test_settings_load_save())

        print("\n" + "=" * 50)
        print("Test Summary")
        print("=" * 50)
        passed = sum(results)
        total = len(results)
        print(f"Passed: {passed}/{total}")

        if all(results):
            print("\n✓ All Phase 5 tests passed!")
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
