"""Snippet edit dialog for creating and editing snippets."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QComboBox, QPushButton,
    QLabel, QDialogButtonBox, QTreeWidget, QTreeWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from typing import Optional, List, Dict


class SnippetDialog(QDialog):
    """Dialog for creating and editing code snippets.

    Features:
    - Input fields for name, language, code, description
    - Tag selection (multi-select tree)
    - Syntax highlighting (future)
    - Validation
    """

    snippet_saved = pyqtSignal(dict)  # Emitted when snippet is saved

    def __init__(self, parent=None, snippet: Optional[Dict] = None,
                 all_tags: Optional[List[Dict]] = None):
        """Initialize the snippet dialog.

        Args:
            parent: Parent widget.
            snippet: Existing snippet data (for edit mode).
            all_tags: List of all available tags.
        """
        super().__init__(parent)

        self.snippet = snippet
        self.all_tags = all_tags or []
        self.selected_tag_ids = []

        self.setWindowTitle("Edit Snippet" if snippet else "New Snippet")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        """Create and layout UI components."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Title
        title = QLabel("📝 " + ("Edit Snippet" if self.snippet else "Create New Snippet"))
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #64B5F6;")
        layout.addWidget(title)

        # Form layout
        form = QFormLayout()
        form.setSpacing(8)

        # Name field
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., List Comprehension")
        form.addRow("Name:", self.name_input)

        # Language field
        self.language_combo = QComboBox()
        self.language_combo.setEditable(True)
        self.language_combo.addItems([
            "python", "javascript", "typescript", "java", "cpp",
            "c", "csharp", "go", "rust", "php", "ruby", "swift",
            "kotlin", "sql", "html", "css", "bash", "powershell"
        ])
        form.addRow("Language:", self.language_combo)

        layout.addLayout(form)

        # Code editor
        code_label = QLabel("Code:")
        layout.addWidget(code_label)

        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText("Enter your code snippet here...")
        self.code_editor.setFont(QFont("Courier New", 11))
        layout.addWidget(self.code_editor, 1)

        # Description field
        desc_label = QLabel("Description (optional):")
        layout.addWidget(desc_label)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Brief description of what this snippet does...")
        self.description_input.setMaximumHeight(80)
        layout.addWidget(self.description_input)

        # Tag selection
        tag_label = QLabel("Tags:")
        layout.addWidget(tag_label)

        self.tag_tree = QTreeWidget()
        self.tag_tree.setHeaderHidden(True)
        self.tag_tree.setMaximumHeight(150)
        self.tag_tree.itemChanged.connect(self._on_tag_changed)
        layout.addWidget(self.tag_tree)

        self._populate_tag_tree()

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._save)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #2E2E2E;
                color: white;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #1E1E1E;
                color: white;
                border: 1px solid #444444;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #64B5F6;
            }
            QLabel {
                color: white;
            }
            QTreeWidget {
                background-color: #1E1E1E;
                color: white;
                border: 1px solid #444444;
                border-radius: 3px;
            }
            QTreeWidget::item:hover {
                background-color: #2A2A2A;
            }
            QTreeWidget::item:selected {
                background-color: #0D47A1;
            }
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #2196F3;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)

    def _populate_tag_tree(self):
        """Populate tag tree with checkboxes."""
        self.tag_tree.clear()
        self.tag_items = {}

        # Create tag items with checkboxes
        root_items = []

        for tag in self.all_tags:
            item = QTreeWidgetItem()
            item.setText(0, f"{tag['icon']} {tag['name']}")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(0, Qt.CheckState.Unchecked)
            item.setData(0, Qt.ItemDataRole.UserRole, tag)

            self.tag_items[tag['id']] = item

            if tag['parent_id'] is None:
                root_items.append(item)

        # Build hierarchy
        for tag in self.all_tags:
            if tag['parent_id'] is not None and tag['parent_id'] in self.tag_items:
                parent_item = self.tag_items[tag['parent_id']]
                parent_item.addChild(self.tag_items[tag['id']])

        self.tag_tree.addTopLevelItems(root_items)
        self.tag_tree.expandAll()

    def _load_data(self):
        """Load existing snippet data (edit mode)."""
        if not self.snippet:
            return

        self.name_input.setText(self.snippet.get('name', ''))
        self.code_editor.setPlainText(self.snippet.get('code', ''))
        self.description_input.setPlainText(self.snippet.get('description', ''))

        language = self.snippet.get('language', '')
        if language:
            index = self.language_combo.findText(language)
            if index >= 0:
                self.language_combo.setCurrentIndex(index)
            else:
                self.language_combo.setCurrentText(language)

        # TODO: Load and check associated tags

    def _on_tag_changed(self, item, column):
        """Handle tag checkbox change.

        Args:
            item: Changed tree item.
            column: Column index.
        """
        tag_data = item.data(0, Qt.ItemDataRole.UserRole)
        if not tag_data:
            return

        if item.checkState(0) == Qt.CheckState.Checked:
            if tag_data['id'] not in self.selected_tag_ids:
                self.selected_tag_ids.append(tag_data['id'])
        else:
            if tag_data['id'] in self.selected_tag_ids:
                self.selected_tag_ids.remove(tag_data['id'])

    def _validate(self) -> bool:
        """Validate input fields.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error",
                              "Please enter a snippet name.")
            self.name_input.setFocus()
            return False

        if not self.code_editor.toPlainText().strip():
            QMessageBox.warning(self, "Validation Error",
                              "Please enter the code snippet.")
            self.code_editor.setFocus()
            return False

        if not self.selected_tag_ids:
            QMessageBox.warning(self, "Validation Error",
                              "Please select at least one tag.")
            return False

        return True

    def _save(self):
        """Save the snippet."""
        if not self._validate():
            return

        snippet_data = {
            'name': self.name_input.text().strip(),
            'code': self.code_editor.toPlainText(),
            'language': self.language_combo.currentText().strip(),
            'description': self.description_input.toPlainText().strip(),
            'tag_ids': self.selected_tag_ids.copy()
        }

        if self.snippet:
            snippet_data['id'] = self.snippet['id']

        self.snippet_saved.emit(snippet_data)
        self.accept()

    def get_snippet_data(self) -> Dict:
        """Get the snippet data.

        Returns:
            Dict: Snippet data dictionary.
        """
        return {
            'name': self.name_input.text().strip(),
            'code': self.code_editor.toPlainText(),
            'language': self.language_combo.currentText().strip(),
            'description': self.description_input.toPlainText().strip(),
            'tag_ids': self.selected_tag_ids.copy()
        }
