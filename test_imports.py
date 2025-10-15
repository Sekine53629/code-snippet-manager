"""Test basic imports without running the full application."""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("Testing imports...")
print("-" * 40)

try:
    print("✓ sys and pathlib")
except ImportError as e:
    print(f"✗ Error: {e}")

try:
    from src.models.models import Base, Tag, Snippet
    print("✓ Database models imported")
except ImportError as e:
    print(f"✗ Database models: {e}")

try:
    from src.utils.config import Config, load_config
    print("✓ Config module imported")
except ImportError as e:
    print(f"✗ Config module: {e}")

try:
    from src.utils.database import DatabaseManager
    print("✓ Database manager imported")
except ImportError as e:
    print(f"✗ Database manager: {e}")

print("-" * 40)
print("\nTo install dependencies, run:")
print("  python3 -m venv venv")
print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
print("  pip install -r requirements.txt")
