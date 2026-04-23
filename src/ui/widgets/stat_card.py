from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, pyqtProperty, pyqtSignal
from PyQt6.QtGui import QEnterEvent, QMouseEvent
from PyQt6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout, QWidget


class StatCard(QFrame):
    """Wiederverwendbare Statistik-Karte für Dashboard-Kennzahlen."""

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
        """Initialisiert die Statistik-Karte."""
        super().__init__(parent)

        self._title = title
        self._value = value
        self._subtitle = subtitle
        self._icon = icon
        self._accent = accent

        self._display_value = self._parse_numeric_value(value) or 0
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
        """Erstellt die Oberfläche der Karte."""
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
        """Aktualisiert den Stil der Karte."""
        self.setProperty("accent", self._accent)
        self.setProperty("hovered", self._hovered)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    @staticmethod
    def _parse_numeric_value(value: str) -> int | None:
        """Wandelt einen Textwert in eine ganze Zahl um."""
        text = value.strip().replace(".", "").replace(",", "")
        return int(text) if text.isdigit() else None

    def _get_animated_value(self) -> float:
        """Liefert den aktuellen Animationswert."""
        return float(self._display_value)

    def _set_animated_value(self, value: float) -> None:
        """Setzt den aktuellen Animationswert."""
        self._display_value = int(value)
        self.value_label.setText(str(self._display_value))

    animated_value = pyqtProperty(float, _get_animated_value, _set_animated_value)

    def animate_to_value(self, target: int, duration: int = 900) -> None:
        """Animiert den angezeigten Zahlenwert."""
        start_value = self._numeric_value if self._numeric_value is not None else 0

        if self._value_animation is not None:
            self._value_animation.stop()

        self._numeric_value = target
        self._value = str(target)

        self._value_animation = QPropertyAnimation(self, b"animated_value", self)
        self._value_animation.setDuration(duration)
        self._value_animation.setStartValue(float(start_value))
        self._value_animation.setEndValue(float(target))
        self._value_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._value_animation.start()

    def set_title(self, title: str) -> None:
        """Setzt den Titel der Karte."""
        self._title = title
        self.title_label.setText(title)

    def set_value(self, value: str) -> None:
        """Setzt den Wert ohne Animation."""
        self._value = value
        self._numeric_value = self._parse_numeric_value(value)

        if self._numeric_value is not None:
            self._display_value = self._numeric_value

        self.value_label.setText(value)

    def set_value_animated(self, value: int, duration: int = 900) -> None:
        """Setzt den Wert mit Animation."""
        self.animate_to_value(value, duration)

    def set_subtitle(self, subtitle: str) -> None:
        """Setzt den Untertitel der Karte."""
        self._subtitle = subtitle
        self.subtitle_label.setText(subtitle)
        self.subtitle_label.setVisible(bool(subtitle.strip()))

    def set_icon(self, icon: str) -> None:
        """Setzt das Symbol der Karte."""
        self._icon = icon
        self.icon_label.setText(icon)

    def set_accent(self, accent: str) -> None:
        """Setzt den Akzentstil der Karte."""
        self._accent = accent
        self._refresh_style()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Sendet ein Klick-Signal bei linker Maustaste."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:
        """Aktiviert den Hover-Zustand."""
        self._hovered = True
        self._refresh_style()
        super().enterEvent(event)

    def leaveEvent(self, event: QEnterEvent) -> None:
        """Deaktiviert den Hover-Zustand."""
        self._hovered = False
        self._refresh_style()
        super().leaveEvent(event)

    def title(self) -> str:
        """Gibt den Titel zurück."""
        return self._title

    def value(self) -> str:
        """Gibt den aktuellen Wert zurück."""
        return self.value_label.text()

    def subtitle(self) -> str:
        """Gibt den Untertitel zurück."""
        return self._subtitle

    def icon(self) -> str:
        """Gibt das Symbol zurück."""
        return self._icon

    def accent(self) -> str:
        """Gibt den Akzentstil zurück."""
        return self._accent