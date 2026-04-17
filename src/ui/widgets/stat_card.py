from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout, QWidget


class StatCard(QFrame):
    """Moderne, stabile Statistik-Karte für Dashboard-Kennzahlen."""

    clicked = pyqtSignal()

    def __init__(
        self,
        title: str,
        value: str,
        subtitle: str = "",
        icon: str = "◉",
        accent: str = "blue",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._title = title
        self._value = value
        self._subtitle = subtitle
        self._icon = icon
        self._accent = accent

        self._numeric_value: int | None = self._parse_numeric_value(value)
        self._hovered = False
        self._value_animation: QPropertyAnimation | None = None

        self.setObjectName("statCard")
        self.setProperty("accent", accent)
        self.setProperty("hovered", False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(150)
        self.setMaximumHeight(160)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        self._build_ui()
        self._refresh_style()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        self.icon_label = QLabel(self._icon)
        self.icon_label.setObjectName("statCardIcon")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.title_label = QLabel(self._title)
        self.title_label.setObjectName("statCardTitle")
        self.title_label.setWordWrap(True)

        self.value_label = QLabel(self._value)
        self.value_label.setObjectName("statCardValue")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.subtitle_label = QLabel(self._subtitle)
        self.subtitle_label.setObjectName("statCardSubtitle")
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setVisible(bool(self._subtitle.strip()))

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()
        layout.addWidget(self.subtitle_label)

    def _refresh_style(self) -> None:
        self.setProperty("accent", self._accent)
        self.setProperty("hovered", self._hovered)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def _parse_numeric_value(self, value: str) -> int | None:
        text = value.strip().replace(".", "").replace(",", "")
        return int(text) if text.isdigit() else None

    def animate_to_value(self, target: int, duration: int = 900) -> None:
        """Animiert den Zahlenwert weich hoch oder runter."""
        start_value = self._parse_numeric_value(self.value_label.text())
        if start_value is None:
            start_value = 0

        self._numeric_value = target

        if self._value_animation is not None:
            self._value_animation.stop()

        self._value_animation = QPropertyAnimation(self, b"windowOpacity", self)
        self._value_animation.setDuration(duration)
        self._value_animation.setStartValue(float(start_value))
        self._value_animation.setEndValue(float(target))
        self._value_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._value_animation.valueChanged.connect(self._update_animated_value)
        self._value_animation.start()

    def _update_animated_value(self, value: object) -> None:
        try:
            self.value_label.setText(str(int(float(value))))
        except (TypeError, ValueError):
            pass

    def set_title(self, title: str) -> None:
        self._title = title
        self.title_label.setText(title)

    def set_value(self, value: str) -> None:
        self._value = value
        self._numeric_value = self._parse_numeric_value(value)
        self.value_label.setText(value)

    def set_value_animated(self, value: int, duration: int = 900) -> None:
        """Setzt einen numerischen Wert animiert."""
        self._value = str(value)
        self._numeric_value = value
        self.animate_to_value(value, duration)

    def set_subtitle(self, subtitle: str) -> None:
        self._subtitle = subtitle
        self.subtitle_label.setText(subtitle)
        self.subtitle_label.setVisible(bool(subtitle.strip()))

    def set_icon(self, icon: str) -> None:
        self._icon = icon
        self.icon_label.setText(icon)

    def set_accent(self, accent: str) -> None:
        self._accent = accent
        self._refresh_style()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event) -> None:
        self._hovered = True
        self._refresh_style()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self._hovered = False
        self._refresh_style()
        super().leaveEvent(event)

    def title(self) -> str:
        return self._title

    def value(self) -> str:
        return self.value_label.text()

    def subtitle(self) -> str:
        return self._subtitle

    def icon(self) -> str:
        return self._icon

    def accent(self) -> str:
        return self._accent