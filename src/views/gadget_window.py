"""Gadget-style main window for Code Snippet Manager.

This module implements a semi-transparent, edge-docked window with smooth animations.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QTextEdit, QLineEdit,
    QPushButton, QLabel, QSplitter
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QFont

from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.config import Config
from src.utils.database import DatabaseManager


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
        self.is_minimized = True

        # Setup UI
        self._setup_window()
        self._setup_ui()
        self._setup_animations()
        self._load_data()

    def _setup_window(self):
        """Configure window properties."""
        # Window flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        # Transparency
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(self.config.appearance.opacity_inactive)

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

        # Main layout
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
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

        # Minimize button
        btn_minimize = QPushButton("—")
        btn_minimize.setFixedSize(30, 30)
        btn_minimize.clicked.connect(self.toggle_visibility)
        btn_minimize.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        header.addWidget(btn_minimize)

        # Close button
        btn_close = QPushButton("×")
        btn_close.setFixedSize(30, 30)
        btn_close.clicked.connect(self.close)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #D32F2F;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #F44336;
            }
        """)
        header.addWidget(btn_close)

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
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: #1E1E1E;
                color: white;
                border: 1px solid #444444;
                border-radius: 5px;
                outline: none;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:hover {
                background-color: #2A2A2A;
            }
            QTreeWidget::item:selected {
                background-color: #0D47A1;
            }
        """)
        splitter.addWidget(self.tree)

        # Preview panel
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText("Select a snippet to preview...")
        self.preview.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: white;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
        """)
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
        """Build tree widget from tag data.

        Args:
            tags: List of tag dictionaries.
        """
        # Create a mapping of tag_id -> QTreeWidgetItem
        tag_items = {}
        root_items = []

        # First pass: create all items
        for tag in tags:
            item = QTreeWidgetItem()
            item.setText(0, f"{tag['icon']} {tag['name']}")
            item.setData(0, Qt.ItemDataRole.UserRole, tag)  # Store tag data

            # Set color
            color = QColor(tag['color'])
            item.setForeground(0, color)

            tag_items[tag['id']] = item

            if tag['parent_id'] is None:
                root_items.append(item)

        # Second pass: build hierarchy
        for tag in tags:
            if tag['parent_id'] is not None and tag['parent_id'] in tag_items:
                parent_item = tag_items[tag['parent_id']]
                parent_item.addChild(tag_items[tag['id']])

        # Add root items to tree
        self.tree.addTopLevelItems(root_items)

        # Expand all
        self.tree.expandAll()

    def _on_search_changed(self, text: str):
        """Handle search input changes.

        Args:
            text: Search query text.
        """
        if not text:
            self._load_data()
            return

        # Search snippets
        results = self.db_manager.search_snippets(text)
        self.status_label.setText(f"Found {len(results)} results")

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle tree item click.

        Args:
            item: Clicked tree item.
            column: Column index.
        """
        tag_data = item.data(0, Qt.ItemDataRole.UserRole)

        if tag_data:
            # Load snippets for this tag
            snippets = self.db_manager.get_snippets_by_tag(tag_data['id'])

            if snippets:
                # Show first snippet
                snippet = snippets[0]
                self.preview.setPlainText(snippet['code'])
                self.status_label.setText(f"{snippet['name']} ({snippet['language']})")
            else:
                self.preview.setPlainText(f"No snippets in '{tag_data['name']}'")

    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle tree item double click (copy to clipboard).

        Args:
            item: Double-clicked tree item.
            column: Column index.
        """
        tag_data = item.data(0, Qt.ItemDataRole.UserRole)

        if tag_data:
            snippets = self.db_manager.get_snippets_by_tag(tag_data['id'])
            if snippets:
                # Copy first snippet to clipboard
                from PyQt6.QtWidgets import QApplication
                clipboard = QApplication.clipboard()
                clipboard.setText(snippets[0]['code'])
                self.status_label.setText("✓ Copied to clipboard!")

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
