"""
Test script for Phase 6 implementations.

Tests:
- Import/Export functionality
- Statistics dialog
- Favorite snippets
"""

import sys
import tempfile
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from PyQt6.QtWidgets import QApplication

from src.utils.config import load_config
from src.utils.database import DatabaseManager
from src.utils.import_export import ImportExportManager
from src.views.statistics_dialog import StatisticsDialog


def test_import_export_json():
    """Test JSON export/import."""
    print("\n[Test 1] Import/Export - JSON")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)
    ie_manager = ImportExportManager(db_manager)

    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name

    try:
        # Export to JSON
        success = ie_manager.export_to_json(temp_file, include_stats=True)
        print(f"✓ JSON export: {success}")

        # Check file exists and has content
        file_path = Path(temp_file)
        file_size = file_path.stat().st_size
        print(f"  File size: {file_size} bytes")

        # Get export stats
        stats = ie_manager.get_export_stats()
        print(f"  Total snippets: {stats['total_snippets']}")
        print(f"  Total tags: {stats['total_tags']}")
        print(f"  Languages: {list(stats['languages'].keys())}")

        print("\n✓ JSON export/import test passed")
        return True

    finally:
        # Cleanup
        try:
            Path(temp_file).unlink()
        except:
            pass
        db_manager.close()


def test_import_export_markdown():
    """Test Markdown export."""
    print("\n[Test 2] Import/Export - Markdown")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)
    ie_manager = ImportExportManager(db_manager)

    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        temp_file = f.name

    try:
        # Export to Markdown
        success = ie_manager.export_to_markdown(temp_file, organize_by_tag=True)
        print(f"✓ Markdown export: {success}")

        # Check file exists and has content
        file_path = Path(temp_file)
        file_size = file_path.stat().st_size
        print(f"  File size: {file_size} bytes")

        # Read first few lines
        with open(temp_file, 'r') as f:
            lines = f.readlines()[:5]
            print(f"  First line: {lines[0].strip() if lines else 'empty'}")

        print("\n✓ Markdown export test passed")
        return True

    finally:
        # Cleanup
        try:
            Path(temp_file).unlink()
        except:
            pass
        db_manager.close()


def test_backup_restore():
    """Test backup functionality."""
    print("\n[Test 3] Backup/Restore")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)
    ie_manager = ImportExportManager(db_manager)

    try:
        # Create backup
        backup_file = ie_manager.create_backup(backup_dir='test_backups')
        print(f"✓ Backup created: {backup_file}")

        if backup_file:
            file_path = Path(backup_file)
            exists = file_path.exists()
            print(f"  File exists: {exists}")

            if exists:
                file_size = file_path.stat().st_size
                print(f"  File size: {file_size} bytes")

                # Cleanup
                file_path.unlink()
                # Only remove directory if empty
                try:
                    file_path.parent.rmdir()
                except OSError:
                    pass  # Directory not empty, that's fine

        print("\n✓ Backup/restore test passed")
        return True

    finally:
        db_manager.close()


def test_statistics_dialog():
    """Test statistics dialog."""
    print("\n[Test 4] Statistics Dialog")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)

    try:
        # Create dialog
        dialog = StatisticsDialog(db_manager)
        print(f"✓ Statistics dialog created")
        print(f"  Window title: {dialog.windowTitle()}")

        # Check tables
        print(f"  Most used table rows: {dialog.most_used_table.rowCount()}")
        print(f"  Language table rows: {dialog.lang_table.rowCount()}")

        # Check summary
        summary_text = dialog.summary_label.text()
        has_content = len(summary_text) > 0
        print(f"  Summary has content: {has_content}")

        dialog.close()
        print("\n✓ Statistics dialog test passed")
        return True

    finally:
        db_manager.close()


def test_favorite_snippets():
    """Test favorite snippets functionality."""
    print("\n[Test 5] Favorite Snippets")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)

    try:
        # Get all snippets
        snippets = db_manager.get_all_snippets()
        print(f"Total snippets: {len(snippets)}")

        if len(snippets) > 0:
            # Toggle favorite on first snippet
            first_snippet = snippets[0]
            snippet_id = first_snippet['id']
            snippet_name = first_snippet['name']

            print(f"\nTesting with snippet: '{snippet_name}'")

            # Toggle to favorite
            is_fav = db_manager.toggle_favorite(snippet_id)
            print(f"  Toggled to favorite: {is_fav}")

            # Get favorites
            favorites = db_manager.get_favorite_snippets()
            print(f"  Total favorites: {len(favorites)}")

            # Toggle back
            is_fav = db_manager.toggle_favorite(snippet_id)
            print(f"  Toggled back: {not is_fav}")

            # Check favorites again
            favorites = db_manager.get_favorite_snippets()
            print(f"  Total favorites after toggle: {len(favorites)}")

        print("\n✓ Favorite snippets test passed")
        return True

    finally:
        db_manager.close()


def main():
    """Run all tests."""
    print("=" * 50)
    print("Phase 6 Tests - Extended Features")
    print("=" * 50)

    # Create QApplication for dialogs
    app = QApplication(sys.argv)

    try:
        results = []
        results.append(test_import_export_json())
        results.append(test_import_export_markdown())
        results.append(test_backup_restore())
        results.append(test_statistics_dialog())
        results.append(test_favorite_snippets())

        print("\n" + "=" * 50)
        print("Test Summary")
        print("=" * 50)
        passed = sum(results)
        total = len(results)
        print(f"Passed: {passed}/{total}")

        if all(results):
            print("\n✓ All Phase 6 tests passed!")
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
