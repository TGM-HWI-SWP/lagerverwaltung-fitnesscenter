from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QPoint, QParallelAnimationGroup, QPropertyAnimation
from PyQt6.QtWidgets import QStackedWidget


class AnimatedStackedWidget(QStackedWidget):
    """QStackedWidget mit weicher Slide-Animation zwischen Seiten."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._is_animating = False
        self._animation_duration = 320
        self._current_group = None

    def set_animation_duration(self, duration: int) -> None:
        """Setzt die Dauer der Seitenanimation."""
        if duration > 0:
            self._animation_duration = duration

    def slide_to_index(self, index: int) -> None:
        """Wechselt animiert zur gewünschten Seite."""
        if self._is_animating:
            return

        if index < 0 or index >= self.count():
            return

        current_index = self.currentIndex()
        if index == current_index:
            return

        current_widget = self.currentWidget()
        next_widget = self.widget(index)

        if current_widget is None or next_widget is None:
            self.setCurrentIndex(index)
            return

        self._is_animating = True

        width = self.frameRect().width()
        height = self.frameRect().height()

        if width <= 0 or height <= 0:
            self.setCurrentIndex(index)
            self._is_animating = False
            return

        direction = 1 if index > current_index else -1

        current_widget.setGeometry(0, 0, width, height)
        next_widget.setGeometry(0, 0, width, height)

        next_start_pos = QPoint(direction * width, 0)
        next_end_pos = QPoint(0, 0)
        current_end_pos = QPoint(-direction * width, 0)

        next_widget.move(next_start_pos)
        next_widget.show()
        next_widget.raise_()

        current_animation = QPropertyAnimation(current_widget, b"pos", self)
        current_animation.setDuration(self._animation_duration)
        current_animation.setStartValue(current_widget.pos())
        current_animation.setEndValue(current_end_pos)
        current_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        next_animation = QPropertyAnimation(next_widget, b"pos", self)
        next_animation.setDuration(self._animation_duration)
        next_animation.setStartValue(next_start_pos)
        next_animation.setEndValue(next_end_pos)
        next_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        group = QParallelAnimationGroup(self)
        group.addAnimation(current_animation)
        group.addAnimation(next_animation)

        def on_finished() -> None:
            self.setCurrentIndex(index)
            current_widget.move(0, 0)
            next_widget.move(0, 0)
            self._is_animating = False

        group.finished.connect(on_finished)
        group.start()
        self._current_group = group