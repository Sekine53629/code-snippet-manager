"""GUI Application Entry Point.

Launch the Code Snippet Manager with graphical user interface.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from src.utils.config import load_config
from src.utils.database import DatabaseManager
from src.views.gadget_window import GadgetWindow


def main():
    """Main GUI application entry point."""
    print("=" * 60)
    print("Code Snippet Manager - GUI Mode")
    print("=" * 60)

    # Create Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName("Code Snippet Manager")
    app.setOrganizationName("Sekine53629")

    # Load configuration
    print("\n[1] Loading configuration...")
    config = load_config()
    print(f"✓ Configuration loaded")
    print(f"  Position: {config.appearance.position}")
    print(f"  Theme: {config.appearance.theme}")
    print(f"  Width: {config.appearance.width}px")

    # Initialize database
    print("\n[2] Initializing database...")
    db_manager = DatabaseManager(config)
    print(f"✓ Database initialized")

    # Check for data
    tags = db_manager.get_all_tags()
    print(f"  Tags: {len(tags)}")

    if len(tags) == 0:
        print("\n⚠️  No data found. Run 'python main.py' first to initialize sample data.")
        print("   Or add snippets through the GUI.")

    # Create main window
    print("\n[3] Creating GUI window...")
    window = GadgetWindow(config, db_manager)
    print(f"✓ Window created")
    print(f"  Size: {window.width()}x{window.height()}")
    print(f"  Position: {window.x()}, {window.y()}")

    # Show window
    print("\n[4] Launching application...")
    window.show_window()

    print("\n" + "=" * 60)
    print("✓ Application running!")
    print("=" * 60)
    print("\nControls:")
    print("  - Search: Type in search box")
    print("  - Select: Click on tag/snippet")
    print("  - Copy: Double-click on snippet")
    print("  - Minimize: Click '—' button")
    print("  - Close: Click '×' button or Ctrl+C")
    print("\nPress Ctrl+C to quit.")
    print("=" * 60)

    # Run event loop
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        db_manager.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
