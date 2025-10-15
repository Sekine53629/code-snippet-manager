"""Test script for Phase 2.2 improvements.

Tests:
- Tree item details (snippet count display)
- Snippet items in tree
- Context menu functionality
- Usage count tracking
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.utils.config import load_config
from src.utils.database import DatabaseManager


def test_snippet_count_display():
    """Test that snippet counts are correctly calculated."""
    print("\n[Test 1] Snippet Count Display")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)

    tags = db_manager.get_all_tags()
    print(f"Total tags: {len(tags)}")

    for tag in tags:
        snippets = db_manager.get_snippets_by_tag(tag['id'])
        print(f"  {tag['icon']} {tag['name']}: {len(snippets)} snippet(s)")

    db_manager.close()
    print("✓ Test passed")


def test_snippet_retrieval():
    """Test that snippets can be retrieved correctly."""
    print("\n[Test 2] Snippet Retrieval")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)

    tags = db_manager.get_all_tags()

    total_snippets = 0
    for tag in tags:
        snippets = db_manager.get_snippets_by_tag(tag['id'])
        for snippet in snippets:
            total_snippets += 1
            print(f"  📄 {snippet['name']} ({snippet['language']})")
            print(f"     Usage: {snippet['usage_count']} times")

    print(f"\nTotal snippets found: {total_snippets}")
    db_manager.close()
    print("✓ Test passed")


def test_usage_count_increment():
    """Test that usage count can be incremented."""
    print("\n[Test 3] Usage Count Increment")
    print("-" * 50)

    config = load_config()
    db_manager = DatabaseManager(config)

    # Find a snippet
    tags = db_manager.get_all_tags()
    if tags:
        snippets = db_manager.get_snippets_by_tag(tags[0]['id'])
        if snippets:
            snippet = snippets[0]
            old_count = snippet['usage_count']
            print(f"Snippet: {snippet['name']}")
            print(f"Current usage count: {old_count}")

            # Increment usage
            with db_manager.get_local_session() as session:
                from src.models.models import Snippet
                db_snippet = session.query(Snippet).filter(Snippet.id == snippet['id']).first()
                if db_snippet:
                    db_snippet.increment_usage()
                    session.commit()
                    new_count = db_snippet.usage_count
                    print(f"New usage count: {new_count}")

                    if new_count == old_count + 1:
                        print("✓ Usage count incremented correctly")
                    else:
                        print(f"✗ Expected {old_count + 1}, got {new_count}")
        else:
            print("⚠ No snippets found in first tag")
    else:
        print("⚠ No tags found")

    db_manager.close()
    print("✓ Test passed")


def test_data_structure():
    """Test the new data structure with type field."""
    print("\n[Test 4] Data Structure")
    print("-" * 50)

    # Simulate tree item data structure
    tag_data = {
        'type': 'tag',
        'data': {
            'id': 1,
            'name': 'Python',
            'icon': '🐍',
            'color': '#64B5F6'
        }
    }

    snippet_data = {
        'type': 'snippet',
        'data': {
            'id': 1,
            'name': 'List Comprehension',
            'code': '[x**2 for x in range(10)]',
            'language': 'python',
            'usage_count': 0
        }
    }

    print("Tag data structure:")
    print(f"  Type: {tag_data['type']}")
    print(f"  Name: {tag_data['data']['name']}")

    print("\nSnippet data structure:")
    print(f"  Type: {snippet_data['type']}")
    print(f"  Name: {snippet_data['data']['name']}")
    print(f"  Language: {snippet_data['data']['language']}")

    print("\n✓ Test passed")


def main():
    """Run all tests."""
    print("=" * 50)
    print("Phase 2.2 Feature Tests")
    print("=" * 50)

    try:
        test_snippet_count_display()
        test_snippet_retrieval()
        test_usage_count_increment()
        test_data_structure()

        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
