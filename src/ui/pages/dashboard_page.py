from __future__ import annotations

from datetime import datetime
from random import choice
from typing import Any, Callable

from PyQt6.QtCore import QDateTime, QEvent, QObject, Qt, QTimer
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.ui.widgets.stat_card import StatCard


class DashboardPage(QWidget):
    """Dashboard mit Kennzahlen, Trends, Alerts und Quick Actions."""

    def __init__(
        self,
        controller: Any | None = None,
        navigator: Callable[[str], None] | None = None,
        quick_action_handler: Callable[[str], None] | None = None,
        snapshot_provider: Callable[[], dict[str, Any]] | None = None,
        health_provider: Callable[[], dict[str, str]] | None = None,
    ) -> None:
        """Initialisiert die Dashboard-Seite."""
        super().__init__()

        self.controller = controller
        self.navigator = navigator
        self.quick_action_handler = quick_action_handler
        self.snapshot_provider = snapshot_provider
        self.health_provider = health_provider

        self._card_targets: dict[QObject, str] = {}
        self._demo_tick = 0

        self._create_ui()
        self.refresh_data()
        self._start_live_updates()

    def _create_ui(self) -> None:
        """Erstellt die komplette Dashboard-Oberfläche."""
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setObjectName("dashboardScrollArea")

        scroll_content = QWidget()
        scroll_content.setObjectName("dashboardScrollContent")

        self.main_layout = QVBoxLayout(scroll_content)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(20)

        self._create_top_section(self.main_layout)
        self._create_stats_grid(self.main_layout)
        self._create_bottom_section(self.main_layout)

        self.main_layout.addStretch()

        scroll_area.setWidget(scroll_content)
        root_layout.addWidget(scroll_area)

    def _create_top_section(self, layout: QVBoxLayout) -> None:
        """Erstellt den oberen Dashboard-Bereich."""
        top_container = QFrame()
        top_container.setObjectName("dashboardHeroCard")
        top_container.setMinimumHeight(140)

        top_layout = QVBoxLayout(top_container)
        top_layout.setContentsMargins(22, 20, 22, 20)
        top_layout.setSpacing(10)

        top_header_row = QHBoxLayout()
        top_header_row.setSpacing(12)

        title_box = QVBoxLayout()
        title_box.setSpacing(6)

        self.title_label = QLabel("Dashboard")
        self.title_label.setObjectName("dashboardTitle")

        self.subtitle_label = QLabel(
            "Die wichtigsten Kennzahlen des Fitnesscenters auf einen Blick."
        )
        self.subtitle_label.setObjectName("dashboardSubtitle")
        self.subtitle_label.setWordWrap(True)

        self.hero_hint_label = QLabel(
            "Mitglieder, Mitarbeiter, Geräte, Automaten und kritische Bestände werden hier kompakt zusammengefasst."
        )
        self.hero_hint_label.setObjectName("dashboardHeroHint")
        self.hero_hint_label.setWordWrap(True)

        title_box.addWidget(self.title_label)
        title_box.addWidget(self.subtitle_label)
        title_box.addWidget(self.hero_hint_label)

        status_box = QVBoxLayout()
        status_box.setSpacing(8)
        status_box.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        self.health_badge = QLabel("● Stabil")
        self.health_badge.setObjectName("dashboardHealthBadge")
        self.health_badge.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.last_updated_label = QLabel("Zuletzt aktualisiert: -")
        self.last_updated_label.setObjectName("dashboardLastUpdated")
        self.last_updated_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        status_box.addWidget(self.health_badge, alignment=Qt.AlignmentFlag.AlignRight)
        status_box.addWidget(self.last_updated_label, alignment=Qt.AlignmentFlag.AlignRight)

        top_header_row.addLayout(title_box, 1)
        top_header_row.addLayout(status_box, 0)

        top_layout.addLayout(top_header_row)
        layout.addWidget(top_container)

    def _create_stats_grid(self, layout: QVBoxLayout) -> None:
        """Erstellt das Raster mit den Statistik-Karten."""
        stats_container = QFrame()
        stats_container.setObjectName("dashboardStatsContainer")

        container_layout = QVBoxLayout(stats_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.stats_grid = QGridLayout()
        self.stats_grid.setHorizontalSpacing(18)
        self.stats_grid.setVerticalSpacing(18)
        self.stats_grid.setColumnStretch(0, 1)
        self.stats_grid.setColumnStretch(1, 1)
        self.stats_grid.setColumnStretch(2, 1)

        self.members_card = StatCard(
            title="Mitglieder",
            value="0",
            subtitle="Aktive Mitglieder im System",
            icon="👥",
            accent="blue",
        )
        self.employees_card = StatCard(
            title="Mitarbeiter",
            value="0",
            subtitle="Aktuell erfasste Mitarbeiter",
            icon="🧑‍💼",
            accent="purple",
        )
        self.products_card = StatCard(
            title="Produkte",
            value="0",
            subtitle="Verfügbare Artikel im Lager",
            icon="📦",
            accent="orange",
        )
        self.equipment_card = StatCard(
            title="Geräte",
            value="0",
            subtitle="Geräte im Einsatz oder verfügbar",
            icon="🏋",
            accent="green",
        )
        self.vending_card = StatCard(
            title="Automaten",
            value="0",
            subtitle="Aktive Snack- und Getränkeautomaten",
            icon="▣",
            accent="blue",
        )
        self.low_stock_card = StatCard(
            title="Kritische Bestände",
            value="0",
            subtitle="Produkte mit niedrigem Lagerstand",
            icon="⚠",
            accent="red",
        )

        self.stats_grid.addWidget(self.members_card, 0, 0)
        self.stats_grid.addWidget(self.employees_card, 0, 1)
        self.stats_grid.addWidget(self.products_card, 0, 2)
        self.stats_grid.addWidget(self.equipment_card, 1, 0)
        self.stats_grid.addWidget(self.vending_card, 1, 1)
        self.stats_grid.addWidget(self.low_stock_card, 1, 2)

        self._make_card_clickable(self.members_card, "members")
        self._make_card_clickable(self.employees_card, "employees")
        self._make_card_clickable(self.products_card, "products")
        self._make_card_clickable(self.equipment_card, "equipment")
        self._make_card_clickable(self.vending_card, "vending")
        self._make_card_clickable(self.low_stock_card, "products")

        container_layout.addLayout(self.stats_grid)
        layout.addWidget(stats_container)

    def _create_bottom_section(self, layout: QVBoxLayout) -> None:
        """Erstellt die unteren Dashboard-Bereiche."""
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(18)

        left_column = QVBoxLayout()
        left_column.setSpacing(18)

        right_column = QVBoxLayout()
        right_column.setSpacing(18)

        self.activity_card = self._create_activity_card()
        self.quick_actions_card = self._create_quick_actions_card()
        self.analytics_card = self._create_analytics_card()
        self.status_card = self._create_status_card()

        left_column.addWidget(self.activity_card)
        left_column.addWidget(self.quick_actions_card)

        right_column.addWidget(self.analytics_card)
        right_column.addWidget(self.status_card)

        bottom_row.addLayout(left_column, 2)
        bottom_row.addLayout(right_column, 1)

        layout.addLayout(bottom_row)

    def _create_activity_card(self) -> QFrame:
        """Erstellt die Karte für letzte Aktivitäten."""
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Letzte Aktivitäten")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Zuletzt erfasste Vorgänge und Änderungen im System.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.activity_list_layout = QVBoxLayout()
        self.activity_list_layout.setSpacing(10)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(self.activity_list_layout)
        layout.addStretch()

        return card

    def _create_quick_actions_card(self) -> QFrame:
        """Erstellt die Quick-Actions-Karte."""
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Quick Actions")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Wichtige Bereiche direkt öffnen.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        actions_row_1 = QHBoxLayout()
        actions_row_1.setSpacing(12)

        actions_row_2 = QHBoxLayout()
        actions_row_2.setSpacing(12)

        self.quick_member_button = self._build_quick_action_button("➕ Mitglied", "new_member")
        self.quick_product_button = self._build_quick_action_button("📦 Produkt", "new_product")
        self.quick_movement_button = self._build_quick_action_button("🔄 Bewegung", "new_movement")
        self.quick_reports_button = self._build_quick_action_button("📊 Reports", "reports")

        actions_row_1.addWidget(self.quick_member_button)
        actions_row_1.addWidget(self.quick_product_button)

        actions_row_2.addWidget(self.quick_movement_button)
        actions_row_2.addWidget(self.quick_reports_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(actions_row_1)
        layout.addLayout(actions_row_2)

        return card

    def _create_analytics_card(self) -> QFrame:
        """Erstellt die Mini-Analytics-Karte."""
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Mini Analytics")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Kurze Trends für Wachstum und Lagerentwicklung.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.member_trend_title = QLabel("Mitgliedertrend")
        self.member_trend_title.setObjectName("dashboardMetricTitle")

        self.member_trend_chart = QLabel("▁▂▃▄▅▆")
        self.member_trend_chart.setObjectName("dashboardTrendChart")

        self.member_trend_value = QLabel("+0")
        self.member_trend_value.setObjectName("dashboardStatusOk")

        self.stock_trend_title = QLabel("Lagertrend")
        self.stock_trend_title.setObjectName("dashboardMetricTitle")

        self.stock_trend_chart = QLabel("▆▅▄▃▂▁")
        self.stock_trend_chart.setObjectName("dashboardTrendChart")

        self.stock_trend_value = QLabel("-0")
        self.stock_trend_value.setObjectName("dashboardStatusWarn")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)
        layout.addWidget(self.member_trend_title)
        layout.addWidget(self.member_trend_chart)
        layout.addWidget(self.member_trend_value)
        layout.addSpacing(10)
        layout.addWidget(self.stock_trend_title)
        layout.addWidget(self.stock_trend_chart)
        layout.addWidget(self.stock_trend_value)

        return card

    def _create_status_card(self) -> QFrame:
        """Erstellt die Status- und Alert-Karte."""
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Systemstatus & Alerts")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Health-Status und automatische Hinweise.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.health_status_label = QLabel("● Stabil")
        self.health_status_label.setObjectName("dashboardStatusOk")

        self.health_message_label = QLabel("Alle Kernbereiche laufen normal.")
        self.health_message_label.setObjectName("dashboardSectionSubtitle")
        self.health_message_label.setWordWrap(True)

        self.alerts_layout = QVBoxLayout()
        self.alerts_layout.setSpacing(10)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.health_status_label)
        layout.addWidget(self.health_message_label)
        layout.addSpacing(4)
        layout.addLayout(self.alerts_layout)
        layout.addStretch()

        return card

    def _start_live_updates(self) -> None:
        """Startet den Timer für automatische Aktualisierungen."""
        self.live_timer = QTimer(self)
        self.live_timer.setInterval(6000)
        self.live_timer.timeout.connect(self.refresh_data)
        self.live_timer.start()

    def _build_quick_action_button(self, text: str, action_key: str) -> QPushButton:
        """Erstellt einen Quick-Action-Button."""
        button = QPushButton(text)
        button.setObjectName("secondaryButton")
        button.clicked.connect(lambda: self._handle_quick_action(action_key))
        return button

    def _handle_quick_action(self, action_key: str) -> None:
        """Leitet eine Quick Action weiter."""
        if callable(self.quick_action_handler):
            self.quick_action_handler(action_key)

    def _make_card_clickable(self, card: StatCard, page_key: str) -> None:
        """Verknüpft eine Karte mit einem Navigationsziel."""
        card.installEventFilter(self)
        card.setToolTip(f"Öffne {page_key}")
        self._card_targets[card] = page_key

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Behandelt Klicks auf Dashboard-Karten."""
        if watched in self._card_targets and event.type() == QEvent.Type.MouseButtonRelease:
            if isinstance(event, QMouseEvent) and event.button() == Qt.MouseButton.LeftButton:
                target = self._card_targets[watched]
                if callable(self.navigator):
                    self.navigator(target)
                return True

        return super().eventFilter(watched, event)

    def _get_snapshot(self) -> dict[str, Any]:
        """Lädt einen Snapshot oder nutzt Demo-Daten."""
        if callable(self.snapshot_provider):
            snapshot = self.snapshot_provider()
            if isinstance(snapshot, dict):
                return snapshot

        return self._get_demo_snapshot()

    def _get_health_from_snapshot(self, snapshot: dict[str, Any]) -> dict[str, str]:
        """Bestimmt den Health-Status aus Snapshot-Daten."""
        if callable(self.health_provider):
            health = self.health_provider()
            if isinstance(health, dict):
                return health

        low_stock = int(snapshot.get("low_stock", 0))

        if low_stock >= 6:
            return {
                "status": "critical",
                "label": "Kritisch",
                "message": "Mehrere Bestände liegen im kritischen Bereich.",
            }
        if low_stock >= 3:
            return {
                "status": "warning",
                "label": "Warnung",
                "message": "Einige Produkte sollten bald nachbestellt werden.",
            }

        return {
            "status": "ok",
            "label": "Stabil",
            "message": "Alle Kernbereiche laufen im normalen Bereich.",
        }

    def _get_demo_snapshot(self) -> dict[str, Any]:
        """Erstellt Demo-Daten mit kleinen Änderungen."""
        self._demo_tick += 1

        member_variants = [124, 125, 126, 124, 127]
        product_variants = [56, 55, 54, 56, 53]
        equipment_variants = [32, 31, 32, 33, 32]
        low_stock_variants = [4, 3, 5, 4, 4]

        idx = self._demo_tick % 5

        return {
            "members": member_variants[idx],
            "employees": 18,
            "products": product_variants[idx],
            "equipment": equipment_variants[idx],
            "vending": 6,
            "low_stock": low_stock_variants[idx],
            "member_trend": [98, 104, 109, 113, 118, member_variants[idx]],
            "stock_trend": [70, 68, 66, 61, 59, product_variants[idx]],
            "alerts": self._build_demo_alerts(low_stock_variants[idx]),
            "activities": self._build_demo_activities(),
        }

    def _build_demo_alerts(self, low_stock: int) -> list[str]:
        """Erstellt Demo-Alerts."""
        alerts: list[str] = []

        if low_stock >= 4:
            alerts.append(f"Kritischer Lagerbestand bei {low_stock} Produkten")

        alerts.append(
            choice(
                [
                    "1 Automat benötigt Sichtprüfung",
                    "2 Geräte wurden heute aktualisiert",
                    "Mitarbeiterdaten wurden erfolgreich synchronisiert",
                ]
            )
        )

        alerts.append(
            choice(
                [
                    "Produktdatenbank wurde zuletzt vor wenigen Sekunden aktualisiert",
                    "Systemcheck erfolgreich abgeschlossen",
                    "Lagerbewegungen wurden neu geladen",
                ]
            )
        )

        return alerts

    def _build_demo_activities(self) -> list[str]:
        """Erstellt Demo-Aktivitäten."""
        return [
            "Neuer Mitarbeiter wurde angelegt",
            "Lagerbestand von Proteinriegeln aktualisiert",
            "2 Geräte wurden als verfügbar markiert",
            "Automat im Eingangsbereich wurde geprüft",
        ]

    def _get_real_member_trend(self) -> list[int]:
        """Liefert den Mitgliedertrend der letzten sechs Monate."""
        if self.controller is None:
            return []

        try:
            members = self.controller.get_all_members()
            now = datetime.now()
            trend: list[int] = []

            for months_back in range(5, -1, -1):
                target_month = now.month - months_back
                target_year = now.year

                while target_month <= 0:
                    target_month += 12
                    target_year -= 1

                count = 0
                for member in members:
                    created_at = getattr(member, "created_at", None)
                    if (
                        created_at is not None
                        and getattr(created_at, "year", None) == target_year
                        and getattr(created_at, "month", None) == target_month
                    ):
                        count += 1

                trend.append(count)

            return trend
        except Exception:
            return []

    def _get_real_stock_trend(self) -> list[int]:
        """Liefert den Lagertrend der letzten sechs Monate."""
        if self.controller is None:
            return []

        try:
            movements = self.controller.get_movements()
            now = datetime.now()
            trend: list[int] = []

            for months_back in range(5, -1, -1):
                target_month = now.month - months_back
                target_year = now.year

                while target_month <= 0:
                    target_month += 12
                    target_year -= 1

                month_sum = 0
                for movement in movements:
                    timestamp = getattr(movement, "timestamp", None)
                    quantity_change = getattr(movement, "quantity_change", 0)

                    if (
                        timestamp is not None
                        and getattr(timestamp, "year", None) == target_year
                        and getattr(timestamp, "month", None) == target_month
                    ):
                        month_sum += int(quantity_change)

                trend.append(month_sum)

            return trend
        except Exception:
            return []

    def _apply_snapshot(self, snapshot: dict[str, Any]) -> None:
        """Überträgt Snapshot-Daten in die Oberfläche."""
        self.members_card.set_value_animated(int(snapshot.get("members", 0)))
        self.members_card.set_subtitle("Gesamtzahl im System")

        self.employees_card.set_value_animated(int(snapshot.get("employees", 0)))
        self.employees_card.set_subtitle("Aktiv im System")

        self.products_card.set_value_animated(int(snapshot.get("products", 0)))
        self.products_card.set_subtitle("Im Lager verfügbar")

        self.equipment_card.set_value_animated(int(snapshot.get("equipment", 0)))
        self.equipment_card.set_subtitle("Geräte einsatzbereit")

        self.vending_card.set_value_animated(int(snapshot.get("vending", 0)))
        self.vending_card.set_subtitle("Alle derzeit aktiv")

        low_stock = int(snapshot.get("low_stock", 0))
        self.low_stock_card.set_value_animated(low_stock)
        self.low_stock_card.set_subtitle("Sofort prüfen" if low_stock >= 3 else "Stabil")

        self._apply_card_highlight_state(low_stock)
        self._update_activities(snapshot.get("activities", []))
        self._update_analytics(snapshot)
        self._update_health_and_alerts(snapshot)
        self._update_last_refresh_label()

    def _apply_card_highlight_state(self, low_stock: int) -> None:
        """Passt den Status der Bestandskarte an."""
        if low_stock >= 5:
            self.low_stock_card.set_accent("red")
        elif low_stock >= 3:
            self.low_stock_card.set_accent("orange")
        else:
            self.low_stock_card.set_accent("green")

    def _update_activities(self, activities: list[str]) -> None:
        """Aktualisiert den Bereich für letzte Aktivitäten."""
        self._clear_layout(self.activity_list_layout)

        for text in activities[:5]:
            item = QLabel(f"• {text}")
            item.setObjectName("dashboardActivityItem")
            item.setWordWrap(True)
            self.activity_list_layout.addWidget(item)

    def _update_analytics(self, snapshot: dict[str, Any]) -> None:
        """Aktualisiert Trends und Delta-Anzeigen."""
        member_trend = self._get_real_member_trend() or snapshot.get("member_trend", [])
        stock_trend = self._get_real_stock_trend() or snapshot.get("stock_trend", [])

        self.member_trend_chart.setText(self._to_sparkline(member_trend))
        self.stock_trend_chart.setText(self._to_sparkline(stock_trend))

        self.member_trend_value.setText(self._format_delta(member_trend))
        self.stock_trend_value.setText(self._format_delta(stock_trend))

    def _update_health_and_alerts(self, snapshot: dict[str, Any]) -> None:
        """Aktualisiert Health-Anzeige und Alerts."""
        health = self._get_health_from_snapshot(snapshot)
        alerts = snapshot.get("alerts", [])

        status = health.get("status", "ok")
        label = health.get("label", "Stabil")
        message = health.get("message", "System läuft normal.")

        badge_text = f"● {label}"
        self.health_badge.setText(badge_text)
        self.health_status_label.setText(badge_text)
        self.health_message_label.setText(message)

        if status == "critical":
            object_name = "dashboardStatusCritical"
        elif status == "warning":
            object_name = "dashboardStatusWarn"
        else:
            object_name = "dashboardStatusOk"

        self.health_badge.setObjectName(object_name)
        self.health_status_label.setObjectName(object_name)

        self.health_badge.style().unpolish(self.health_badge)
        self.health_badge.style().polish(self.health_badge)
        self.health_status_label.style().unpolish(self.health_status_label)
        self.health_status_label.style().polish(self.health_status_label)

        self._clear_layout(self.alerts_layout)
        for alert in alerts[:4]:
            alert_label = QLabel(f"⚠ {alert}")
            alert_label.setObjectName("dashboardAlertItem")
            alert_label.setWordWrap(True)
            self.alerts_layout.addWidget(alert_label)

    def _update_last_refresh_label(self) -> None:
        """Aktualisiert die Zeit der letzten Aktualisierung."""
        now = QDateTime.currentDateTime().toString("dd.MM.yyyy HH:mm:ss")
        self.last_updated_label.setText(f"Zuletzt aktualisiert: {now}")

    def refresh_data(self) -> None:
        """Aktualisiert das komplette Dashboard."""
        try:
            snapshot = self._get_snapshot()
            self._apply_snapshot(snapshot)
        except Exception:
            self._apply_snapshot(self._get_demo_snapshot())

    def _clear_layout(self, layout: QVBoxLayout | QHBoxLayout | QGridLayout) -> None:
        """Entfernt alle Inhalte aus einem Layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()

            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self._clear_layout(child_layout)

    def _to_sparkline(self, values: list[int]) -> str:
        """Erzeugt eine einfache Sparkline aus Zahlenwerten."""
        if not values:
            return "–"

        bars = "▁▂▃▄▅▆▇█"
        minimum = min(values)
        maximum = max(values)

        if minimum == maximum:
            return bars[3] * len(values)

        result: list[str] = []
        for value in values:
            normalized = (value - minimum) / (maximum - minimum)
            index = min(int(normalized * (len(bars) - 1)), len(bars) - 1)
            result.append(bars[index])

        return "".join(result)

    def _format_delta(self, values: list[int]) -> str:
        """Formatiert die Veränderung eines Trends."""
        if len(values) < 2:
            return "±0"

        delta = values[-1] - values[0]

        if delta > 0:
            return f"+{delta} Wachstum"
        if delta < 0:
            return f"{delta} Rückgang"
        return "Stabil"