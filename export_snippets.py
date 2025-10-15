#!/usr/bin/env python3
"""
Export Snippets to JSON

Exports all snippets and tags from the database to a JSON file
for backup or transfer to another environment.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.config import load_config
from utils.database import DatabaseManager


def export_snippets_to_json(db_manager: DatabaseManager, output_file: str):
    """Export all snippets and tags to JSON file.

    Args:
        db_manager: Database manager instance
        output_file: Output JSON file path
    """
    print("=" * 60)
    print("Exporting snippets and tags to JSON...")
    print("=" * 60)

    # Get all data
    print("\n📦 Fetching data from database...")
    all_tags = db_manager.get_all_tags()
    all_snippets = db_manager.get_all_snippets()

    print(f"   Tags found: {len(all_tags)}")
    print(f"   Snippets found: {len(all_snippets)}")

    # Build export data structure
    export_data = {
        "metadata": {
            "exported_at": datetime.now().isoformat(),
            "version": "1.0",
            "total_tags": len(all_tags),
            "total_snippets": len(all_snippets)
        },
        "tags": [],
        "snippets": []
    }

    # Export tags
    print("\n🏷️  Processing tags...")
    for tag in all_tags:
        tag_data = {
            "id": tag['id'],
            "name": tag['name'],
            "icon": tag['icon'],
            "color": tag['color'],
            "parent_id": tag['parent_id'],
            "type": tag.get('type', 'folder')
        }
        export_data['tags'].append(tag_data)

    # Export snippets with their tag associations
    print("📄 Processing snippets...")
    for snippet in all_snippets:
        # Get tags for this snippet
        with db_manager.get_local_session() as session:
            from models.models import Snippet, TagSnippet
            db_snippet = session.query(Snippet).filter(Snippet.id == snippet['id']).first()

            tag_ids = []
            if db_snippet:
                tag_snippets = session.query(TagSnippet).filter(
                    TagSnippet.snippet_id == db_snippet.id
                ).all()
                tag_ids = [ts.tag_id for ts in tag_snippets]

        snippet_data = {
            "name": snippet['name'],
            "code": snippet['code'],
            "language": snippet.get('language'),
            "description": snippet.get('description'),
            "tag_ids": tag_ids,
            "usage_count": snippet.get('usage_count', 0),
            "created_at": snippet.get('created_at').isoformat() if snippet.get('created_at') else None,
            "updated_at": snippet.get('updated_at').isoformat() if snippet.get('updated_at') else None
        }
        export_data['snippets'].append(snippet_data)

    # Write to JSON file
    print(f"\n💾 Writing to {output_file}...")
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    file_size = output_path.stat().st_size
    file_size_kb = file_size / 1024

    print(f"✅ Export complete!")
    print(f"   File: {output_file}")
    print(f"   Size: {file_size_kb:.2f} KB")
    print(f"   Tags: {len(export_data['tags'])}")
    print(f"   Snippets: {len(export_data['snippets'])}")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Code Snippet Manager - Export Tool")
    print("=" * 60)

    # Default output file
    default_output = f"snippets_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Get output file from command line or use default
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    else:
        output_file = default_output

    print(f"\nOutput file: {output_file}")

    # Load configuration
    config = load_config()

    # Initialize database
    db_manager = DatabaseManager(config)

    # Export snippets
    export_snippets_to_json(db_manager, output_file)

    print("\n✅ Done!")
    print(f"\nTo import in another environment:")
    print(f"  python import_snippets.py {output_file}")


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
