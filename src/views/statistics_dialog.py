"""
Statistics dialog for usage analytics.

Displays:
- Most used snippets
- Language distribution
- Usage trends
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QGroupBox, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.utils.database import DatabaseManager
from typing import List, Dict


class StatisticsDialog(QDialog):
    """Dialog for displaying usage statistics."""

    def __init__(self, db_manager: DatabaseManager, parent=None):
        """
        Initialize statistics dialog.

        Args:
            db_manager: Database manager instance
            parent: Parent widget
        """
        super().__init__(parent)

        self.db_manager = db_manager

        self.setWindowTitle("Usage Statistics")
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)

        self._setup_ui()
        self._load_statistics()

    def _setup_ui(self):
        """Setup user interface."""
        layout = QVBoxLayout()

        # Summary section
        summary_group = QGroupBox("Summary")
        summary_layout = QVBoxLayout()

        self.summary_label = QLabel()
        self.summary_label.setFont(QFont("Arial", 11))
        summary_layout.addWidget(self.summary_label)

        summary_group.setLayout(summary_layout)
        layout.addWidget(summary_group)

        # Most used snippets
        most_used_group = QGroupBox("Most Used Snippets (Top 10)")
        most_used_layout = QVBoxLayout()

        self.most_used_table = QTableWidget()
        self.most_used_table.setColumnCount(4)
        self.most_used_table.setHorizontalHeaderLabels(["Name", "Language", "Usage Count", "Last Used"])
        self.most_used_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.most_used_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.most_used_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        most_used_layout.addWidget(self.most_used_table)
        most_used_group.setLayout(most_used_layout)
        layout.addWidget(most_used_group)

        # Language distribution
        lang_group = QGroupBox("Language Distribution")
        lang_layout = QVBoxLayout()

        self.lang_table = QTableWidget()
        self.lang_table.setColumnCount(3)
        self.lang_table.setHorizontalHeaderLabels(["Language", "Snippet Count", "Total Usage"])
        self.lang_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.lang_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.lang_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        lang_layout.addWidget(self.lang_table)
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)

        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Apply dark theme
        self._apply_theme()

    def _apply_theme(self):
        """Apply dark theme to dialog."""
        self.setStyleSheet("""
            QDialog {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QGroupBox {
                border: 1px solid #444444;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #FFFFFF;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                padding: 0 5px;
                color: #64B5F6;
            }
            QLabel {
                color: #CCCCCC;
            }
            QTableWidget {
                background-color: #1E1E1E;
                border: 1px solid #444444;
                color: #FFFFFF;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #1976D2;
            }
            QHeaderView::section {
                background-color: #3C3C3C;
                color: #FFFFFF;
                padding: 5px;
                border: 1px solid #444444;
            }
            QPushButton {
                background-color: #3C3C3C;
                border: 1px solid #444444;
                border-radius: 3px;
                padding: 5px 15px;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #4C4C4C;
            }
        """)

    def _load_statistics(self):
        """Load and display statistics."""
        # Get all snippets
        snippets = self.db_manager.get_all_snippets()

        # Calculate summary
        total_snippets = len(snippets)
        total_usage = sum(s.get('usage_count', 0) for s in snippets)
        avg_usage = total_usage / total_snippets if total_snippets > 0 else 0

        # Get tags count
        tags = self.db_manager.get_all_tags()
        total_tags = len(tags)

        # Update summary label
        summary_text = (
            f"<b>Total Snippets:</b> {total_snippets}<br>"
            f"<b>Total Tags:</b> {total_tags}<br>"
            f"<b>Total Usage:</b> {total_usage} times<br>"
            f"<b>Average Usage:</b> {avg_usage:.1f} times per snippet"
        )
        self.summary_label.setText(summary_text)

        # Load most used snippets
        self._load_most_used(snippets)

        # Load language distribution
        self._load_language_distribution(snippets)

    def _load_most_used(self, snippets: List[Dict]):
        """Load most used snippets table."""
        # Sort by usage count
        sorted_snippets = sorted(
            snippets,
            key=lambda s: s.get('usage_count', 0),
            reverse=True
        )[:10]

        self.most_used_table.setRowCount(len(sorted_snippets))

        for row, snippet in enumerate(sorted_snippets):
            # Name
            name_item = QTableWidgetItem(snippet.get('name', 'Unnamed'))
            self.most_used_table.setItem(row, 0, name_item)

            # Language
            lang_item = QTableWidgetItem(snippet.get('language', 'text'))
            self.most_used_table.setItem(row, 1, lang_item)

            # Usage count
            usage_item = QTableWidgetItem(str(snippet.get('usage_count', 0)))
            usage_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.most_used_table.setItem(row, 2, usage_item)

            # Last used
            last_used = snippet.get('last_used', 'Never')
            if last_used and last_used != 'Never':
                # Format datetime
                try:
                    from datetime import datetime
                    # Handle both datetime objects and ISO strings
                    if hasattr(last_used, 'strftime'):
                        last_used = last_used.strftime('%Y-%m-%d %H:%M')
                    else:
                        dt = datetime.fromisoformat(last_used)
                        last_used = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    last_used = str(last_used)
            else:
                last_used = 'Never'

            last_used_item = QTableWidgetItem(str(last_used))
            self.most_used_table.setItem(row, 3, last_used_item)

    def _load_language_distribution(self, snippets: List[Dict]):
        """Load language distribution table."""
        # Count by language
        lang_stats = {}
        for snippet in snippets:
            lang = snippet.get('language', 'text')
            if lang not in lang_stats:
                lang_stats[lang] = {'count': 0, 'usage': 0}

            lang_stats[lang]['count'] += 1
            lang_stats[lang]['usage'] += snippet.get('usage_count', 0)

        # Sort by snippet count
        sorted_langs = sorted(
            lang_stats.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )

        self.lang_table.setRowCount(len(sorted_langs))

        for row, (lang, stats) in enumerate(sorted_langs):
            # Language
            lang_item = QTableWidgetItem(lang)
            self.lang_table.setItem(row, 0, lang_item)

            # Snippet count
            count_item = QTableWidgetItem(str(stats['count']))
            count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lang_table.setItem(row, 1, count_item)

            # Total usage
            usage_item = QTableWidgetItem(str(stats['usage']))
            usage_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lang_table.setItem(row, 2, usage_item)
