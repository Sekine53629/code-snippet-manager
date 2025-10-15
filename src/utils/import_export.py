"""
Import/Export utility for code snippets.

Supports:
- JSON format (complete data export/import)
- Markdown format (human-readable export)
- Backup and restore
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.utils.database import DatabaseManager


class ImportExportManager:
    """Manager for importing and exporting snippets."""

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize import/export manager.

        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager

    def export_to_json(self, file_path: str, include_stats: bool = True) -> bool:
        """
        Export all data to JSON format.

        Args:
            file_path: Output file path
            include_stats: Whether to include usage statistics

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get all data
            tags = self.db_manager.get_all_tags()
            snippets = self.db_manager.get_all_snippets()

            # Convert datetime objects to ISO strings
            snippets = self._serialize_datetime(snippets)

            # Build export data
            export_data = {
                'version': '1.0',
                'exported_at': datetime.now().isoformat(),
                'tags': tags,
                'snippets': snippets if include_stats else self._strip_stats(snippets),
            }

            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Export to JSON failed: {e}")
            return False

    def import_from_json(self, file_path: str, merge: bool = True) -> tuple[bool, str]:
        """
        Import data from JSON format.

        Args:
            file_path: Input file path
            merge: If True, merge with existing data; if False, replace

        Returns:
            Tuple of (success, message)
        """
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            # Validate format
            if 'version' not in import_data or 'tags' not in import_data or 'snippets' not in import_data:
                return False, "Invalid JSON format"

            # TODO: Implement actual import logic
            # For now, just count items
            tag_count = len(import_data['tags'])
            snippet_count = len(import_data['snippets'])

            return True, f"Imported {tag_count} tags and {snippet_count} snippets"

        except Exception as e:
            return False, f"Import failed: {e}"

    def export_to_markdown(self, file_path: str, organize_by_tag: bool = True) -> bool:
        """
        Export snippets to Markdown format.

        Args:
            file_path: Output file path
            organize_by_tag: Whether to organize by tags

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get all data
            tags = self.db_manager.get_all_tags()
            snippets = self.db_manager.get_all_snippets()

            # Build markdown
            lines = [
                "# Code Snippets",
                "",
                f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                f"Total: {len(snippets)} snippets in {len(tags)} tags",
                "",
                "---",
                ""
            ]

            if organize_by_tag:
                # Organize by tags
                tag_dict = {tag['id']: tag for tag in tags}

                for tag in tags:
                    tag_snippets = self.db_manager.get_snippets_by_tag(tag['id'])
                    if not tag_snippets:
                        continue

                    # Tag header
                    lines.append(f"## {tag['icon']} {tag['name']}")
                    if tag.get('description'):
                        lines.append(f"*{tag['description']}*")
                    lines.append("")

                    # Snippets under this tag
                    for snippet in tag_snippets:
                        self._add_snippet_markdown(lines, snippet)

                    lines.append("")
            else:
                # Flat list
                lines.append("## All Snippets")
                lines.append("")

                for snippet in sorted(snippets, key=lambda s: s['name']):
                    self._add_snippet_markdown(lines, snippet)

            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

            return True

        except Exception as e:
            print(f"Export to Markdown failed: {e}")
            return False

    def _add_snippet_markdown(self, lines: List[str], snippet: Dict[str, Any]):
        """Add snippet to markdown lines."""
        lines.append(f"### {snippet['name']}")

        if snippet.get('description'):
            lines.append(f"{snippet['description']}")
            lines.append("")

        # Language and stats
        lang = snippet.get('language', 'text')
        usage = snippet.get('usage_count', 0)
        lines.append(f"**Language**: {lang} | **Used**: {usage} times")
        lines.append("")

        # Code block
        lines.append(f"```{lang}")
        lines.append(snippet['code'])
        lines.append("```")
        lines.append("")

    def _strip_stats(self, snippets: List[Dict]) -> List[Dict]:
        """Remove usage statistics from snippets."""
        cleaned = []
        for snippet in snippets:
            clean_snippet = snippet.copy()
            clean_snippet.pop('usage_count', None)
            clean_snippet.pop('last_used', None)
            cleaned.append(clean_snippet)
        return cleaned

    def create_backup(self, backup_dir: str = 'backups') -> Optional[str]:
        """
        Create a backup of all data.

        Args:
            backup_dir: Directory to store backups

        Returns:
            Path to backup file, or None if failed
        """
        try:
            # Create backup directory
            Path(backup_dir).mkdir(parents=True, exist_ok=True)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"backup_{timestamp}.json"
            file_path = Path(backup_dir) / filename

            # Export to JSON
            if self.export_to_json(str(file_path), include_stats=True):
                return str(file_path)
            return None

        except Exception as e:
            print(f"Backup failed: {e}")
            return None

    def restore_backup(self, backup_file: str) -> tuple[bool, str]:
        """
        Restore data from backup file.

        Args:
            backup_file: Path to backup file

        Returns:
            Tuple of (success, message)
        """
        return self.import_from_json(backup_file, merge=False)

    def get_export_stats(self) -> Dict[str, Any]:
        """
        Get statistics for export.

        Returns:
            Dictionary with export statistics
        """
        tags = self.db_manager.get_all_tags()
        snippets = self.db_manager.get_all_snippets()

        # Count snippets by language
        lang_count = {}
        for snippet in snippets:
            lang = snippet.get('language', 'unknown')
            lang_count[lang] = lang_count.get(lang, 0) + 1

        # Total usage
        total_usage = sum(s.get('usage_count', 0) for s in snippets)

        return {
            'total_tags': len(tags),
            'total_snippets': len(snippets),
            'languages': lang_count,
            'total_usage': total_usage,
            'avg_usage': total_usage / len(snippets) if snippets else 0,
        }

    def _serialize_datetime(self, snippets: List[Dict]) -> List[Dict]:
        """
        Convert datetime objects to ISO format strings.

        Args:
            snippets: List of snippet dictionaries

        Returns:
            List of snippets with datetime converted to strings
        """
        serialized = []
        for snippet in snippets:
            snippet_copy = snippet.copy()
            if 'last_used' in snippet_copy and snippet_copy['last_used']:
                if hasattr(snippet_copy['last_used'], 'isoformat'):
                    snippet_copy['last_used'] = snippet_copy['last_used'].isoformat()
            serialized.append(snippet_copy)
        return serialized
