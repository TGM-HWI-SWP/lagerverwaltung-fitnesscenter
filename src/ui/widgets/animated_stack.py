from __future__ import annotations

from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QParallelAnimationGroup,
    QPropertyAnimation,
)
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QStackedWidget, QWidget


class AnimatedStackedWidget(QStackedWidget):
    """QStackedWidget mit weicher Slide- und Fade-Animation zwischen Seiten."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._is_animating = False
        self._animation_duration = 360
        self._current_group: QParallelAnimationGroup | None = None
        self._queued_index: int | None = None

    def set_animation_duration(self, duration: int) -> None:
        """Setzt die Dauer der Seitenanimation."""
        if duration > 0:
            self._animation_duration = duration

    def is_animating(self) -> bool:
        """Gibt zurück, ob gerade eine Animation läuft."""
        return self._is_animating

    def slide_to_index(self, index: int) -> None:
        """Wechselt weich animiert zur gewünschten Seite."""
        if index < 0 or index >= self.count():
            return

        current_index = self.currentIndex()
        if index == current_index:
            return

        if self._is_animating:
            self._queued_index = index
            return

        current_widget = self.currentWidget()
        next_widget = self.widget(index)

        if current_widget is None or next_widget is None:
            self.setCurrentIndex(index)
            return

        width = self.frameRect().width()
        height = self.frameRect().height()

        if width <= 0 or height <= 0:
            self.setCurrentIndex(index)
            return

        self._is_animating = True
        self._queued_index = None

        direction = 1 if index > current_index else -1

        self._prepare_widget_for_animation(current_widget, width, height)
        self._prepare_widget_for_animation(next_widget, width, height)

        next_start_pos = QPoint(direction * width, 0)
        next_end_pos = QPoint(0, 0)
        current_end_pos = QPoint(-direction * width, 0)

        next_widget.move(next_start_pos)
        next_widget.show()
        next_widget.raise_()

        current_opacity = self._ensure_opacity_effect(current_widget)
        next_opacity = self._ensure_opacity_effect(next_widget)

        current_opacity.setOpacity(1.0)
        next_opacity.setOpacity(0.0)

        current_slide = QPropertyAnimation(current_widget, b"pos", self)
        current_slide.setDuration(self._animation_duration)
        current_slide.setStartValue(QPoint(0, 0))
        current_slide.setEndValue(current_end_pos)
        current_slide.setEasingCurve(QEasingCurve.Type.InOutCubic)

        next_slide = QPropertyAnimation(next_widget, b"pos", self)
        next_slide.setDuration(self._animation_duration)
        next_slide.setStartValue(next_start_pos)
        next_slide.setEndValue(next_end_pos)
        next_slide.setEasingCurve(QEasingCurve.Type.InOutCubic)

        current_fade = QPropertyAnimation(current_opacity, b"opacity", self)
        current_fade.setDuration(self._animation_duration)
        current_fade.setStartValue(1.0)
        current_fade.setEndValue(0.82)
        current_fade.setEasingCurve(QEasingCurve.Type.InOutQuad)

        next_fade = QPropertyAnimation(next_opacity, b"opacity", self)
        next_fade.setDuration(self._animation_duration)
        next_fade.setStartValue(0.0)
        next_fade.setEndValue(1.0)
        next_fade.setEasingCurve(QEasingCurve.Type.InOutQuad)

        group = QParallelAnimationGroup(self)
        group.addAnimation(current_slide)
        group.addAnimation(next_slide)
        group.addAnimation(current_fade)
        group.addAnimation(next_fade)

        def on_finished() -> None:
            self.setCurrentIndex(index)

            current_widget.move(0, 0)
            next_widget.move(0, 0)

            current_opacity.setOpacity(1.0)
            next_opacity.setOpacity(1.0)

            current_widget.hide()
            self.currentWidget().show()

            self._is_animating = False
            self._current_group = None

            if self._queued_index is not None and self._queued_index != self.currentIndex():
                queued_index = self._queued_index
                self._queued_index = None
                self.slide_to_index(queued_index)

        group.finished.connect(on_finished)
        group.start()
        self._current_group = group

    def _prepare_widget_for_animation(self, widget: QWidget, width: int, height: int) -> None:
        """Bereitet ein Widget geometrisch für die Animation vor."""
        widget.setGeometry(0, 0, width, height)
        widget.show()

    def _ensure_opacity_effect(self, widget: QWidget) -> QGraphicsOpacityEffect:
        """Stellt sicher, dass ein Widget einen Opacity-Effekt besitzt."""
        effect = widget.graphicsEffect()

        if isinstance(effect, QGraphicsOpacityEffect):
            return effect

        opacity_effect = QGraphicsOpacityEffect(widget)
        opacity_effect.setOpacity(1.0)
        widget.setGraphicsEffect(opacity_effect)
        return opacity_effect

    def resizeEvent(self, event) -> None:
        """Sorgt dafür, dass Seiten nach Größenänderungen sauber bleiben."""
        super().resizeEvent(event)

        width = self.frameRect().width()
        height = self.frameRect().height()

        for i in range(self.count()):
            widget = self.widget(i)
            if widget is not None and not self._is_animating:
                widget.setGeometry(0, 0, width, height)
                widget.move(0, 0)