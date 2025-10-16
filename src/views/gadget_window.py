"""Gadget-style main window for Code Snippet Manager.

This module implements a semi-transparent, edge-docked window with smooth animations.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QTextEdit, QLineEdit,
    QPushButton, QLabel, QSplitter, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QFont, QAction

from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.config import Config
from src.utils.database import DatabaseManager
from src.utils.fuzzy_search import fuzzy_search_snippets, fuzzy_search_tags
from src.views.snippet_dialog import SnippetDialog
from src.views.code_highlighter import apply_highlighter, normalize_language


class GadgetWindow(QMainWindow):
    """Main gadget window with semi-transparent UI.

    Features:
    - Semi-transparent background
    - Docked to screen edge (left or right)
    - Smooth fade in/out animations
    - Always on top
    - Frameless window style
    """

    # Signals
    snippet_selected = pyqtSignal(dict)  # Emitted when snippet is selected
    tag_selected = pyqtSignal(dict)  # Emitted when tag is selected

    def __init__(self, config: Config, db_manager: DatabaseManager):
        """Initialize the gadget window.

        Args:
            config: Application configuration.
            db_manager: Database manager instance.
        """
        super().__init__()

        self.config = config
        self.db_manager = db_manager

        # State
        self.is_visible = False
        self.is_minimized = False
        self.is_always_on_top = True  # Default: always on top
        self.normal_height = None  # Store normal height for minimize/restore

        # Setup UI
        self._setup_window()
        self._setup_ui()
        self._setup_animations()
        self._apply_rounded_mask()
        self._load_data()

    def _setup_window(self):
        """Configure window properties."""
        # Window flags
        # Note: Qt.WindowType.Tool removed - it conflicts with WindowStaysOnTopHint on macOS
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        # Transparency
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Use opacity_active for better readability (opacity_inactive is too transparent)
        self.setWindowOpacity(self.config.appearance.opacity_active)

        # Size
        self.setFixedWidth(self.config.appearance.width)
        self.setMinimumHeight(self.config.appearance.height_min)
        self.setMaximumHeight(self.config.appearance.height_max)

        # Position
        self._position_window()

    def _position_window(self):
        """Position window at screen edge based on config."""
        from PyQt6.QtGui import QGuiApplication

        screen = QGuiApplication.primaryScreen().geometry()

        if self.config.appearance.position == 'right':
            # Right edge
            x = screen.width() - self.width() - self.config.appearance.offset_x
        else:
            # Left edge
            x = self.config.appearance.offset_x

        # Vertical center with offset
        y = (screen.height() - self.height()) // 2 + self.config.appearance.offset_y

        self.move(x, y)

    def _setup_ui(self):
        """Create and layout UI components."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Apply rounded corners to central widget for rounded window effect
        central.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border-radius: 20px;
            }
        """)

        # Main layout
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(5)

        # Header
        self._create_header(layout)

        # Search bar
        self._create_search_bar(layout)

        # Main content (splitter)
        self._create_content_area(layout)

        # Footer
        self._create_footer(layout)

        # Apply theme
        self._apply_theme()

    def _create_header(self, parent_layout):
        """Create header with title and controls.

        Args:
            parent_layout: Parent layout to add header to.
        """
        header = QHBoxLayout()

        # Title
        title = QLabel("Code Snippet Manager")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #FFFFFF;")
        header.addWidget(title)

        header.addStretch()

        # macOS-style window buttons container
        button_container = QHBoxLayout()
        button_container.setSpacing(8)

        # Close button (Red) - 閉じる
        self.btn_close = QPushButton()
        self.btn_close.setFixedSize(14, 14)
        self.btn_close.clicked.connect(self.close_application)
        self.btn_close.setToolTip("アプリケーションを終了")
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 95, 86, 255);
                border: 1px solid rgba(200, 75, 66, 255);
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: rgba(255, 95, 86, 255);
                border: 1px solid rgba(100, 40, 35, 255);
            }
            QPushButton:pressed {
                background-color: rgba(200, 75, 66, 255);
            }
        """)
        button_container.addWidget(self.btn_close)

        # Minimize button (Yellow) - 最小化
        self.btn_minimize = QPushButton()
        self.btn_minimize.setFixedSize(14, 14)
        self.btn_minimize.clicked.connect(self.toggle_minimize)
        self.btn_minimize.setToolTip("ウィンドウを最小化/復元")
        self.btn_minimize.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_minimize.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 189, 68, 255);
                border: 1px solid rgba(200, 150, 50, 255);
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: rgba(255, 189, 68, 255);
                border: 1px solid rgba(120, 90, 30, 255);
            }
            QPushButton:pressed {
                background-color: rgba(200, 150, 50, 255);
            }
        """)
        button_container.addWidget(self.btn_minimize)

        # Always on top button (Green) - 常に最前面
        self.btn_always_on_top = QPushButton()
        self.btn_always_on_top.setFixedSize(14, 14)
        self.btn_always_on_top.clicked.connect(self.toggle_always_on_top)
        self.btn_always_on_top.setToolTip("常に最前面に固定/解除")
        self.btn_always_on_top.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_always_on_top.setStyleSheet("""
            QPushButton {
                background-color: rgba(40, 205, 65, 255);
                border: 1px solid rgba(30, 160, 50, 255);
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: rgba(40, 205, 65, 255);
                border: 1px solid rgba(20, 100, 35, 255);
            }
            QPushButton:pressed {
                background-color: rgba(30, 160, 50, 255);
            }
        """)
        button_container.addWidget(self.btn_always_on_top)

        header.addLayout(button_container)

        parent_layout.addLayout(header)

    def _create_search_bar(self, parent_layout):
        """Create search input.

        Args:
            parent_layout: Parent layout to add search bar to.
        """
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search snippets...")
        self.search_input.textChanged.connect(self._on_search_changed)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #2E2E2E;
                color: white;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #64B5F6;
            }
        """)
        parent_layout.addWidget(self.search_input)

    def _create_content_area(self, parent_layout):
        """Create main content area with tree and preview.

        Args:
            parent_layout: Parent layout to add content to.
        """
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemClicked.connect(self._on_item_clicked)
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        # Style is now managed globally in main.py
        splitter.addWidget(self.tree)

        # Preview panel
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText("Select a snippet to preview...")
        # Style is now managed globally in main.py

        # Initialize syntax highlighter
        self.highlighter = None
        self.current_language = 'text'

        splitter.addWidget(self.preview)

        # Set initial sizes
        splitter.setSizes([250, 150])

        parent_layout.addWidget(splitter, 1)

    def _create_footer(self, parent_layout):
        """Create footer with status and actions.

        Args:
            parent_layout: Parent layout to add footer to.
        """
        footer = QHBoxLayout()

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #888888; font-size: 11px;")
        footer.addWidget(self.status_label)

        footer.addStretch()

        # Action buttons
        btn_new = QPushButton("+ New")
        btn_new.clicked.connect(self._create_new_snippet)
        btn_new.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px 15px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #2196F3;
            }
        """)
        footer.addWidget(btn_new)

        parent_layout.addLayout(footer)

    def _apply_theme(self):
        """Apply theme based on config."""
        if self.config.appearance.theme == 'dark':
            self.setStyleSheet("""
                QMainWindow {
                    background-color: rgba(30, 30, 30, 240);
                    border: 1px solid #444444;
                    border-radius: 10px;
                }
            """)
        else:
            # Light theme (future implementation)
            pass

    def _apply_rounded_mask(self):
        """Apply rounded corners mask to window."""
        from PyQt6.QtGui import QPainterPath, QRegion

        # Create a rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 20, 20)

        # Create region from path and set as mask
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        """Handle window resize events to reapply rounded mask."""
        super().resizeEvent(event)
        self._apply_rounded_mask()

    def _setup_animations(self):
        """Setup animation effects."""
        # Opacity animation
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(self.config.appearance.opacity_transition)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def _load_data(self):
        """Load tags and snippets from database."""
        self.tree.clear()

        # Get all tags
        tags = self.db_manager.get_all_tags()

        # Build tree structure
        self._build_tree(tags)

        # Update status
        self.status_label.setText(f"{len(tags)} tags loaded")

    def _build_tree(self, tags):
        """Build tree widget from tag data with snippets.

        Args:
            tags: List of tag dictionaries.
        """
        # Create a mapping of tag_id -> QTreeWidgetItem
        tag_items = {}
        root_items = []

        # First pass: create tag items
        for tag in tags:
            # Get snippets for this tag
            snippets = self.db_manager.get_snippets_by_tag(tag['id'])
            snippet_count = len(snippets)

            # Create tag item with snippet count
            item = QTreeWidgetItem()
            if snippet_count > 0:
                item.setText(0, f"{tag['icon']} {tag['name']} ({snippet_count})")
            else:
                item.setText(0, f"{tag['icon']} {tag['name']}")

            # Store tag data
            item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'tag', 'data': tag})

            # Set color
            color = QColor(tag['color'])
            item.setForeground(0, color)

            # Add snippet children
            for snippet in snippets:
                snippet_item = QTreeWidgetItem()
                # Display name in first line
                name = snippet['name']
                snippet_item.setText(0, f"  📄 {name}")
                snippet_item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'snippet', 'data': snippet})

                # Set snippet color (lighter)
                snippet_color = QColor("#AAAAAA")
                snippet_item.setForeground(0, snippet_color)

                # Add description as child item (second line)
                desc = snippet.get('description', '')
                if desc:
                    desc_short = desc if len(desc) <= 50 else desc[:47] + '...'
                    desc_item = QTreeWidgetItem()
                    desc_item.setText(0, f"     {desc_short}")
                    desc_item.setForeground(0, QColor("#888888"))  # Even lighter gray
                    desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)  # Non-selectable
                    snippet_item.addChild(desc_item)

                # Add usage count tooltip
                if snippet['usage_count'] > 0:
                    snippet_item.setToolTip(0, f"Used {snippet['usage_count']} times")

                item.addChild(snippet_item)

            tag_items[tag['id']] = item

            if tag['parent_id'] is None:
                root_items.append(item)

        # Second pass: build tag hierarchy
        for tag in tags:
            if tag['parent_id'] is not None and tag['parent_id'] in tag_items:
                parent_item = tag_items[tag['parent_id']]
                parent_item.addChild(tag_items[tag['id']])

        # Add root items to tree
        self.tree.addTopLevelItems(root_items)

        # Expand all
        self.tree.expandAll()

    def _on_search_changed(self, text: str):
        """Handle search input changes with fuzzy matching.

        Args:
            text: Search query text.
        """
        if not text:
            # No search query - show all data
            self._load_data()
            return

        # Get all snippets and tags
        all_snippets = self.db_manager.get_all_snippets()
        all_tags = self.db_manager.get_all_tags()

        # Perform fuzzy search
        snippet_results = fuzzy_search_snippets(text, all_snippets, threshold=0.3)
        tag_results = fuzzy_search_tags(text, all_tags, threshold=0.3)

        # Build filtered tree
        self._build_search_results(snippet_results, tag_results, text)

        total_results = len(snippet_results) + len(tag_results)
        self.status_label.setText(f"Found {total_results} results for '{text}'")

    def _build_search_results(self, snippet_results, tag_results, query):
        """Build tree widget from search results.

        Args:
            snippet_results: List of (snippet, score) tuples
            tag_results: List of (tag, score) tuples
            query: Search query for highlighting
        """
        self.tree.clear()

        # Add matching tags
        if tag_results:
            tags_root = QTreeWidgetItem()
            tags_root.setText(0, f"📁 Matching Tags ({len(tag_results)})")
            tags_root.setForeground(0, QColor("#FFEB3B"))  # Yellow
            self.tree.addTopLevelItem(tags_root)

            for tag, score in tag_results:
                tag_item = QTreeWidgetItem()
                score_pct = int(score * 100)
                tag_item.setText(0, f"{tag['icon']} {tag['name']} ({score_pct}%)")
                tag_item.setData(0, Qt.ItemDataRole.UserRole, {'type': 'tag', 'data': tag})

                # Set color based on score
                if score > 0.7:
                    color = QColor("#4CAF50")  # Green - high match
                elif score > 0.5:
                    color = QColor("#FFC107")  # Amber - medium match
                else:
                    color = QColor("#FF9800")  # Orange - low match
                tag_item.setForeground(0, color)

                # Add snippets from this tag
                snippets = self.db_manager.get_snippets_by_tag(tag['id'])
                for snippet in snippets:
                    snippet_item = QTreeWidgetItem()
                    # Display name in first line
                    name = snippet['name']
                    snippet_item.setText(0, f"  📄 {name}")
                    snippet_item.setData(0, Qt.ItemDataRole.UserRole,
                                       {'type': 'snippet', 'data': snippet})
                    snippet_item.setForeground(0, QColor("#AAAAAA"))

                    # Add description as child item (second line)
                    desc = snippet.get('description', '')
                    if desc:
                        desc_short = desc if len(desc) <= 50 else desc[:47] + '...'
                        desc_item = QTreeWidgetItem()
                        desc_item.setText(0, f"     {desc_short}")
                        desc_item.setForeground(0, QColor("#888888"))
                        desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                        snippet_item.addChild(desc_item)

                    tag_item.addChild(snippet_item)

                tags_root.addChild(tag_item)

            tags_root.setExpanded(True)

        # Add matching snippets
        if snippet_results:
            snippets_root = QTreeWidgetItem()
            snippets_root.setText(0, f"📄 Matching Snippets ({len(snippet_results)})")
            snippets_root.setForeground(0, QColor("#64B5F6"))  # Light blue
            self.tree.addTopLevelItem(snippets_root)

            for snippet, score in snippet_results:
                snippet_item = QTreeWidgetItem()
                score_pct = int(score * 100)
                lang = snippet.get('language', 'text')
                name = snippet['name']
                snippet_item.setText(0, f"📄 {name} ({lang}, {score_pct}%)")
                snippet_item.setData(0, Qt.ItemDataRole.UserRole,
                                   {'type': 'snippet', 'data': snippet})

                # Add description as child item (second line)
                desc = snippet.get('description', '')
                if desc:
                    desc_short = desc if len(desc) <= 50 else desc[:47] + '...'
                    desc_item = QTreeWidgetItem()
                    desc_item.setText(0, f"   {desc_short}")
                    desc_item.setForeground(0, QColor("#888888"))
                    desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                    snippet_item.addChild(desc_item)

                # Set color based on score
                if score > 0.7:
                    color = QColor("#4CAF50")  # Green
                elif score > 0.5:
                    color = QColor("#FFC107")  # Amber
                else:
                    color = QColor("#FF9800")  # Orange
                snippet_item.setForeground(0, color)

                # Add tooltip with match info
                snippet_item.setToolTip(0,
                    f"Match score: {score_pct}%\n"
                    f"Language: {lang}\n"
                    f"Usage: {snippet.get('usage_count', 0)} times"
                )

                snippets_root.addChild(snippet_item)

            snippets_root.setExpanded(True)

        # If no results, show message
        if not snippet_results and not tag_results:
            no_results = QTreeWidgetItem()
            no_results.setText(0, f"No results for '{query}'")
            no_results.setForeground(0, QColor("#888888"))
            self.tree.addTopLevelItem(no_results)

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle tree item click.

        Args:
            item: Clicked tree item.
            column: Column index.
        """
        item_data = item.data(0, Qt.ItemDataRole.UserRole)

        if not item_data:
            return

        if item_data['type'] == 'snippet':
            # Show snippet preview with syntax highlighting
            snippet = item_data['data']
            self._show_snippet_preview(snippet)
        elif item_data['type'] == 'tag':
            # Show tag info
            tag = item_data['data']
            snippets = self.db_manager.get_snippets_by_tag(tag['id'])
            if snippets:
                # Show first snippet with syntax highlighting
                snippet = snippets[0]
                self._show_snippet_preview(snippet, tag_prefix=tag['name'])
            else:
                self.preview.setPlainText(f"No snippets in '{tag['name']}'")
                self.status_label.setText(f"{tag['name']} (empty)")
                # Remove highlighter for plain text
                if self.highlighter:
                    self.highlighter.setDocument(None)
                    self.highlighter = None

    def _show_snippet_preview(self, snippet: dict, tag_prefix: str = None):
        """Show snippet in preview panel with syntax highlighting.

        Args:
            snippet: Snippet dictionary with code and language
            tag_prefix: Optional tag name prefix for status label
        """
        code = snippet.get('code', '')
        language = snippet.get('language', 'text')
        name = snippet.get('name', 'Unnamed')

        # Set preview text
        self.preview.setPlainText(code)

        # Apply syntax highlighting
        if language and language.lower() != 'text':
            # Normalize language name
            normalized_lang = normalize_language(language)

            # Create or update highlighter
            if self.highlighter is None or self.current_language != normalized_lang:
                # Remove old highlighter if exists
                if self.highlighter:
                    self.highlighter.setDocument(None)

                # Create new highlighter
                self.highlighter = apply_highlighter(
                    self.preview,
                    language=normalized_lang,
                    theme='dark'
                )
                self.current_language = normalized_lang
        else:
            # Remove highlighter for plain text
            if self.highlighter:
                self.highlighter.setDocument(None)
                self.highlighter = None
            self.current_language = 'text'

        # Update status label
        lang_display = language or 'text'
        if tag_prefix:
            self.status_label.setText(f"{tag_prefix}: {name} ({lang_display})")
        else:
            self.status_label.setText(f"{name} ({lang_display})")

    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle tree item double click (copy to clipboard).

        Args:
            item: Double-clicked tree item.
            column: Column index.
        """
        item_data = item.data(0, Qt.ItemDataRole.UserRole)

        if not item_data:
            return

        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()

        if item_data['type'] == 'snippet':
            # Copy snippet code
            snippet = item_data['data']
            clipboard.setText(snippet['code'])
            self.status_label.setText(f"✓ Copied '{snippet['name']}' to clipboard!")

            # Update usage count
            with self.db_manager.get_local_session() as session:
                from src.models.models import Snippet
                db_snippet = session.query(Snippet).filter(Snippet.id == snippet['id']).first()
                if db_snippet:
                    db_snippet.increment_usage()
                    session.commit()

        elif item_data['type'] == 'tag':
            # Copy first snippet in tag
            tag = item_data['data']
            snippets = self.db_manager.get_snippets_by_tag(tag['id'])
            if snippets:
                clipboard.setText(snippets[0]['code'])
                self.status_label.setText(f"✓ Copied '{snippets[0]['name']}' to clipboard!")

    def _show_context_menu(self, position):
        """Show context menu for tree items.

        Args:
            position: Menu position.
        """
        item = self.tree.itemAt(position)
        if not item:
            return

        item_data = item.data(0, Qt.ItemDataRole.UserRole)
        if not item_data:
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2E2E2E;
                color: white;
                border: 1px solid #444444;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #0D47A1;
            }
        """)

        if item_data['type'] == 'snippet':
            snippet = item_data['data']

            # Copy action
            copy_action = QAction("📋 Copy to Clipboard", self)
            copy_action.triggered.connect(lambda: self._copy_snippet(snippet))
            menu.addAction(copy_action)

            # Edit action (placeholder)
            edit_action = QAction("✏️ Edit Snippet", self)
            edit_action.triggered.connect(lambda: self._edit_snippet(snippet))
            menu.addAction(edit_action)

            menu.addSeparator()

            # Delete action (placeholder)
            delete_action = QAction("🗑️ Delete Snippet", self)
            delete_action.triggered.connect(lambda: self._delete_snippet(snippet))
            menu.addAction(delete_action)

        elif item_data['type'] == 'tag':
            tag = item_data['data']

            # Add snippet action (placeholder)
            add_action = QAction("➕ Add Snippet", self)
            add_action.triggered.connect(lambda: self._add_snippet_to_tag(tag))
            menu.addAction(add_action)

            menu.addSeparator()

            # Edit tag action (placeholder)
            edit_tag_action = QAction("✏️ Edit Tag", self)
            edit_tag_action.triggered.connect(lambda: self._edit_tag(tag))
            menu.addAction(edit_tag_action)

        menu.exec(self.tree.viewport().mapToGlobal(position))

    def _copy_snippet(self, snippet):
        """Copy snippet to clipboard.

        Args:
            snippet: Snippet data dictionary.
        """
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(snippet['code'])
        self.status_label.setText(f"✓ Copied '{snippet['name']}' to clipboard!")

    def _edit_snippet(self, snippet):
        """Edit snippet with dialog.

        Args:
            snippet: Snippet data dictionary.
        """
        # Get all tags for selection
        tags = self.db_manager.get_all_tags()

        # Open edit dialog
        dialog = SnippetDialog(self, snippet=snippet, all_tags=tags)
        dialog.snippet_saved.connect(self._on_snippet_updated)

        if dialog.exec():
            self.status_label.setText(f"✓ Updated '{snippet['name']}'")
        else:
            self.status_label.setText("Edit cancelled")

    def _delete_snippet(self, snippet):
        """Delete snippet with confirmation.

        Args:
            snippet: Snippet data dictionary.
        """
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Delete Snippet",
            f"Are you sure you want to delete '{snippet['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Delete from database
            success = self.db_manager.delete_snippet(snippet['id'])

            if success:
                self.status_label.setText(f"✓ Deleted '{snippet['name']}'")
                self._load_data()  # Reload tree
            else:
                self.status_label.setText(f"✗ Failed to delete '{snippet['name']}'")

    def _add_snippet_to_tag(self, tag):
        """Add new snippet to tag.

        Args:
            tag: Tag data dictionary.
        """
        # Get all tags for selection
        tags = self.db_manager.get_all_tags()

        # Open new snippet dialog
        dialog = SnippetDialog(self, snippet=None, all_tags=tags)

        # Pre-select this tag
        if tag['id'] in dialog.tag_items:
            item = dialog.tag_items[tag['id']]
            item.setCheckState(0, Qt.CheckState.Checked)
            dialog.selected_tag_ids.append(tag['id'])

        dialog.snippet_saved.connect(self._on_snippet_created)

        if dialog.exec():
            self.status_label.setText(f"✓ Snippet added to '{tag['name']}'")
        else:
            self.status_label.setText("Cancelled")

    def _edit_tag(self, tag):
        """Edit tag (placeholder - for future implementation).

        Args:
            tag: Tag data dictionary.
        """
        self.status_label.setText(f"Edit tag: {tag['name']} (Not implemented yet)")

    def _create_new_snippet(self):
        """Create a new snippet (from + New button)."""
        # Get all tags for selection
        tags = self.db_manager.get_all_tags()

        # Open new snippet dialog
        dialog = SnippetDialog(self, snippet=None, all_tags=tags)
        dialog.snippet_saved.connect(self._on_snippet_created)

        if dialog.exec():
            self.status_label.setText("✓ Snippet created")
        else:
            self.status_label.setText("Cancelled")

    def _on_snippet_created(self, snippet_data):
        """Handle new snippet creation.

        Args:
            snippet_data: New snippet data from dialog.
        """
        # Add to database
        self.db_manager.add_snippet(
            name=snippet_data['name'],
            code=snippet_data['code'],
            language=snippet_data.get('language'),
            description=snippet_data.get('description'),
            tag_ids=snippet_data.get('tag_ids', [])
        )

        # Reload tree
        self._load_data()

    def _on_snippet_updated(self, snippet_data):
        """Handle snippet update.

        Args:
            snippet_data: Updated snippet data from dialog.
        """
        # Update in database
        self.db_manager.update_snippet(
            snippet_data['id'],
            name=snippet_data['name'],
            code=snippet_data['code'],
            language=snippet_data.get('language'),
            description=snippet_data.get('description')
        )

        # TODO: Update tag associations

        # Reload tree
        self._load_data()

    def toggle_visibility(self):
        """Toggle window visibility with animation."""
        if self.is_visible:
            self.hide_window()
        else:
            self.show_window()

    def show_window(self):
        """Show window with fade-in animation."""
        self.show()
        self.is_visible = True

        # Animate opacity
        self.fade_animation.setStartValue(self.config.appearance.opacity_inactive)
        self.fade_animation.setEndValue(self.config.appearance.opacity_active)
        self.fade_animation.start()

        # Focus search box
        self.search_input.setFocus()

    def hide_window(self):
        """Hide window with fade-out animation."""
        self.fade_animation.setStartValue(self.config.appearance.opacity_active)
        self.fade_animation.setEndValue(self.config.appearance.opacity_inactive)
        self.fade_animation.finished.connect(self._finish_hide)
        self.fade_animation.start()

    def _finish_hide(self):
        """Complete hiding after animation."""
        self.hide()
        self.is_visible = False
        self.fade_animation.finished.disconnect(self._finish_hide)

    def close_application(self):
        """Close the entire application."""
        from PyQt6.QtWidgets import QApplication
        QApplication.quit()

    def toggle_minimize(self):
        """Toggle window minimize/restore state."""
        if self.is_minimized:
            # Restore to normal size
            if self.normal_height:
                self.setMinimumHeight(self.config.appearance.height_min)
                self.setMaximumHeight(self.config.appearance.height_max)
                self.resize(self.width(), self.normal_height)
                self.normal_height = None
            self.is_minimized = False
            self.btn_minimize.setToolTip("ウィンドウを最小化")
        else:
            # Minimize to title bar only
            self.normal_height = self.height()
            self.setMinimumHeight(50)
            self.setMaximumHeight(50)
            self.resize(self.width(), 50)
            self.is_minimized = True
            self.btn_minimize.setToolTip("ウィンドウを復元")

    def toggle_always_on_top(self):
        """Toggle always on top state."""
        self.is_always_on_top = not self.is_always_on_top

        # Get current window flags
        flags = self.windowFlags()

        if self.is_always_on_top:
            # Add WindowStaysOnTopHint flag
            flags |= Qt.WindowType.WindowStaysOnTopHint
            self.btn_always_on_top.setStyleSheet("""
                QPushButton {
                    background-color: rgba(40, 205, 65, 255);
                    border: 1px solid rgba(30, 160, 50, 255);
                    border-radius: 7px;
                }
                QPushButton:hover {
                    background-color: rgba(40, 205, 65, 255);
                    border: 1px solid rgba(20, 100, 35, 255);
                }
                QPushButton:pressed {
                    background-color: rgba(30, 160, 50, 255);
                }
            """)
            self.btn_always_on_top.setToolTip("常に最前面に固定中（クリックで解除）")
        else:
            # Remove WindowStaysOnTopHint flag
            flags &= ~Qt.WindowType.WindowStaysOnTopHint
            self.btn_always_on_top.setStyleSheet("""
                QPushButton {
                    background-color: rgba(40, 205, 65, 120);
                    border: 1px solid rgba(30, 160, 50, 255);
                    border-radius: 7px;
                }
                QPushButton:hover {
                    background-color: rgba(40, 205, 65, 180);
                    border: 1px solid rgba(20, 100, 35, 255);
                }
                QPushButton:pressed {
                    background-color: rgba(30, 160, 50, 255);
                }
            """)
            self.btn_always_on_top.setToolTip("通常モード（クリックで最前面に固定）")

        # Apply new flags
        self.setWindowFlags(flags)

        # Re-apply critical attributes that may be lost after setWindowFlags()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Note: Don't change window opacity here - it makes text hard to read

        # Show window with new flags
        self.show()

        # Re-apply rounded mask after show
        self._apply_rounded_mask()

        # Raise window to ensure it's visible when turning always-on-top ON
        if self.is_always_on_top:
            self.raise_()
            self.activateWindow()
