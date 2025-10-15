"""
Controllers package for application logic.

Provides controllers for:
- Hotkey management (Ctrl double-tap, global shortcuts)
- Animation (expand/collapse, fade, slide)
"""

from src.controllers.hotkey_controller import HotkeyController
from src.controllers.animation_controller import AnimationController

__all__ = [
    'HotkeyController',
    'AnimationController',
]
