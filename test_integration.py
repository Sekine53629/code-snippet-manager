#!/usr/bin/env python3
"""
Integration Tests for Code Snippet Manager

Tests the complete integration of all application components.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.config import load_config
from utils.database import DatabaseManager
from utils.fuzzy_search import fuzzy_search_snippets, fuzzy_search_tags
from utils.import_export import ImportExportManager
from utils.syntax_highlighter import SyntaxHighlighter


def test_config():
    """Test configuration loading."""
    print("\n[Test 1] Configuration Loading")
    print("-" * 50)

    try:
        config = load_config()

        # Check configuration fields
        assert hasattr(config, 'appearance'), "Missing appearance config"
        assert hasattr(config, 'behavior'), "Missing behavior config"
        assert hasattr(config, 'database'), "Missing database config"

        print(f"✓ Config loaded successfully")
        print(f"  Theme: {config.appearance.theme}")
        print(f"  Position: {config.appearance.position}")
        print(f"  Database mode: {config.database.mode}")

        return True, config

    except Exception as e:
        print(f"✗ Config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_database(config):
    """Test database operations."""
    print("\n[Test 2] Database Operations")
    print("-" * 50)

    try:
        # Initialize database
        db_manager = DatabaseManager(config)

        # Test: Get all tags
        tags = db_manager.get_all_tags()
        print(f"✓ Tags retrieved: {len(tags)} tags")
        for tag in tags[:3]:
            print(f"  • {tag['name']} ({tag['type']})")

        # Test: Get all snippets
        snippets = db_manager.get_all_snippets()
        print(f"✓ Snippets retrieved: {len(snippets)} snippets")
        for snippet in snippets[:3]:
            print(f"  • {snippet['name']} ({snippet['language']})")

        # Test: Search snippets
        search_results = db_manager.search_snippets("python")
        print(f"✓ Search works: {len(search_results)} results for 'python'")

        # Test: Get snippets by tag
        if tags:
            tag_snippets = db_manager.get_snippets_by_tag(tags[0]['id'])
            print(f"✓ Tag filtering works: {len(tag_snippets)} snippets for '{tags[0]['name']}'")

        return True, db_manager

    except Exception as e:
        print(f"✗ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_fuzzy_search(db_manager):
    """Test fuzzy search functionality."""
    print("\n[Test 3] Fuzzy Search")
    print("-" * 50)

    try:
        # Get test data
        snippets = db_manager.get_all_snippets()
        tags = db_manager.get_all_tags()

        # Test: Fuzzy search snippets
        query = "djngo"  # Intentional typo
        results = fuzzy_search_snippets(query, snippets, threshold=0.3, max_results=10)
        print(f"✓ Fuzzy search snippets: '{query}' found {len(results)} results")
        for result in results[:3]:
            print(f"  • {result['snippet']['name']} (score: {result['score']:.2f})")

        # Test: Fuzzy search tags
        query = "pyton"  # Intentional typo
        tag_results = fuzzy_search_tags(query, tags, threshold=0.3, max_results=10)
        print(f"✓ Fuzzy search tags: '{query}' found {len(tag_results)} results")
        for tag, score in tag_results[:3]:
            print(f"  • {tag['name']} (score: {score:.2f})")

        return True

    except Exception as e:
        print(f"✗ Fuzzy search test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_import_export(db_manager):
    """Test import/export functionality."""
    print("\n[Test 4] Import/Export")
    print("-" * 50)

    try:
        ie_manager = ImportExportManager(db_manager)

        # Test: Get export stats
        stats = ie_manager.get_export_stats()
        print(f"✓ Export stats retrieved:")
        print(f"  Total tags: {stats['total_tags']}")
        print(f"  Total snippets: {stats['total_snippets']}")
        print(f"  Total usage: {stats['total_usage']}")
        print(f"  Languages: {list(stats['languages'].keys())}")

        # Test: JSON export
        test_export_path = Path("test_export.json")
        success = ie_manager.export_to_json(str(test_export_path))
        if success and test_export_path.exists():
            file_size = test_export_path.stat().st_size
            print(f"✓ JSON export successful: {file_size} bytes")
            test_export_path.unlink()  # Cleanup
        else:
            print(f"✗ JSON export failed")
            return False

        # Test: Markdown export
        test_md_path = Path("test_export.md")
        success = ie_manager.export_to_markdown(str(test_md_path))
        if success and test_md_path.exists():
            file_size = test_md_path.stat().st_size
            print(f"✓ Markdown export successful: {file_size} bytes")
            test_md_path.unlink()  # Cleanup
        else:
            print(f"✗ Markdown export failed")
            return False

        return True

    except Exception as e:
        print(f"✗ Import/Export test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_syntax_highlighter():
    """Test syntax highlighter."""
    print("\n[Test 5] Syntax Highlighter")
    print("-" * 50)

    try:
        highlighter = SyntaxHighlighter(style='monokai', line_numbers=False)

        # Test: Python highlighting
        python_code = "def hello():\n    print('Hello, World!')"
        html_output = highlighter.highlight_code(python_code, language='python')

        assert '<' in html_output, "HTML output expected"
        assert 'def' in html_output or 'hello' in html_output, "Code not in output"
        print(f"✓ Python highlighting works")
        print(f"  Output length: {len(html_output)} chars")

        # Test: JavaScript highlighting
        js_code = "const x = 10;"
        html_output = highlighter.highlight_code(js_code, language='javascript')
        assert 'const' in html_output or 'x' in html_output, "JS code not in output"
        print(f"✓ JavaScript highlighting works")

        # Test: Auto language detection
        html_output = highlighter.highlight_code(python_code)
        print(f"✓ Auto language detection works")

        return True

    except Exception as e:
        print(f"✗ Syntax highlighter test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_favorites(db_manager):
    """Test favorite snippets functionality."""
    print("\n[Test 6] Favorite Snippets")
    print("-" * 50)

    try:
        # Get a snippet to test with
        snippets = db_manager.get_all_snippets()
        if not snippets:
            print("⚠ No snippets available for favorite test")
            return True

        test_snippet = snippets[0]
        snippet_id = test_snippet['id']

        # Test: Toggle favorite
        is_favorite = db_manager.toggle_favorite(snippet_id)
        print(f"✓ Toggled favorite: {test_snippet['name']} -> {is_favorite}")

        # Test: Get favorites
        favorites = db_manager.get_favorite_snippets()
        print(f"✓ Retrieved favorites: {len(favorites)} snippets")

        # Toggle back
        is_favorite = db_manager.toggle_favorite(snippet_id)
        print(f"✓ Toggled back: {test_snippet['name']} -> {is_favorite}")

        return True

    except Exception as e:
        print(f"✗ Favorites test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("Code Snippet Manager - Integration Tests")
    print("=" * 60)

    results = []

    # Test 1: Configuration
    success, config = test_config()
    results.append(("Configuration", success))
    if not success:
        print("\n❌ Configuration test failed. Stopping tests.")
        return False

    # Test 2: Database
    success, db_manager = test_database(config)
    results.append(("Database", success))
    if not success:
        print("\n❌ Database test failed. Stopping tests.")
        return False

    # Test 3: Fuzzy Search
    success = test_fuzzy_search(db_manager)
    results.append(("Fuzzy Search", success))

    # Test 4: Import/Export
    success = test_import_export(db_manager)
    results.append(("Import/Export", success))

    # Test 5: Syntax Highlighter
    success = test_syntax_highlighter()
    results.append(("Syntax Highlighter", success))

    # Test 6: Favorites
    success = test_favorites(db_manager)
    results.append(("Favorites", success))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status:8} | {name}")

    print("-" * 60)
    print(f"Result: {passed}/{total} tests passed")

    if passed == total:
        print("\n✅ All integration tests passed!")
        return True
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return False


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
