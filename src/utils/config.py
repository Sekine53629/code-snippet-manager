"""Configuration management using Pydantic for type safety."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class DatabaseConfig(BaseModel):
    """Database configuration."""
    mode: str = Field(default='local', description="Database mode: 'local', 'shared', or 'hybrid'")

    class LocalConfig(BaseModel):
        path: str = Field(default='data/local.db')
        writable: bool = True

    class SharedConfig(BaseModel):
        enabled: bool = False
        path: Optional[str] = None
        readonly: bool = True
        auto_sync: bool = True
        sync_interval: int = 300  # seconds

    local: LocalConfig = LocalConfig()
    shared: SharedConfig = SharedConfig()


class AppearanceConfig(BaseModel):
    """UI appearance configuration."""
    position: str = Field(default='right', description="Window position: 'right' or 'left'")
    offset_x: int = Field(default=10, description="Horizontal offset from screen edge")
    offset_y: int = Field(default=0, description="Vertical offset from center")

    opacity_active: float = Field(default=0.95, ge=0.1, le=1.0)
    opacity_inactive: float = Field(default=0.3, ge=0.1, le=1.0)
    opacity_transition: int = Field(default=300, description="Transition time in ms")

    width: int = Field(default=350, ge=250, le=800)
    width_min: int = 250
    width_max: int = 800

    height_min: int = 400
    height_max: int = 800  # Reduced from 1200 to fit preview on screen

    theme: str = Field(default='dark', description="UI theme: 'dark' or 'light'")

    @validator('position')
    def validate_position(cls, v):
        if v not in ['left', 'right']:
            raise ValueError("position must be 'left' or 'right'")
        return v


class HotkeyConfig(BaseModel):
    """Hotkey configuration."""
    toggle_key: str = Field(default='ctrl', description="Primary toggle key")
    toggle_mode: str = Field(default='double_tap', description="'double_tap' or 'single'")
    double_tap_threshold: float = Field(default=0.3, ge=0.1, le=1.0, description="Double tap timeout in seconds")

    # Additional shortcuts
    search_key: str = Field(default='ctrl+f')
    new_snippet_key: str = Field(default='ctrl+n')
    new_tag_key: str = Field(default='ctrl+shift+n')


class BehaviorConfig(BaseModel):
    """Application behavior configuration."""
    auto_insert: bool = Field(default=True, description="Auto-insert snippet on selection")
    auto_minimize: bool = Field(default=True, description="Auto-minimize after insertion")
    minimize_delay: int = Field(default=500, description="Delay before minimizing (ms)")

    remember_state: bool = Field(default=True, description="Remember last viewed hierarchy")
    remember_expanded: bool = Field(default=True, description="Remember expanded folders")

    confirm_delete: bool = Field(default=True, description="Confirm before deleting")
    backup_on_delete: bool = Field(default=True, description="Backup deleted items")


class SearchConfig(BaseModel):
    """Search configuration."""
    fuzzy_enabled: bool = Field(default=True)
    fuzzy_threshold: int = Field(default=70, ge=0, le=100, description="Fuzzy match threshold (0-100)")
    incremental: bool = Field(default=True, description="Search as you type")
    search_in_code: bool = Field(default=True)
    search_in_description: bool = Field(default=True)
    max_results: int = Field(default=50, ge=10, le=500)


class Config(BaseModel):
    """Main application configuration."""
    version: str = Field(default='1.0.0')

    database: DatabaseConfig = DatabaseConfig()
    appearance: AppearanceConfig = AppearanceConfig()
    hotkey: HotkeyConfig = HotkeyConfig()
    behavior: BehaviorConfig = BehaviorConfig()
    search: SearchConfig = SearchConfig()

    class Config:
        """Pydantic configuration."""
        validate_assignment = True


def get_config_path() -> Path:
    """Get the configuration file path.

    On Windows: %APPDATA%/CodeSnippetManager/config.json
    On Mac/Linux: ~/.config/CodeSnippetManager/config.json
    """
    if os.name == 'nt':  # Windows
        config_dir = Path(os.environ.get('APPDATA', '')) / 'CodeSnippetManager'
    else:  # Mac/Linux
        config_dir = Path.home() / '.config' / 'CodeSnippetManager'

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / 'config.json'


def load_config(config_path: Optional[Path] = None) -> Config:
    """Load configuration from file.

    Args:
        config_path: Optional custom config path. If None, uses default.

    Returns:
        Config: Loaded configuration object.
    """
    if config_path is None:
        config_path = get_config_path()

    if not config_path.exists():
        # Create default config
        config = Config()
        save_config(config, config_path)
        return config

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Config(**data)
    except Exception as e:
        print(f"Error loading config: {e}")
        print("Using default configuration.")
        return Config()


def save_config(config: Config, config_path: Optional[Path] = None) -> bool:
    """Save configuration to file.

    Args:
        config: Configuration object to save.
        config_path: Optional custom config path. If None, uses default.

    Returns:
        bool: True if successful, False otherwise.
    """
    if config_path is None:
        config_path = get_config_path()

    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config.dict(), f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False


def expand_path(path: str) -> Path:
    """Expand environment variables and convert to absolute path.

    Supports:
    - %APPDATA% on Windows
    - ~ for home directory
    - Relative paths (converted to absolute)

    Args:
        path: Path string with possible environment variables.

    Returns:
        Path: Expanded absolute path.
    """
    # Expand environment variables
    path = os.path.expandvars(path)

    # Expand home directory
    path = os.path.expanduser(path)

    # Convert to Path and make absolute
    path_obj = Path(path)
    if not path_obj.is_absolute():
        path_obj = Path.cwd() / path_obj

    return path_obj
