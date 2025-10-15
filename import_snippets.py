#!/usr/bin/env python3
"""
Import Snippets from JSON

Imports snippets and tags from a JSON file exported by export_snippets.py.
"""

import sys
import json
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.config import load_config
from utils.database import DatabaseManager


def import_snippets_from_json(db_manager: DatabaseManager, input_file: str, merge: bool = False):
    """Import snippets and tags from JSON file.

    Args:
        db_manager: Database manager instance
        input_file: Input JSON file path
        merge: If True, merge with existing data. If False, clear database first.
    """
    print("=" * 60)
    print("Importing snippets and tags from JSON...")
    print("=" * 60)

    # Read JSON file
    print(f"\n📖 Reading {input_file}...")
    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_file}")

    with open(input_path, 'r', encoding='utf-8') as f:
        import_data = json.load(f)

    # Display metadata
    metadata = import_data.get('metadata', {})
    print(f"\n📊 Import file metadata:")
    print(f"   Exported at: {metadata.get('exported_at', 'Unknown')}")
    print(f"   Version: {metadata.get('version', 'Unknown')}")
    print(f"   Tags: {metadata.get('total_tags', 0)}")
    print(f"   Snippets: {metadata.get('total_snippets', 0)}")

    # Confirm import
    if not merge:
        print("\n⚠️  WARNING: This will CLEAR all existing data!")
        response = input("Continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Import cancelled.")
            return
    else:
        print("\n🔄 Merge mode: Existing data will be preserved.")

    # Clear database if not merging
    if not merge:
        print("\n🗑️  Clearing existing data...")
        with db_manager.get_local_session() as session:
            from models.models import Tag, Snippet, TagSnippet
            session.query(TagSnippet).delete()
            session.query(Snippet).delete()
            session.query(Tag).delete()
            session.commit()
        print("   ✓ Database cleared")

    # Import tags
    print("\n🏷️  Importing tags...")
    tags = import_data.get('tags', [])
    tag_id_mapping = {}  # old_id -> new_id

    for tag_data in tags:
        old_id = tag_data.get('id')
        name = tag_data['name']
        icon = tag_data.get('icon', '📁')
        color = tag_data.get('color', '#FFFFFF')
        parent_id = tag_data.get('parent_id')
        tag_type = tag_data.get('type', 'folder')

        # Create or get tag (without icon and color parameters)
        new_id = db_manager.get_or_create_tag(
            name=name,
            parent_id=None,  # Will update parent later
            tag_type=tag_type
        )

        # Update icon and color separately
        with db_manager.get_local_session() as session:
            from models.models import Tag
            tag = session.query(Tag).filter(Tag.id == new_id).first()
            if tag:
                tag.icon = icon
                tag.color = color
                session.commit()

        tag_id_mapping[old_id] = new_id
        print(f"   ✓ {icon} {name} (ID: {old_id} -> {new_id})")

    # Update parent relationships
    print("\n🔗 Updating tag hierarchy...")
    for tag_data in tags:
        old_id = tag_data.get('id')
        old_parent_id = tag_data.get('parent_id')

        if old_parent_id is not None:
            new_id = tag_id_mapping.get(old_id)
            new_parent_id = tag_id_mapping.get(old_parent_id)

            if new_id and new_parent_id:
                with db_manager.get_local_session() as session:
                    from models.models import Tag
                    tag = session.query(Tag).filter(Tag.id == new_id).first()
                    if tag:
                        tag.parent_id = new_parent_id
                        session.commit()
                        print(f"   ✓ Updated parent for tag ID {new_id}")

    # Import snippets
    print("\n📄 Importing snippets...")
    snippets = import_data.get('snippets', [])
    imported_count = 0

    for snippet_data in snippets:
        name = snippet_data['name']
        code = snippet_data['code']
        language = snippet_data.get('language')
        description = snippet_data.get('description')
        old_tag_ids = snippet_data.get('tag_ids', [])

        # Map old tag IDs to new tag IDs
        new_tag_ids = []
        for old_tag_id in old_tag_ids:
            new_tag_id = tag_id_mapping.get(old_tag_id)
            if new_tag_id:
                new_tag_ids.append(new_tag_id)

        # Add snippet
        try:
            db_manager.add_snippet(
                name=name,
                code=code,
                language=language,
                description=description,
                tag_ids=new_tag_ids
            )
            imported_count += 1
            print(f"   ✓ {name} ({language}) - {len(new_tag_ids)} tags")
        except Exception as e:
            print(f"   ✗ Failed to import '{name}': {e}")

    print(f"\n✅ Import complete!")
    print(f"   Tags imported: {len(tags)}")
    print(f"   Snippets imported: {imported_count}/{len(snippets)}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Code Snippet Manager - Import Tool")
    print("=" * 60)

    # Get input file from command line
    if len(sys.argv) < 2:
        print("\nUsage: python import_snippets.py <input_file.json> [--merge]")
        print("\nOptions:")
        print("  --merge    Merge with existing data (default: replace)")
        sys.exit(1)

    input_file = sys.argv[1]
    merge = '--merge' in sys.argv

    print(f"\nInput file: {input_file}")
    print(f"Mode: {'Merge' if merge else 'Replace'}")

    # Load configuration
    config = load_config()

    # Initialize database
    db_manager = DatabaseManager(config)

    # Import snippets
    import_snippets_from_json(db_manager, input_file, merge)

    print("\n✅ Done!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
