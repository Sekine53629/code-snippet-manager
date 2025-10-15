"""
Settings dialog for application configuration.

Provides UI for:
- Appearance settings (position, theme, opacity)
- Behavior settings (hotkeys, auto-insert)
- Database settings (local/shared paths)
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox,
    QSpinBox, QDoubleSpinBox, QGroupBox, QFormLayout,
    QDialogButtonBox, QFileDialog, QSlider
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from src.utils.config import Config, AppearanceConfig, BehaviorConfig, DatabaseConfig
from typing import Optional


class SettingsDialog(QDialog):
    """Dialog for application settings."""

    settings_changed = pyqtSignal()  # Emitted when settings are saved

    def __init__(self, config: Config, parent=None):
        """
        Initialize settings dialog.

        Args:
            config: Current application configuration
            parent: Parent widget
        """
        super().__init__(parent)

        self.config = config
        self.temp_config = config.model_copy(deep=True)  # Working copy

        self.setWindowTitle("Settings")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        """Setup user interface."""
        layout = QVBoxLayout()

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_appearance_tab(), "Appearance")
        self.tabs.addTab(self._create_behavior_tab(), "Behavior")
        self.tabs.addTab(self._create_database_tab(), "Database")

        layout.addWidget(self.tabs)

        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Apply
        )
        buttons.accepted.connect(self._save_and_close)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self._apply)

        layout.addWidget(buttons)

        self.setLayout(layout)

        # Apply dark theme
        self._apply_theme()

    def _create_appearance_tab(self) -> QWidget:
        """Create appearance settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Window position group
        position_group = QGroupBox("Window Position")
        position_layout = QFormLayout()

        self.position_combo = QComboBox()
        self.position_combo.addItems(["left", "right"])
        position_layout.addRow("Edge:", self.position_combo)

        self.offset_x_spin = QSpinBox()
        self.offset_x_spin.setRange(-1000, 1000)
        self.offset_x_spin.setSuffix(" px")
        position_layout.addRow("X Offset:", self.offset_x_spin)

        self.offset_y_spin = QSpinBox()
        self.offset_y_spin.setRange(-1000, 1000)
        self.offset_y_spin.setSuffix(" px")
        position_layout.addRow("Y Offset:", self.offset_y_spin)

        position_group.setLayout(position_layout)
        layout.addWidget(position_group)

        # Theme and opacity group
        theme_group = QGroupBox("Theme")
        theme_layout = QFormLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        theme_layout.addRow("Color Theme:", self.theme_combo)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(50, 100)
        self.opacity_slider.setValue(95)
        self.opacity_label = QLabel("95%")
        self.opacity_slider.valueChanged.connect(
            lambda v: self.opacity_label.setText(f"{v}%")
        )
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_label)
        theme_layout.addRow("Opacity:", opacity_layout)

        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # Size group
        size_group = QGroupBox("Window Size")
        size_layout = QFormLayout()

        self.width_spin = QSpinBox()
        self.width_spin.setRange(200, 1000)
        self.width_spin.setSuffix(" px")
        size_layout.addRow("Width:", self.width_spin)

        self.height_spin = QSpinBox()
        self.height_spin.setRange(300, 1200)
        self.height_spin.setSuffix(" px")
        size_layout.addRow("Height:", self.height_spin)

        size_group.setLayout(size_layout)
        layout.addWidget(size_group)

        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def _create_behavior_tab(self) -> QWidget:
        """Create behavior settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Auto-insert group
        insert_group = QGroupBox("Auto-Insert")
        insert_layout = QFormLayout()

        self.auto_insert_enabled = QCheckBox("Enable auto-insert on selection")
        insert_layout.addRow(self.auto_insert_enabled)

        insert_group.setLayout(insert_layout)
        layout.addWidget(insert_group)

        # Minimize group
        minimize_group = QGroupBox("Window Behavior")
        minimize_layout = QFormLayout()

        self.auto_minimize_enabled = QCheckBox("Auto-minimize after insertion")
        minimize_layout.addRow(self.auto_minimize_enabled)

        self.minimize_delay_spin = QSpinBox()
        self.minimize_delay_spin.setRange(0, 5000)
        self.minimize_delay_spin.setSuffix(" ms")
        minimize_layout.addRow("Minimize delay:", self.minimize_delay_spin)

        minimize_group.setLayout(minimize_layout)
        layout.addWidget(minimize_group)

        # Confirmation group
        confirm_group = QGroupBox("Confirmations")
        confirm_layout = QFormLayout()

        self.confirm_delete_enabled = QCheckBox("Confirm before deleting")
        confirm_layout.addRow(self.confirm_delete_enabled)

        confirm_group.setLayout(confirm_layout)
        layout.addWidget(confirm_group)

        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def _create_database_tab(self) -> QWidget:
        """Create database settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Database mode group
        mode_group = QGroupBox("Database Mode")
        mode_layout = QFormLayout()

        self.db_mode_combo = QComboBox()
        self.db_mode_combo.addItems(["local", "shared", "hybrid"])
        mode_layout.addRow("Mode:", self.db_mode_combo)

        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Paths group
        paths_group = QGroupBox("Database Paths")
        paths_layout = QVBoxLayout()

        # Local database path
        local_layout = QHBoxLayout()
        local_layout.addWidget(QLabel("Local DB:"))
        self.local_db_input = QLineEdit()
        local_layout.addWidget(self.local_db_input)
        local_browse_btn = QPushButton("Browse...")
        local_browse_btn.clicked.connect(self._browse_local_db)
        local_layout.addWidget(local_browse_btn)
        paths_layout.addLayout(local_layout)

        # Shared database path
        shared_layout = QHBoxLayout()
        shared_layout.addWidget(QLabel("Shared DB:"))
        self.shared_db_input = QLineEdit()
        shared_layout.addWidget(self.shared_db_input)
        shared_browse_btn = QPushButton("Browse...")
        shared_browse_btn.clicked.connect(self._browse_shared_db)
        shared_layout.addWidget(shared_browse_btn)
        paths_layout.addLayout(shared_layout)

        paths_group.setLayout(paths_layout)
        layout.addWidget(paths_group)

        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def _apply_theme(self):
        """Apply dark theme to dialog."""
        self.setStyleSheet("""
            QDialog {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QTabWidget::pane {
                border: 1px solid #444444;
                background-color: #2E2E2E;
            }
            QTabBar::tab {
                background-color: #3C3C3C;
                color: #FFFFFF;
                padding: 8px 16px;
                border: 1px solid #444444;
            }
            QTabBar::tab:selected {
                background-color: #1976D2;
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
            QLineEdit, QComboBox, QSpinBox {
                background-color: #1E1E1E;
                border: 1px solid #444444;
                border-radius: 3px;
                padding: 5px;
                color: #FFFFFF;
            }
            QCheckBox {
                color: #FFFFFF;
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

    def _load_settings(self):
        """Load settings from config into UI."""
        # Appearance
        self.position_combo.setCurrentText(self.temp_config.appearance.position)
        self.offset_x_spin.setValue(self.temp_config.appearance.offset_x)
        self.offset_y_spin.setValue(self.temp_config.appearance.offset_y)
        self.theme_combo.setCurrentText(self.temp_config.appearance.theme)
        self.opacity_slider.setValue(int(self.temp_config.appearance.opacity_active * 100))
        self.width_spin.setValue(self.temp_config.appearance.width_max)
        self.height_spin.setValue(self.temp_config.appearance.height_max)

        # Behavior
        self.auto_insert_enabled.setChecked(self.temp_config.behavior.auto_insert)
        self.auto_minimize_enabled.setChecked(self.temp_config.behavior.auto_minimize)
        self.minimize_delay_spin.setValue(self.temp_config.behavior.minimize_delay)
        self.confirm_delete_enabled.setChecked(self.temp_config.behavior.confirm_delete)

        # Database
        self.db_mode_combo.setCurrentText(self.temp_config.database.mode)
        self.local_db_input.setText(self.temp_config.database.local.path)
        self.shared_db_input.setText(self.temp_config.database.shared.path or "")

    def _save_settings(self):
        """Save settings from UI to config."""
        # Appearance
        self.temp_config.appearance.position = self.position_combo.currentText()
        self.temp_config.appearance.offset_x = self.offset_x_spin.value()
        self.temp_config.appearance.offset_y = self.offset_y_spin.value()
        self.temp_config.appearance.theme = self.theme_combo.currentText()
        self.temp_config.appearance.opacity_active = self.opacity_slider.value() / 100.0
        self.temp_config.appearance.width_max = self.width_spin.value()
        self.temp_config.appearance.height_max = self.height_spin.value()

        # Behavior
        self.temp_config.behavior.auto_insert = self.auto_insert_enabled.isChecked()
        self.temp_config.behavior.auto_minimize = self.auto_minimize_enabled.isChecked()
        self.temp_config.behavior.minimize_delay = self.minimize_delay_spin.value()
        self.temp_config.behavior.confirm_delete = self.confirm_delete_enabled.isChecked()

        # Database
        self.temp_config.database.mode = self.db_mode_combo.currentText()
        self.temp_config.database.local.path = self.local_db_input.text()
        shared_path = self.shared_db_input.text()
        self.temp_config.database.shared.path = shared_path if shared_path else None

    def _apply(self):
        """Apply settings without closing."""
        self._save_settings()
        # Copy temp config back to original
        for key, value in self.temp_config.model_dump().items():
            setattr(self.config, key, value)
        self.settings_changed.emit()

    def _save_and_close(self):
        """Save settings and close dialog."""
        self._apply()
        self.accept()

    def _browse_local_db(self):
        """Browse for local database file."""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Select Local Database",
            self.local_db_input.text(),
            "SQLite Database (*.db *.sqlite)"
        )
        if filename:
            self.local_db_input.setText(filename)

    def _browse_shared_db(self):
        """Browse for shared database file."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Shared Database",
            self.shared_db_input.text(),
            "SQLite Database (*.db *.sqlite)"
        )
        if filename:
            self.shared_db_input.setText(filename)
