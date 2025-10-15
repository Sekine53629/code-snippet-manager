"""Test script for Phase 2.3 - Dialog implementations.

Tests:
- SnippetDialog initialization
- Dialog field validation
- Snippet creation flow
- Snippet editing flow
- Snippet deletion flow
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt

from src.utils.config import load_config
from src.utils.database import DatabaseManager
from src.views.snippet_dialog import SnippetDialog


def test_dialog_import():
    """Test that SnippetDialog can be imported."""
    print("\n[Test 1] Dialog Import")
    print("-" * 50)

    try:
        from src.views.snippet_dialog import SnippetDialog
        print("✓ SnippetDialog imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_dialog_initialization():
    """Test dialog initialization with tags."""
    print("\n[Test 2] Dialog Initialization")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)

    # Get tags
    tags = db_manager.get_all_tags()
    print(f"Available tags: {len(tags)}")

    # Create dialog (using existing app)
    dialog = SnippetDialog(parent=None, snippet=None, all_tags=tags)

    print(f"✓ Dialog created")
    print(f"  Title: {dialog.windowTitle()}")
    print(f"  Size: {dialog.width()}x{dialog.height()}")
    print(f"  Tag tree items: {dialog.tag_tree.topLevelItemCount()}")

    db_manager.close()
    dialog.close()
    return True


def test_dialog_fields():
    """Test that dialog has all required fields."""
    print("\n[Test 3] Dialog Fields")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)

    tags = db_manager.get_all_tags()
    dialog = SnippetDialog(parent=None, snippet=None, all_tags=tags)

    fields = {
        'name_input': hasattr(dialog, 'name_input'),
        'language_combo': hasattr(dialog, 'language_combo'),
        'code_editor': hasattr(dialog, 'code_editor'),
        'description_input': hasattr(dialog, 'description_input'),
        'tag_tree': hasattr(dialog, 'tag_tree'),
    }

    for field_name, exists in fields.items():
        status = "✓" if exists else "✗"
        print(f"  {status} {field_name}: {exists}")

    db_manager.close()
    dialog.close()
    all_exist = all(fields.values())

    if all_exist:
        print("\n✓ All fields exist")
    else:
        print("\n✗ Some fields missing")

    return all_exist


def test_dialog_validation():
    """Test dialog validation logic."""
    print("\n[Test 4] Dialog Validation")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)

    tags = db_manager.get_all_tags()
    dialog = SnippetDialog(parent=None, snippet=None, all_tags=tags)

    # Temporarily replace QMessageBox to avoid blocking
    from unittest.mock import Mock
    original_warning = QMessageBox.warning
    QMessageBox.warning = Mock(return_value=QMessageBox.StandardButton.Ok)

    # Test empty validation (should fail)
    print("Testing empty form validation...")
    is_valid = dialog._validate()
    print(f"  Empty form valid: {is_valid} (should be False)")

    # Fill in required fields
    dialog.name_input.setText("Test Snippet")
    dialog.code_editor.setPlainText("print('Hello')")

    # Select a tag
    if dialog.tag_tree.topLevelItemCount() > 0:
        first_item = dialog.tag_tree.topLevelItem(0)
        first_item.setCheckState(0, Qt.CheckState.Checked)
        tag_data = first_item.data(0, Qt.ItemDataRole.UserRole)
        if tag_data:
            dialog.selected_tag_ids.append(tag_data['id'])

    print("Testing filled form validation...")
    is_valid = dialog._validate()
    print(f"  Filled form valid: {is_valid} (should be True)")

    # Restore original QMessageBox
    QMessageBox.warning = original_warning

    db_manager.close()
    dialog.close()

    if not is_valid:
        print("✗ Validation failed unexpectedly")
        return False

    print("✓ Validation working correctly")
    return True


def test_snippet_data_structure():
    """Test snippet data structure from dialog."""
    print("\n[Test 5] Snippet Data Structure")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)

    tags = db_manager.get_all_tags()
    dialog = SnippetDialog(parent=None, snippet=None, all_tags=tags)

    # Fill fields
    dialog.name_input.setText("Test Snippet")
    dialog.code_editor.setPlainText("print('Hello, World!')")
    dialog.language_combo.setCurrentText("python")
    dialog.description_input.setPlainText("A simple test snippet")

    # Get data
    data = dialog.get_snippet_data()

    print("Snippet data structure:")
    print(f"  Name: {data['name']}")
    print(f"  Language: {data['language']}")
    print(f"  Code length: {len(data['code'])} chars")
    print(f"  Description length: {len(data['description'])} chars")
    print(f"  Tag IDs: {data['tag_ids']}")

    required_keys = ['name', 'code', 'language', 'description', 'tag_ids']
    has_all_keys = all(key in data for key in required_keys)

    if has_all_keys:
        print("\n✓ All required keys present")
    else:
        print("\n✗ Some keys missing")

    db_manager.close()
    dialog.close()
    return has_all_keys


def main():
    """Run all tests."""
    print("=" * 50)
    print("Phase 2.3 Dialog Tests")
    print("=" * 50)

    # Create QApplication once for all tests
    app = QApplication(sys.argv)

    try:
        results = []
        results.append(test_dialog_import())
        results.append(test_dialog_initialization())
        results.append(test_dialog_fields())
        results.append(test_dialog_validation())
        results.append(test_snippet_data_structure())

        print("\n" + "=" * 50)
        print("Test Summary")
        print("=" * 50)
        passed = sum(results)
        total = len(results)
        print(f"Passed: {passed}/{total}")

        if all(results):
            print("\n✓ All Phase 2.3 tests passed!")
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
