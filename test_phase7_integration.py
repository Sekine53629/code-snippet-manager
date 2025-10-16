#!/usr/bin/env python3
"""
Phase 7 Integration Tests - Full System Testing

This script tests the integration of all components of the Code Snippet Manager application.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.config import Config, load_config
from utils.database import DatabaseManager
from utils.fuzzy_search import fuzzy_search_snippets, fuzzy_search_tags
from utils.clipboard import ClipboardManager
from utils.import_export import ImportExportManager
from controllers.hotkey_controller import HotkeyController
from controllers.animation_controller import AnimationController

# For testing Qt components
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from views.gadget_window import GadgetWindow
from views.settings_dialog import SettingsDialog
from views.statistics_dialog import StatisticsDialog


def test_config_loading():
    """Test 1: Configuration loading and validation."""
    print("\n[Test 1] Configuration Loading")
    print("-" * 50)

    try:
        config = load_config()

        # Check appearance config
        assert hasattr(config, 'appearance'), "Config missing appearance"
        assert hasattr(config.appearance, 'theme'), "Appearance missing theme"
        assert hasattr(config.appearance, 'opacity_active'), "Appearance missing opacity_active"
        assert hasattr(config.appearance, 'width_max'), "Appearance missing width_max"

        # Check behavior config
        assert hasattr(config, 'behavior'), "Config missing behavior"
        assert hasattr(config.behavior, 'auto_insert'), "Behavior missing auto_insert"

        # Check database config
        assert hasattr(config, 'database'), "Config missing database"
        assert hasattr(config.database, 'local'), "Database missing local"
        assert hasattr(config.database.local, 'path'), "Database.local missing path"

        print(f"✓ Config loaded successfully")
        print(f"  Theme: {config.appearance.theme}")
        print(f"  Opacity: {config.appearance.opacity_active}")
        print(f"  Size: {config.appearance.width_max}x{config.appearance.height_max}")
        print(f"  Local DB: {config.database.local.path}")

        return True, config

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_database_operations(config):
    """Test 2: Database CRUD operations."""
    print("\n[Test 2] Database Operations")
    print("-" * 50)

    try:
        db_manager = DatabaseManager(config)

        # Test tag creation
        tag_id = db_manager.get_or_create_tag("TestTag", tag_type="folder")
        assert tag_id is not None, "Failed to create tag"
        print(f"✓ Tag created: ID={tag_id}")

        # Test snippet creation
        snippet_id = db_manager.add_snippet(
            name="Test Snippet",
            code="print('Hello')",
            language="python",
            description="Test snippet",
            tag_ids=[tag_id]
        )
        assert snippet_id is not None, "Failed to create snippet"
        print(f"✓ Snippet created: ID={snippet_id}")

        # Test snippet retrieval
        snippet = db_manager.get_snippet_by_id(snippet_id)
        assert snippet is not None, "Failed to retrieve snippet"
        assert snippet['name'] == "Test Snippet", "Snippet name mismatch"
        print(f"✓ Snippet retrieved: {snippet['name']}")

        # Test favorite toggle
        is_fav = db_manager.toggle_favorite(snippet_id)
        print(f"✓ Favorite toggled: {is_fav}")

        favorites = db_manager.get_favorite_snippets()
        assert len(favorites) >= 1, "Failed to get favorites"
        print(f"✓ Favorites retrieved: {len(favorites)} snippets")

        # Note: Test data will remain in database for inspection
        print(f"✓ Test completed successfully")

        return True, db_manager

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_fuzzy_search(db_manager):
    """Test 3: Fuzzy search functionality."""
    print("\n[Test 3] Fuzzy Search")
    print("-" * 50)

    try:
        # Create test data
        tag_id = db_manager.get_or_create_tag("SearchTest")
        snippet_id = db_manager.add_snippet(
            name="Django Model",
            code="class Article(models.Model): pass",
            language="python",
            description="A Django model example",
            tag_ids=[tag_id]
        )

        # Test fuzzy search
        all_snippets = db_manager.get_all_snippets()

        # Exact match
        results = fuzzy_search_snippets("Django", all_snippets, threshold=0.3)
        assert len(results) > 0, "Fuzzy search failed for exact match"
        print(f"✓ Exact match 'Django': {len(results)} results")

        # Typo match
        results = fuzzy_search_snippets("Djngo", all_snippets, threshold=0.3)
        print(f"✓ Typo match 'Djngo': {len(results)} results")

        # Partial match
        results = fuzzy_search_snippets("mod", all_snippets, threshold=0.3)
        print(f"✓ Partial match 'mod': {len(results)} results")

        # Note: Test data will remain in database for inspection

        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_import_export(db_manager):
    """Test 4: Import/Export functionality."""
    print("\n[Test 4] Import/Export")
    print("-" * 50)

    try:
        import_export = ImportExportManager(db_manager)

        # Test JSON export
        json_file = Path("test_export.json")
        success = import_export.export_to_json(str(json_file))
        assert success, "JSON export failed"
        assert json_file.exists(), "JSON file not created"
        print(f"✓ JSON export: {json_file.stat().st_size} bytes")

        # Test Markdown export
        md_file = Path("test_export.md")
        success = import_export.export_to_markdown(str(md_file))
        assert success, "Markdown export failed"
        assert md_file.exists(), "Markdown file not created"
        print(f"✓ Markdown export: {md_file.stat().st_size} bytes")

        # Test statistics
        stats = import_export.get_export_stats()
        print(f"✓ Export stats:")
        print(f"  Total snippets: {stats['total_snippets']}")
        print(f"  Total tags: {stats['total_tags']}")
        print(f"  Languages: {', '.join(stats['languages'])}")

        # Cleanup
        json_file.unlink(missing_ok=True)
        md_file.unlink(missing_ok=True)

        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_qt_integration(db_manager, config):
    """Test 5: Qt GUI integration."""
    print("\n[Test 5] Qt GUI Integration")
    print("-" * 50)

    try:
        app = QApplication.instance() or QApplication(sys.argv)

        # Test GadgetWindow creation
        gadget = GadgetWindow(db_manager=db_manager, config=config)
        assert gadget is not None, "Failed to create GadgetWindow"
        print(f"✓ GadgetWindow created")

        # Test SettingsDialog creation
        settings = SettingsDialog(config, parent=gadget)
        assert settings is not None, "Failed to create SettingsDialog"
        print(f"✓ SettingsDialog created")

        # Test StatisticsDialog creation
        statistics = StatisticsDialog(db_manager, parent=gadget)
        assert statistics is not None, "Failed to create StatisticsDialog"
        print(f"✓ StatisticsDialog created")

        # Test HotkeyController creation
        hotkey = HotkeyController()
        assert hotkey is not None, "Failed to create HotkeyController"
        print(f"✓ HotkeyController created")

        # Test AnimationController creation
        animation = AnimationController(gadget)
        assert animation is not None, "Failed to create AnimationController"
        print(f"✓ AnimationController created")

        # Test window visibility
        gadget.show()
        assert gadget.isVisible(), "Window not visible"
        print(f"✓ Window shown successfully")

        # Close window using QTimer to avoid blocking
        QTimer.singleShot(100, app.quit)
        QTimer.singleShot(50, gadget.close)

        # Run event loop briefly
        app.processEvents()

        print(f"✓ All Qt components initialized successfully")

        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_clipboard(db_manager):
    """Test 6: Clipboard operations."""
    print("\n[Test 6] Clipboard Operations")
    print("-" * 50)

    try:
        # Ensure QApplication exists
        app = QApplication.instance()
        if app is None:
            print("⚠ QApplication not available, skipping clipboard test")
            return True

        # Create test snippet
        tag_id = db_manager.get_or_create_tag("ClipboardTest")
        snippet_id = db_manager.add_snippet(
            name="Copy Test",
            code="def hello(): return 'world'",
            language="python",
            description="Test clipboard",
            tag_ids=[tag_id]
        )

        snippet = db_manager.get_snippet_by_id(snippet_id)

        # Test clipboard copy
        success = ClipboardManager.copy_snippet(snippet, include_comments=False)
        assert success, "Failed to copy snippet"
        print(f"✓ Snippet copied to clipboard")

        # Test with comments
        success = ClipboardManager.copy_snippet(snippet, include_comments=True)
        assert success, "Failed to copy snippet with comments"
        print(f"✓ Snippet copied with comments")

        # Note: Test data will remain in database for inspection

        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling(db_manager):
    """Test 7: Error handling and edge cases."""
    print("\n[Test 7] Error Handling")
    print("-" * 50)

    try:
        # Test invalid snippet ID
        snippet = db_manager.get_snippet_by_id(999999)
        assert snippet is None, "Should return None for invalid ID"
        print(f"✓ Invalid snippet ID handled correctly")

        # Test invalid tag ID
        tag = db_manager.get_tag_by_id(999999)
        assert tag is None, "Should return None for invalid tag ID"
        print(f"✓ Invalid tag ID handled correctly")

        # Test delete non-existent snippet
        success = db_manager.delete_snippet(999999)
        assert not success, "Should return False for non-existent snippet"
        print(f"✓ Delete non-existent snippet handled correctly")

        # Test empty search
        results = fuzzy_search_snippets("", [], threshold=0.3)
        assert len(results) == 0, "Empty search should return empty results"
        print(f"✓ Empty search handled correctly")

        # Test very long snippet name
        long_name = "A" * 1000
        snippet_id = db_manager.add_snippet(
            name=long_name,
            code="pass",
            language="python",
            description="Test"
        )
        assert snippet_id is not None, "Failed to create snippet with long name"
        db_manager.delete_snippet(snippet_id)
        print(f"✓ Long snippet name handled correctly")

        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("Phase 7 Integration Tests - Full System Testing")
    print("=" * 60)

    results = []
    config = None
    db_manager = None

    # Test 1: Configuration
    success, config = test_config_loading()
    results.append(("Configuration Loading", success))
    if not success:
        print("\n⚠ Skipping remaining tests due to config failure")
        return

    # Test 2: Database
    success, db_manager = test_database_operations(config)
    results.append(("Database Operations", success))
    if not success:
        print("\n⚠ Skipping remaining tests due to database failure")
        return

    # Test 3: Fuzzy Search
    success = test_fuzzy_search(db_manager)
    results.append(("Fuzzy Search", success))

    # Test 4: Import/Export
    success = test_import_export(db_manager)
    results.append(("Import/Export", success))

    # Test 5: Qt Integration (creates QApplication for clipboard test)
    success = test_qt_integration(db_manager, config)
    results.append(("Qt GUI Integration", success))

    # Test 6: Clipboard (requires QApplication from test 5)
    success = test_clipboard(db_manager)
    results.append(("Clipboard Operations", success))

    # Test 7: Error Handling
    success = test_error_handling(db_manager)
    results.append(("Error Handling", success))

    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✓" if success else "✗"
        print(f"{status} {name}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("\n✓ All integration tests passed!")
    else:
        print(f"\n⚠ {total - passed} test(s) failed")

    # Cleanup
    if db_manager:
        db_manager.close()


if __name__ == '__main__':
    main()
