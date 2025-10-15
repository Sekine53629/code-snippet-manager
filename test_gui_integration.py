"""GUI Integration Test for Phase 2.2.

This script tests the GUI without actually displaying it
by verifying the widget structure and data loading.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from PyQt6.QtWidgets import QApplication

from src.utils.config import load_config
from src.utils.database import DatabaseManager
from src.views.gadget_window import GadgetWindow


# test_gui_initialization function removed - integrated into main()


def test_tree_population(window):
    """Test that tree is populated with tags and snippets."""
    print("\n[Test 2] Tree Population")
    print("-" * 50)

    tree = window.tree
    root_count = tree.topLevelItemCount()

    print(f"Root items: {root_count}")

    total_items = 0
    tag_items = 0
    snippet_items = 0

    def count_items(item):
        nonlocal total_items, tag_items, snippet_items
        total_items += 1

        item_data = item.data(0, 0x0100)  # Qt.ItemDataRole.UserRole
        if item_data:
            if item_data.get('type') == 'tag':
                tag_items += 1
            elif item_data.get('type') == 'snippet':
                snippet_items += 1

        for i in range(item.childCount()):
            count_items(item.child(i))

    for i in range(root_count):
        count_items(tree.topLevelItem(i))

    print(f"Total items: {total_items}")
    print(f"  Tags: {tag_items}")
    print(f"  Snippets: {snippet_items}")

    if tag_items >= 5 and snippet_items >= 4:
        print("✓ Tree populated correctly")
        return True
    else:
        print(f"✗ Expected at least 5 tags and 4 snippets")
        return False


def test_widget_components(window):
    """Test that all widget components exist."""
    print("\n[Test 3] Widget Components")
    print("-" * 50)

    components = {
        'search_input': hasattr(window, 'search_input'),
        'tree': hasattr(window, 'tree'),
        'preview': hasattr(window, 'preview'),
        'status_label': hasattr(window, 'status_label'),
    }

    for name, exists in components.items():
        status = "✓" if exists else "✗"
        print(f"  {status} {name}: {exists}")

    all_exist = all(components.values())
    if all_exist:
        print("\n✓ All components exist")
    else:
        print("\n✗ Some components missing")

    return all_exist


def test_snippet_text_display(window):
    """Test that snippet text can be displayed."""
    print("\n[Test 4] Snippet Text Display")
    print("-" * 50)

    tree = window.tree

    # Find first snippet item
    def find_snippet_item(item):
        item_data = item.data(0, 0x0100)  # UserRole
        if item_data and item_data.get('type') == 'snippet':
            return item

        for i in range(item.childCount()):
            result = find_snippet_item(item.child(i))
            if result:
                return result
        return None

    snippet_item = None
    for i in range(tree.topLevelItemCount()):
        snippet_item = find_snippet_item(tree.topLevelItem(i))
        if snippet_item:
            break

    if snippet_item:
        item_data = snippet_item.data(0, 0x0100)
        snippet = item_data['data']
        print(f"Found snippet: {snippet['name']}")
        print(f"  Language: {snippet['language']}")
        print(f"  Code length: {len(snippet['code'])} characters")

        # Check if it has a tooltip
        tooltip = snippet_item.toolTip(0)
        print(f"  Tooltip: {tooltip if tooltip else '(none)'}")

        print("✓ Snippet display data validated")
        return True
    else:
        print("✗ No snippet items found")
        return False


def test_context_menu_methods(window):
    """Test that context menu methods exist."""
    print("\n[Test 5] Context Menu Methods")
    print("-" * 50)

    methods = [
        '_show_context_menu',
        '_copy_snippet',
        '_edit_snippet',
        '_delete_snippet',
        '_add_snippet_to_tag',
        '_edit_tag'
    ]

    all_exist = True
    for method_name in methods:
        exists = hasattr(window, method_name)
        status = "✓" if exists else "✗"
        print(f"  {status} {method_name}: {exists}")
        all_exist = all_exist and exists

    if all_exist:
        print("\n✓ All context menu methods exist")
    else:
        print("\n✗ Some methods missing")

    return all_exist


def main():
    """Run all GUI integration tests."""
    print("=" * 50)
    print("GUI Integration Tests - Phase 2.2")
    print("=" * 50)

    # Keep app alive during tests
    app = QApplication(sys.argv)

    try:
        config = load_config()
        db_manager = DatabaseManager(config)
        window = GadgetWindow(config, db_manager)

        print("\n[Test 1] GUI Initialization")
        print("-" * 50)
        print(f"✓ Window created")
        print(f"  Size: {window.width()}x{window.height()}")
        print(f"  Position: ({window.x()}, {window.y()})")
        print(f"  Opacity: {window.windowOpacity()}")

        results = []
        results.append(test_tree_population(window))
        results.append(test_widget_components(window))
        results.append(test_snippet_text_display(window))
        results.append(test_context_menu_methods(window))

        db_manager.close()

        print("\n" + "=" * 50)
        print("Test Summary")
        print("=" * 50)
        passed = sum(results)
        total = len(results)
        print(f"Passed: {passed}/{total}")

        if all(results):
            print("\n✓ All GUI integration tests passed!")
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
