"""Code Snippet Manager - Main Entry Point

A modern, beautiful code snippet manager with hierarchical organization.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.utils.config import load_config, save_config
from src.utils.database import DatabaseManager
from src.models.models import Tag, Snippet


def initialize_sample_data(db_manager: DatabaseManager):
    """Initialize sample data for testing.

    Args:
        db_manager: Database manager instance.
    """
    print("\n=== Initializing sample data ===")

    # Create sample tags (returns tag IDs)
    python_tag_id = db_manager.get_or_create_tag("Python", tag_type="folder")
    js_tag_id = db_manager.get_or_create_tag("JavaScript", tag_type="folder")

    # Python subtags
    django_tag_id = db_manager.get_or_create_tag("Django", parent_id=python_tag_id, tag_type="folder")
    flask_tag_id = db_manager.get_or_create_tag("Flask", parent_id=python_tag_id, tag_type="folder")

    # JavaScript subtags
    react_tag_id = db_manager.get_or_create_tag("React", parent_id=js_tag_id, tag_type="folder")

    # Create sample snippets
    snippets_data = [
        {
            "name": "List Comprehension",
            "code": "[x**2 for x in range(10)]",
            "language": "python",
            "description": "Create a list of squares using list comprehension",
            "tag_ids": [python_tag_id]
        },
        {
            "name": "Django Model Example",
            "code": """from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title""",
            "language": "python",
            "description": "Basic Django model with common fields",
            "tag_ids": [django_tag_id]
        },
        {
            "name": "Flask Route",
            "code": """@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())""",
            "language": "python",
            "description": "Flask route with URL parameter",
            "tag_ids": [flask_tag_id]
        },
        {
            "name": "React useState Hook",
            "code": """const [count, setCount] = useState(0);

const increment = () => {
  setCount(prevCount => prevCount + 1);
};""",
            "language": "javascript",
            "description": "Basic usage of React useState hook",
            "tag_ids": [react_tag_id]
        }
    ]

    for snippet_data in snippets_data:
        db_manager.add_snippet(**snippet_data)

    print("✓ Sample data initialized successfully")


def test_database_operations(db_manager: DatabaseManager):
    """Test basic database operations.

    Args:
        db_manager: Database manager instance.
    """
    print("\n=== Testing database operations ===")

    # Get all tags
    tags = db_manager.get_all_tags()
    print(f"\nFound {len(tags)} tags:")
    for tag in tags:
        path_parts = tag['full_path'].split(' > ')
        indent = "  " * (len(path_parts) - 1)
        print(f"{indent}{tag['icon']} {tag['name']} ({tag['type']})")

    # Search snippets
    print("\n--- Searching for 'Flask' ---")
    results = db_manager.search_snippets("Flask")
    print(f"Found {len(results)} results:")
    for snippet in results:
        print(f"  • {snippet['name']} ({snippet['language']}) - Source: {snippet['source']}")
        if snippet['description']:
            print(f"    {snippet['description'][:60]}...")

    # Get snippets by tag
    print("\n--- Getting Python snippets ---")
    python_tag = tags[0] if tags else None
    if python_tag:
        snippets = db_manager.get_snippets_by_tag(python_tag['id'])
        print(f"Found {len(snippets)} Python snippets:")
        for snippet in snippets:
            print(f"  • {snippet['name']}")


def main():
    """Main application entry point."""
    print("=" * 60)
    print("Code Snippet Manager - Testing Foundation")
    print("=" * 60)

    # Load configuration
    print("\n[1] Loading configuration...")
    config = load_config()
    print(f"✓ Configuration loaded")
    print(f"  Database mode: {config.database.mode}")
    print(f"  Window position: {config.appearance.position}")
    print(f"  Theme: {config.appearance.theme}")

    # Initialize database
    print("\n[2] Initializing database...")
    db_manager = DatabaseManager(config)
    print(f"✓ Database initialized")

    # Check if database is empty
    with db_manager.get_local_session() as session:
        tag_count = session.query(Tag).count()
        snippet_count = session.query(Snippet).count()

    print(f"  Tags: {tag_count}")
    print(f"  Snippets: {snippet_count}")

    # Initialize sample data if empty
    if tag_count == 0:
        initialize_sample_data(db_manager)

    # Test operations
    test_database_operations(db_manager)

    # Clean up
    db_manager.close()

    print("\n" + "=" * 60)
    print("Foundation test completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Implement GUI (GadgetWindow)")
    print("  2. Add hotkey support")
    print("  3. Implement clipboard operations")
    print("  4. Add search functionality")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
