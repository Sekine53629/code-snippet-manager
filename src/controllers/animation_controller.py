"""
Animation controller for smooth UI transitions.

Provides animation effects for:
- Window expand/collapse
- Fade in/out
- Slide transitions
- Custom easing functions
"""

from typing import Optional, Callable
from PyQt6.QtCore import (
    QObject, QPropertyAnimation, QEasingCurve,
    QParallelAnimationGroup, QSequentialAnimationGroup,
    pyqtSignal, QAbstractAnimation
)
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRect, QPoint, QSize


class AnimationController(QObject):
    """Controller for managing UI animations."""

    # Signals
    animation_started = pyqtSignal()
    animation_finished = pyqtSignal()

    def __init__(self, widget: Optional[QWidget] = None):
        """
        Initialize animation controller.

        Args:
            widget: Widget to animate (can be set later)
        """
        super().__init__()
        self.widget = widget
        self.current_animation: Optional[QAbstractAnimation] = None

    def set_widget(self, widget: QWidget):
        """
        Set the widget to animate.

        Args:
            widget: Widget to animate
        """
        self.widget = widget

    def fade_in(self, duration_ms: int = 300,
                easing: QEasingCurve.Type = QEasingCurve.Type.InOutQuad) -> QPropertyAnimation:
        """
        Fade in animation.

        Args:
            duration_ms: Animation duration in milliseconds
            easing: Easing curve type

        Returns:
            Animation object
        """
        if not self.widget:
            return None

        animation = QPropertyAnimation(self.widget, b"windowOpacity")
        animation.setDuration(duration_ms)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(easing)

        animation.finished.connect(self.animation_finished.emit)

        self.current_animation = animation
        return animation

    def fade_out(self, duration_ms: int = 300,
                 easing: QEasingCurve.Type = QEasingCurve.Type.InOutQuad) -> QPropertyAnimation:
        """
        Fade out animation.

        Args:
            duration_ms: Animation duration in milliseconds
            easing: Easing curve type

        Returns:
            Animation object
        """
        if not self.widget:
            return None

        animation = QPropertyAnimation(self.widget, b"windowOpacity")
        animation.setDuration(duration_ms)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(easing)

        animation.finished.connect(self.animation_finished.emit)

        self.current_animation = animation
        return animation

    def expand_horizontal(self, target_width: int, duration_ms: int = 400,
                         easing: QEasingCurve.Type = QEasingCurve.Type.OutCubic) -> QPropertyAnimation:
        """
        Expand widget horizontally.

        Args:
            target_width: Target width in pixels
            duration_ms: Animation duration in milliseconds
            easing: Easing curve type

        Returns:
            Animation object
        """
        if not self.widget:
            return None

        current_width = self.widget.width()

        animation = QPropertyAnimation(self.widget, b"maximumWidth")
        animation.setDuration(duration_ms)
        animation.setStartValue(current_width)
        animation.setEndValue(target_width)
        animation.setEasingCurve(easing)

        animation.finished.connect(self.animation_finished.emit)

        self.current_animation = animation
        return animation

    def collapse_horizontal(self, target_width: int, duration_ms: int = 400,
                           easing: QEasingCurve.Type = QEasingCurve.Type.InCubic) -> QPropertyAnimation:
        """
        Collapse widget horizontally.

        Args:
            target_width: Target width in pixels
            duration_ms: Animation duration in milliseconds
            easing: Easing curve type

        Returns:
            Animation object
        """
        if not self.widget:
            return None

        current_width = self.widget.width()

        animation = QPropertyAnimation(self.widget, b"maximumWidth")
        animation.setDuration(duration_ms)
        animation.setStartValue(current_width)
        animation.setEndValue(target_width)
        animation.setEasingCurve(easing)

        animation.finished.connect(self.animation_finished.emit)

        self.current_animation = animation
        return animation

    def slide_in(self, start_pos: QPoint, end_pos: QPoint, duration_ms: int = 400,
                easing: QEasingCurve.Type = QEasingCurve.Type.OutCubic) -> QPropertyAnimation:
        """
        Slide widget from start position to end position.

        Args:
            start_pos: Starting position
            end_pos: Ending position
            duration_ms: Animation duration in milliseconds
            easing: Easing curve type

        Returns:
            Animation object
        """
        if not self.widget:
            return None

        animation = QPropertyAnimation(self.widget, b"pos")
        animation.setDuration(duration_ms)
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setEasingCurve(easing)

        animation.finished.connect(self.animation_finished.emit)

        self.current_animation = animation
        return animation

    def slide_out(self, end_pos: QPoint, duration_ms: int = 400,
                 easing: QEasingCurve.Type = QEasingCurve.Type.InCubic) -> QPropertyAnimation:
        """
        Slide widget out to position.

        Args:
            end_pos: Ending position
            duration_ms: Animation duration in milliseconds
            easing: Easing curve type

        Returns:
            Animation object
        """
        if not self.widget:
            return None

        start_pos = self.widget.pos()

        animation = QPropertyAnimation(self.widget, b"pos")
        animation.setDuration(duration_ms)
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setEasingCurve(easing)

        animation.finished.connect(self.animation_finished.emit)

        self.current_animation = animation
        return animation

    def expand_from_edge(self, edge: str = 'right', collapsed_width: int = 32,
                        expanded_width: int = 300, duration_ms: int = 400) -> QParallelAnimationGroup:
        """
        Expand widget from screen edge.

        Args:
            edge: Edge to expand from ('left' or 'right')
            collapsed_width: Width when collapsed
            expanded_width: Width when expanded
            duration_ms: Animation duration in milliseconds

        Returns:
            Animation group
        """
        if not self.widget:
            return None

        # Create parallel animation group for smooth expansion
        group = QParallelAnimationGroup()

        # Width animation
        width_anim = QPropertyAnimation(self.widget, b"maximumWidth")
        width_anim.setDuration(duration_ms)
        width_anim.setStartValue(collapsed_width)
        width_anim.setEndValue(expanded_width)
        width_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Position animation (for edge docking)
        if edge == 'right':
            # Expand leftward from right edge
            current_pos = self.widget.pos()
            end_x = current_pos.x() - (expanded_width - collapsed_width)
            pos_anim = QPropertyAnimation(self.widget, b"pos")
            pos_anim.setDuration(duration_ms)
            pos_anim.setStartValue(current_pos)
            pos_anim.setEndValue(QPoint(end_x, current_pos.y()))
            pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            group.addAnimation(pos_anim)

        # Opacity animation
        opacity_anim = QPropertyAnimation(self.widget, b"windowOpacity")
        opacity_anim.setDuration(duration_ms)
        opacity_anim.setStartValue(0.8)
        opacity_anim.setEndValue(1.0)
        opacity_anim.setEasingCurve(QEasingCurve.Type.Linear)

        group.addAnimation(width_anim)
        group.addAnimation(opacity_anim)

        group.finished.connect(self.animation_finished.emit)

        self.current_animation = group
        return group

    def collapse_to_edge(self, edge: str = 'right', collapsed_width: int = 32,
                        expanded_width: int = 300, duration_ms: int = 400) -> QParallelAnimationGroup:
        """
        Collapse widget to screen edge.

        Args:
            edge: Edge to collapse to ('left' or 'right')
            collapsed_width: Width when collapsed
            expanded_width: Width when expanded
            duration_ms: Animation duration in milliseconds

        Returns:
            Animation group
        """
        if not self.widget:
            return None

        # Create parallel animation group
        group = QParallelAnimationGroup()

        # Width animation
        width_anim = QPropertyAnimation(self.widget, b"maximumWidth")
        width_anim.setDuration(duration_ms)
        width_anim.setStartValue(expanded_width)
        width_anim.setEndValue(collapsed_width)
        width_anim.setEasingCurve(QEasingCurve.Type.InCubic)

        # Position animation
        if edge == 'right':
            # Collapse rightward to right edge
            current_pos = self.widget.pos()
            end_x = current_pos.x() + (expanded_width - collapsed_width)
            pos_anim = QPropertyAnimation(self.widget, b"pos")
            pos_anim.setDuration(duration_ms)
            pos_anim.setStartValue(current_pos)
            pos_anim.setEndValue(QPoint(end_x, current_pos.y()))
            pos_anim.setEasingCurve(QEasingCurve.Type.InCubic)
            group.addAnimation(pos_anim)

        # Opacity animation
        opacity_anim = QPropertyAnimation(self.widget, b"windowOpacity")
        opacity_anim.setDuration(duration_ms)
        opacity_anim.setStartValue(1.0)
        opacity_anim.setEndValue(0.8)
        opacity_anim.setEasingCurve(QEasingCurve.Type.Linear)

        group.addAnimation(width_anim)
        group.addAnimation(opacity_anim)

        group.finished.connect(self.animation_finished.emit)

        self.current_animation = group
        return group

    def stop(self):
        """Stop current animation."""
        if self.current_animation:
            self.current_animation.stop()
            self.current_animation = None

    def is_running(self) -> bool:
        """
        Check if animation is currently running.

        Returns:
            True if animation is running, False otherwise
        """
        if self.current_animation:
            return self.current_animation.state() == QAbstractAnimation.State.Running
        return False
