#!/usr/bin/env python3
"""
Code Snippet Manager - Main Entry Point

A modern, beautiful code snippet manager with hierarchical organization.
This is the main application entry point that initializes and runs
the Code Snippet Manager application.
"""

import sys
import os
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.config import Config, load_config
from utils.database import DatabaseManager
from views.gadget_window import GadgetWindow
from controllers.hotkey_controller import HotkeyController
from controllers.animation_controller import AnimationController


class CodeSnippetApp:
    """Main application class that manages all components."""

    def __init__(self):
        """Initialize the application."""
        self.app = None
        self.config = None
        self.db_manager = None
        self.gadget_window = None
        self.hotkey_controller = None
        self.animation_controller = None

    def initialize(self):
        """Initialize all application components."""
        print("Initializing Code Snippet Manager...")

        # Create QApplication
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Code Snippet Manager")
        self.app.setApplicationVersion("1.0.0")

        # Note: AA_UseHighDpiPixmaps is deprecated in PyQt6 (automatically enabled)

        # Load configuration
        print("Loading configuration...")
        self.config = load_config()

        # Initialize database
        print("Initializing database...")
        self.db_manager = DatabaseManager(self.config)

        # Initialize sample data if database is empty
        self._initialize_sample_data_if_needed()

        # Create gadget window
        print("Creating gadget window...")
        self.gadget_window = GadgetWindow(
            db_manager=self.db_manager,
            config=self.config
        )

        # Initialize hotkey controller
        print("Initializing hotkey controller...")
        self.hotkey_controller = HotkeyController()

        # Connect hotkey to gadget window
        self.hotkey_controller.ctrl_double_tap.connect(self._on_hotkey_activated)

        # Initialize animation controller
        print("Initializing animation controller...")
        self.animation_controller = AnimationController(self.gadget_window)

        # Apply initial appearance settings
        self._apply_appearance_settings()

        print("Initialization complete!")

    def _initialize_sample_data_if_needed(self):
        """Initialize sample data if database is empty."""
        tags = self.db_manager.get_all_tags()
        snippets = self.db_manager.get_all_snippets()

        if len(tags) == 0 and len(snippets) == 0:
            print("Database is empty. Initializing sample data...")
            self._create_sample_data()

    def _create_sample_data(self):
        """Create sample data for testing."""
        # Create sample tags
        python_tag_id = self.db_manager.get_or_create_tag("Python", tag_type="folder")
        js_tag_id = self.db_manager.get_or_create_tag("JavaScript", tag_type="folder")

        # Python subtags
        django_tag_id = self.db_manager.get_or_create_tag("Django", parent_id=python_tag_id, tag_type="folder")
        flask_tag_id = self.db_manager.get_or_create_tag("Flask", parent_id=python_tag_id, tag_type="folder")

        # JavaScript subtags
        react_tag_id = self.db_manager.get_or_create_tag("React", parent_id=js_tag_id, tag_type="folder")

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
            self.db_manager.add_snippet(**snippet_data)

        print("Sample data created successfully!")

    def _apply_appearance_settings(self):
        """Apply appearance settings from config."""
        appearance = self.config.appearance

        # Set window opacity
        self.gadget_window.setWindowOpacity(appearance.opacity_active)

        # Set initial size
        self.gadget_window.resize(appearance.width_max, appearance.height_max)

        # Set theme
        if appearance.theme == 'dark':
            self._apply_dark_theme()
        else:
            self._apply_light_theme()

    def _apply_dark_theme(self):
        """Apply dark theme to the application."""
        dark_stylesheet = """
        QWidget {
            background-color: #2b2b2b;
            color: #e0e0e0;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QLineEdit {
            background-color: #3c3c3c;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 5px;
            color: #e0e0e0;
        }
        QLineEdit:focus {
            border: 1px solid #007acc;
        }
        QPushButton {
            background-color: #0e639c;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px 15px;
        }
        QPushButton:hover {
            background-color: #1177bb;
        }
        QPushButton:pressed {
            background-color: #005a9e;
        }
        QTreeWidget {
            background-color: #252526;
            border: none;
            outline: none;
        }
        QTreeWidget::item {
            padding: 5px;
        }
        QTreeWidget::item:hover {
            background-color: #2a2d2e;
        }
        QTreeWidget::item:selected {
            background-color: #094771;
        }
        QTextEdit {
            background-color: #1e1e1e;
            border: 1px solid #555555;
            color: #d4d4d4;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        QScrollBar:vertical {
            background-color: #2b2b2b;
            width: 12px;
        }
        QScrollBar::handle:vertical {
            background-color: #555555;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #666666;
        }
        """
        self.app.setStyleSheet(dark_stylesheet)

    def _apply_light_theme(self):
        """Apply light theme to the application."""
        light_stylesheet = """
        QWidget {
            background-color: #ffffff;
            color: #000000;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 5px;
            color: #000000;
        }
        QLineEdit:focus {
            border: 1px solid #007acc;
        }
        QPushButton {
            background-color: #0e639c;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px 15px;
        }
        QPushButton:hover {
            background-color: #1177bb;
        }
        QPushButton:pressed {
            background-color: #005a9e;
        }
        QTreeWidget {
            background-color: #f5f5f5;
            border: none;
            outline: none;
        }
        QTreeWidget::item {
            padding: 5px;
        }
        QTreeWidget::item:hover {
            background-color: #e8e8e8;
        }
        QTreeWidget::item:selected {
            background-color: #cce8ff;
        }
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            color: #000000;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        """
        self.app.setStyleSheet(light_stylesheet)

    def _on_hotkey_activated(self):
        """Handle hotkey activation (Ctrl double-tap)."""
        print("Hotkey activated!")

        if self.gadget_window.isVisible():
            # Hide window with animation
            self.animation_controller.fade_out(duration=200)
            # Note: Window will be hidden automatically by animation controller
        else:
            # Show window with animation
            self.gadget_window.show()
            self.animation_controller.fade_in(duration=200)
            self.gadget_window.activateWindow()
            self.gadget_window.raise_()

    def run(self):
        """Run the application."""
        # Show gadget window
        self.gadget_window.show()

        # Start hotkey controller
        print("Starting hotkey controller...")
        self.hotkey_controller.start()

        # Enter event loop
        print("\nApplication started successfully!")
        print("Press Ctrl twice quickly to toggle window visibility.")
        print("Press Ctrl+C in terminal to exit.\n")

        exit_code = self.app.exec()

        # Cleanup
        self.cleanup()

        return exit_code

    def cleanup(self):
        """Clean up resources before exit."""
        print("\nCleaning up...")

        # Stop hotkey controller
        if self.hotkey_controller:
            self.hotkey_controller.stop()

        # Close database connections
        if self.db_manager:
            self.db_manager.close()

        print("Cleanup complete.")


def main():
    """Main entry point."""
    print("=" * 60)
    print("Code Snippet Manager v1.0.0")
    print("=" * 60)

    try:
        # Create and initialize application
        app = CodeSnippetApp()
        app.initialize()

        # Run application
        exit_code = app.run()

        # Exit with code
        sys.exit(exit_code)

    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        sys.exit(0)

    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
