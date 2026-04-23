from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QMouseEvent
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.ui.widgets.stat_card import StatCard


@dataclass
class ReportRecord:
    """Speichert die aufbereiteten Daten eines Reports."""

    report_id: str
    title: str
    category: str
    period: str
    status: str
    priority: str
    created_by: str
    last_update: str
    summary: str
    export_state: str


class ReportHighlightCard(QFrame):
    """Große klickbare Kachel für einen Report."""

    clicked = pyqtSignal(str)

    def __init__(self, report: ReportRecord, parent: QWidget | None = None) -> None:
        """Initialisiert die Report-Kachel."""
        super().__init__(parent)

        self.report = report
        self._selected = False

        self.setObjectName("reportHighlightCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(220)
        self.setMaximumHeight(240)

        self._create_ui()
        self._refresh_style()

    def _create_ui(self) -> None:
        """Erstellt die Inhalte der Report-Kachel."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.id_label = QLabel(self.report.report_id)
        self.id_label.setObjectName("reportCardBadge")

        self.priority_label = QLabel(self.report.priority)
        self.priority_label.setObjectName("reportCardPriority")
        self._apply_priority_style()

        top_row.addWidget(self.id_label)
        top_row.addStretch()
        top_row.addWidget(self.priority_label)

        self.title_label = QLabel(self.report.title)
        self.title_label.setObjectName("reportCardTitle")
        self.title_label.setWordWrap(True)

        self.meta_label = QLabel(f"{self.report.category} • {self.report.period}")
        self.meta_label.setObjectName("reportCardMeta")
        self.meta_label.setWordWrap(True)

        self.summary_label = QLabel(self.report.summary)
        self.summary_label.setObjectName("reportCardSummary")
        self.summary_label.setWordWrap(True)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(8)

        self.status_label = QLabel(f"● {self.report.status}")
        self._apply_status_style(self.status_label, self.report.status)

        self.export_label = QLabel(self.report.export_state)
        self.export_label.setObjectName("reportCardExport")

        bottom_row.addWidget(self.status_label)
        bottom_row.addStretch()
        bottom_row.addWidget(self.export_label)

        layout.addLayout(top_row)
        layout.addWidget(self.title_label)
        layout.addWidget(self.meta_label)
        layout.addWidget(self.summary_label)
        layout.addStretch()
        layout.addLayout(bottom_row)

    def _apply_priority_style(self) -> None:
        """Setzt den Stil für die Priorität."""
        if self.report.priority == "Hoch":
            self.priority_label.setProperty("priorityLevel", "high")
        elif self.report.priority == "Mittel":
            self.priority_label.setProperty("priorityLevel", "medium")
        else:
            self.priority_label.setProperty("priorityLevel", "low")

    def _apply_status_style(self, label: QLabel, status: str) -> None:
        """Setzt den Stil für den Report-Status."""
        if status == "Fertig":
            label.setObjectName("dashboardStatusOk")
        elif status == "In Arbeit":
            label.setObjectName("dashboardStatusWarn")
        else:
            label.setObjectName("dashboardStatusCritical")

    def set_selected(self, selected: bool) -> None:
        """Markiert die Kachel als ausgewählt oder nicht ausgewählt."""
        self._selected = selected
        self.setProperty("selectedReportCard", selected)
        self._refresh_style()

    def _refresh_style(self) -> None:
        """Aktualisiert den Stil der Kachel."""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Sendet das Klicksignal bei linker Maustaste."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.report.report_id)
        super().mouseReleaseEvent(event)


class ReportsPage(QWidget):
    """Report-Center mit Filterung, Highlight-Kacheln und Detailansicht."""

    TABLE_COLUMNS = [
        "Report-ID",
        "Titel",
        "Kategorie",
        "Zeitraum",
        "Status",
        "Priorität",
        "Erstellt von",
        "Letztes Update",
        "Export",
    ]

    def __init__(self, controller: Any | None = None) -> None:
        """Initialisiert die Report-Seite."""
        super().__init__()

        self.controller = controller
        self.reports: list[ReportRecord] = []
        self.filtered_reports: list[ReportRecord] = []
        self.report_cards: dict[str, ReportHighlightCard] = {}
        self.selected_report_id: str | None = None

        self._create_ui()
        self.refresh_data()

    def _create_ui(self) -> None:
        """Erstellt die komplette Oberfläche der Seite."""
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.page_scroll = QScrollArea()
        self.page_scroll.setWidgetResizable(True)
        self.page_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.page_content = QWidget()
        self.page_layout = QVBoxLayout(self.page_content)
        self.page_layout.setContentsMargins(24, 24, 24, 24)
        self.page_layout.setSpacing(20)

        self.page_layout.addWidget(self._create_executive_summary())
        self.page_layout.addWidget(self._create_toolbar())

        main_row = QHBoxLayout()
        main_row.setSpacing(18)

        self.left_column = self._create_highlight_area()
        self.right_column = self._create_insight_panel()

        main_row.addWidget(self.left_column, 3)
        main_row.addWidget(self.right_column, 2)

        self.page_layout.addLayout(main_row)
        self.page_layout.addWidget(self._create_archive_table())
        self.page_layout.addStretch()

        self.page_scroll.setWidget(self.page_content)
        root_layout.addWidget(self.page_scroll)

    def _create_executive_summary(self) -> QWidget:
        """Erstellt den oberen Übersichtsbereich mit Kennzahlen."""
        card = QFrame()
        card.setObjectName("reportsHeroCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)

        title = QLabel("Executive Report Center")
        title.setObjectName("reportsHeroTitle")

        subtitle = QLabel(
            "Analysecenter für Management-Reports und aktuell verfügbare Auswertungen."
        )
        subtitle.setObjectName("reportsHeroSubtitle")
        subtitle.setWordWrap(True)

        stats_grid = QGridLayout()
        stats_grid.setHorizontalSpacing(18)
        stats_grid.setVerticalSpacing(18)

        self.total_reports_card = StatCard(
            title="Reports gesamt",
            value="0",
            subtitle="Alle sichtbaren Reports",
            icon="📊",
            accent="blue",
        )
        self.finished_card = StatCard(
            title="Fertig",
            value="0",
            subtitle="Abgeschlossene Reports",
            icon="✅",
            accent="green",
        )
        self.in_progress_card = StatCard(
            title="In Arbeit",
            value="0",
            subtitle="Aktuell in Bearbeitung",
            icon="🛠",
            accent="orange",
        )
        self.high_priority_card = StatCard(
            title="Hohe Priorität",
            value="0",
            subtitle="Sofort relevante Reports",
            icon="🚨",
            accent="red",
        )

        stats_grid.addWidget(self.total_reports_card, 0, 0)
        stats_grid.addWidget(self.finished_card, 0, 1)
        stats_grid.addWidget(self.in_progress_card, 0, 2)
        stats_grid.addWidget(self.high_priority_card, 0, 3)

        for col in range(4):
            stats_grid.setColumnStretch(col, 1)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(stats_grid)

        return card

    def _create_toolbar(self) -> QWidget:
        """Erstellt Suchfeld, Filter und Aktualisierungsbutton."""
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Report-Steuerung")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Reports filtern, durchsuchen und neu laden.")
        subtitle.setObjectName("dashboardSectionSubtitle")

        controls = QHBoxLayout()
        controls.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Suche nach Titel, Kategorie, Report-ID oder Ersteller ..."
        )
        self.search_input.textChanged.connect(self.apply_filters)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Alle Status", "Fertig", "In Arbeit", "Geplant"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)

        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["Alle Prioritäten", "Hoch", "Mittel", "Niedrig"])
        self.priority_filter.currentTextChanged.connect(self.apply_filters)

        self.category_filter = QComboBox()
        self.category_filter.addItems(
            ["Alle Kategorien", "Lager", "Mitglieder", "Finanzen", "Geräte", "Automaten"]
        )
        self.category_filter.currentTextChanged.connect(self.apply_filters)

        self.refresh_button = QPushButton("🔄 Neu laden")
        self.refresh_button.setObjectName("secondaryButton")
        self.refresh_button.clicked.connect(self.refresh_data)

        controls.addWidget(self.search_input, 2)
        controls.addWidget(self.status_filter, 1)
        controls.addWidget(self.priority_filter, 1)
        controls.addWidget(self.category_filter, 1)
        controls.addWidget(self.refresh_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(controls)

        return card

    def _create_highlight_area(self) -> QWidget:
        """Erstellt den Bereich mit den Highlight-Kacheln."""
        container = QFrame()
        container.setObjectName("dashboardBottomCard")
        container.setMinimumHeight(620)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Highlight Reports")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Verfügbare Reports als Management-Kacheln.")
        subtitle.setObjectName("dashboardSectionSubtitle")

        self.highlight_scroll = QScrollArea()
        self.highlight_scroll.setWidgetResizable(True)
        self.highlight_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.highlight_scroll.setMinimumHeight(500)

        self.highlight_content = QWidget()
        self.highlight_grid = QGridLayout(self.highlight_content)
        self.highlight_grid.setContentsMargins(0, 0, 0, 0)
        self.highlight_grid.setHorizontalSpacing(16)
        self.highlight_grid.setVerticalSpacing(16)

        self.highlight_scroll.setWidget(self.highlight_content)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.highlight_scroll)

        return container

    def _create_insight_panel(self) -> QWidget:
        """Erstellt den Detail- und Insight-Bereich."""
        container = QFrame()
        container.setObjectName("dashboardBottomCard")
        container.setMinimumHeight(620)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Management Insight Panel")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Zusammenfassung und Kernaussagen des ausgewählten Reports.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.selected_title = QLabel("Kein Report ausgewählt")
        self.selected_title.setObjectName("reportsSelectedTitle")
        self.selected_title.setWordWrap(True)

        self.selected_status = QLabel("● -")
        self.selected_status.setObjectName("dashboardSectionSubtitle")

        self.detail_id = self._build_detail_label("Report-ID", "-")
        self.detail_category = self._build_detail_label("Kategorie", "-")
        self.detail_period = self._build_detail_label("Zeitraum", "-")
        self.detail_priority = self._build_detail_label("Priorität", "-")
        self.detail_creator = self._build_detail_label("Erstellt von", "-")
        self.detail_update = self._build_detail_label("Letztes Update", "-")
        self.detail_export = self._build_detail_label("Exportstatus", "-")

        insight_title = QLabel("Executive Summary")
        insight_title.setObjectName("reportsInsightTitle")

        self.insight_box = QLabel("-")
        self.insight_box.setObjectName("reportsInsightBox")
        self.insight_box.setWordWrap(True)
        self.insight_box.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        ampel_title = QLabel("Management-Ampel")
        ampel_title.setObjectName("reportsInsightTitle")

        self.ampel_label = QLabel("● Keine Bewertung")
        self.ampel_label.setObjectName("reportsAmpelNeutral")

        quick_metrics_title = QLabel("Schnellbewertung")
        quick_metrics_title.setObjectName("reportsInsightTitle")

        self.metric_1 = QLabel("• Priorität: -")
        self.metric_1.setObjectName("dashboardActivityItem")

        self.metric_2 = QLabel("• Status: -")
        self.metric_2.setObjectName("dashboardActivityItem")

        self.metric_3 = QLabel("• Export: -")
        self.metric_3.setObjectName("dashboardActivityItem")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(6)
        layout.addWidget(self.selected_title)
        layout.addWidget(self.selected_status)
        layout.addWidget(self.detail_id)
        layout.addWidget(self.detail_category)
        layout.addWidget(self.detail_period)
        layout.addWidget(self.detail_priority)
        layout.addWidget(self.detail_creator)
        layout.addWidget(self.detail_update)
        layout.addWidget(self.detail_export)
        layout.addSpacing(8)
        layout.addWidget(insight_title)
        layout.addWidget(self.insight_box)
        layout.addWidget(ampel_title)
        layout.addWidget(self.ampel_label)
        layout.addWidget(quick_metrics_title)
        layout.addWidget(self.metric_1)
        layout.addWidget(self.metric_2)
        layout.addWidget(self.metric_3)
        layout.addStretch()

        return container

    def _create_archive_table(self) -> QWidget:
        """Erstellt die tabellarische Archivansicht."""
        card = QFrame()
        card.setObjectName("dashboardBottomCard")
        card.setMinimumHeight(380)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Report-Archiv")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Tabellarische Übersicht aller gefilterten Reports.")
        subtitle.setObjectName("dashboardSectionSubtitle")

        self.report_table = QTableWidget()
        self.report_table.setColumnCount(len(self.TABLE_COLUMNS))
        self.report_table.setHorizontalHeaderLabels(self.TABLE_COLUMNS)
        self.report_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.report_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.report_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.report_table.setAlternatingRowColors(True)
        self.report_table.setSortingEnabled(True)
        self.report_table.verticalHeader().setVisible(False)
        self.report_table.horizontalHeader().setStretchLastSection(True)
        self.report_table.setMinimumHeight(250)
        self.report_table.itemSelectionChanged.connect(self._select_from_table)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.report_table)

        return card

    def _build_detail_label(self, title: str, value: str) -> QLabel:
        """Erstellt ein Detail-Label für den rechten Bereich."""
        label = QLabel(f"<b>{title}:</b><br>{value}")
        label.setObjectName("dashboardActivityItem")
        label.setWordWrap(True)
        return label

    def _build_inventory_report_record(self, report_data: Any) -> ReportRecord:
        """Wandelt den Inventory Report in ein ReportRecord um."""
        if isinstance(report_data, dict):
            summary = str(
                report_data.get("summary")
                or report_data.get("description")
                or report_data.get("result")
                or report_data.get("report")
                or report_data
            )
            period = str(report_data.get("period", "Aktuell"))
            last_update = str(report_data.get("last_update", "Aktuell"))
        else:
            summary = str(report_data)
            period = "Aktuell"
            last_update = "Aktuell"

        return ReportRecord(
            report_id="REP-INVENTORY-001",
            title="Inventory Report",
            category="Lager",
            period=period,
            status="Fertig",
            priority="Hoch",
            created_by="System",
            last_update=last_update,
            summary=summary,
            export_state="Nicht exportiert",
        )

    def refresh_data(self) -> None:
        """Lädt die verfügbaren Reports neu."""
        try:
            if self.controller is not None:
                report_data = self.controller.generate_inventory_report()
                self.reports = [self._build_inventory_report_record(report_data)]
            else:
                self.reports = []

            self.apply_filters()
        except Exception:
            self.reports = []
            self.apply_filters()

    def apply_filters(self) -> None:
        """Filtert Reports nach Suche, Status, Priorität und Kategorie."""
        search_text = self.search_input.text().strip().lower()
        selected_status = self.status_filter.currentText()
        selected_priority = self.priority_filter.currentText()
        selected_category = self.category_filter.currentText()

        result: list[ReportRecord] = []

        for report in self.reports:
            searchable = " ".join(
                [
                    report.report_id,
                    report.title,
                    report.category,
                    report.created_by,
                    report.summary,
                ]
            ).lower()

            matches_search = search_text in searchable
            matches_status = selected_status == "Alle Status" or report.status == selected_status
            matches_priority = (
                selected_priority == "Alle Prioritäten" or report.priority == selected_priority
            )
            matches_category = (
                selected_category == "Alle Kategorien" or report.category == selected_category
            )

            if matches_search and matches_status and matches_priority and matches_category:
                result.append(report)

        self.filtered_reports = result
        self._rebuild_highlight_cards()
        self._populate_table()
        self._update_stats()

        if self.filtered_reports:
            current = self._find_report(self.selected_report_id)
            if current is None:
                self.select_report(self.filtered_reports[0].report_id)
            else:
                self.select_report(current.report_id)
        else:
            self._clear_detail_panel()

    def _rebuild_highlight_cards(self) -> None:
        """Erstellt die Highlight-Kacheln der gefilterten Reports neu."""
        while self.highlight_grid.count():
            item = self.highlight_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.report_cards.clear()

        for index, report in enumerate(self.filtered_reports):
            card = ReportHighlightCard(report)
            card.clicked.connect(self.select_report)
            self.report_cards[report.report_id] = card

            row = index // 2
            col = index % 2
            self.highlight_grid.addWidget(card, row, col)

        self.highlight_grid.setColumnStretch(0, 1)
        self.highlight_grid.setColumnStretch(1, 1)

    def _apply_table_item_color(
        self,
        item: QTableWidgetItem,
        column: int,
        report: ReportRecord,
    ) -> None:
        """Setzt passende Farben für Status und Priorität."""
        if column == 4:
            if report.status == "Fertig":
                item.setForeground(QColor("#8df0c4"))
            elif report.status == "In Arbeit":
                item.setForeground(QColor("#ffbb72"))
            else:
                item.setForeground(QColor("#ff8aa5"))

        if column == 5:
            if report.priority == "Hoch":
                item.setForeground(QColor("#ff8aa5"))
            elif report.priority == "Mittel":
                item.setForeground(QColor("#ffbb72"))
            else:
                item.setForeground(QColor("#8df0c4"))

    def _populate_table(self) -> None:
        """Füllt die Archivtabelle mit den gefilterten Reports."""
        self.report_table.setSortingEnabled(False)
        self.report_table.setRowCount(len(self.filtered_reports))
        self.report_table.clearContents()

        for row, report in enumerate(self.filtered_reports):
            values = [
                report.report_id,
                report.title,
                report.category,
                report.period,
                report.status,
                report.priority,
                report.created_by,
                report.last_update,
                report.export_state,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self._apply_table_item_color(item, col, report)
                self.report_table.setItem(row, col, item)

        self.report_table.resizeColumnsToContents()
        self.report_table.setSortingEnabled(True)

        if self.filtered_reports and self.report_table.rowCount() > 0:
            self.report_table.selectRow(0)

    def _select_from_table(self) -> None:
        """Übernimmt die Auswahl aus der Tabelle in die Detailansicht."""
        row = self.report_table.currentRow()
        if row < 0:
            return

        report_id_item = self.report_table.item(row, 0)
        if report_id_item is None:
            return

        self.select_report(report_id_item.text())

    def select_report(self, report_id: str) -> None:
        """Wählt einen Report aus und aktualisiert die Detailansicht."""
        self.selected_report_id = report_id
        report = self._find_report(report_id)

        if report is None:
            self._clear_detail_panel()
            return

        self.selected_title.setText(report.title)
        self.selected_status.setText(f"● {report.status}")

        if report.status == "Fertig":
            self.selected_status.setObjectName("dashboardStatusOk")
        elif report.status == "In Arbeit":
            self.selected_status.setObjectName("dashboardStatusWarn")
        else:
            self.selected_status.setObjectName("dashboardStatusCritical")

        self.selected_status.style().unpolish(self.selected_status)
        self.selected_status.style().polish(self.selected_status)

        self.detail_id.setText(f"<b>Report-ID:</b><br>{report.report_id}")
        self.detail_category.setText(f"<b>Kategorie:</b><br>{report.category}")
        self.detail_period.setText(f"<b>Zeitraum:</b><br>{report.period}")
        self.detail_priority.setText(f"<b>Priorität:</b><br>{report.priority}")
        self.detail_creator.setText(f"<b>Erstellt von:</b><br>{report.created_by}")
        self.detail_update.setText(f"<b>Letztes Update:</b><br>{report.last_update}")
        self.detail_export.setText(f"<b>Exportstatus:</b><br>{report.export_state}")

        self.insight_box.setText(report.summary)
        self.metric_1.setText(f"• Priorität: {report.priority}")
        self.metric_2.setText(f"• Status: {report.status}")
        self.metric_3.setText(f"• Export: {report.export_state}")

        if report.priority == "Hoch":
            self.ampel_label.setText("● ROT – Management-Fokus empfohlen")
            self.ampel_label.setObjectName("reportsAmpelRed")
        elif report.priority == "Mittel":
            self.ampel_label.setText("● GELB – Beobachten und nachfassen")
            self.ampel_label.setObjectName("reportsAmpelYellow")
        else:
            self.ampel_label.setText("● GRÜN – Stabil und kontrolliert")
            self.ampel_label.setObjectName("reportsAmpelGreen")

        self.ampel_label.style().unpolish(self.ampel_label)
        self.ampel_label.style().polish(self.ampel_label)

        for current_id, card in self.report_cards.items():
            card.set_selected(current_id == report_id)

    def _clear_detail_panel(self) -> None:
        """Setzt die Detailansicht auf den Standardzustand zurück."""
        self.selected_title.setText("Kein Report ausgewählt")
        self.selected_status.setText("● -")
        self.selected_status.setObjectName("dashboardSectionSubtitle")
        self.selected_status.style().unpolish(self.selected_status)
        self.selected_status.style().polish(self.selected_status)

        self.detail_id.setText("<b>Report-ID:</b><br>-")
        self.detail_category.setText("<b>Kategorie:</b><br>-")
        self.detail_period.setText("<b>Zeitraum:</b><br>-")
        self.detail_priority.setText("<b>Priorität:</b><br>-")
        self.detail_creator.setText("<b>Erstellt von:</b><br>-")
        self.detail_update.setText("<b>Letztes Update:</b><br>-")
        self.detail_export.setText("<b>Exportstatus:</b><br>-")
        self.insight_box.setText("-")
        self.metric_1.setText("• Priorität: -")
        self.metric_2.setText("• Status: -")
        self.metric_3.setText("• Export: -")
        self.ampel_label.setText("● Keine Bewertung")
        self.ampel_label.setObjectName("reportsAmpelNeutral")
        self.ampel_label.style().unpolish(self.ampel_label)
        self.ampel_label.style().polish(self.ampel_label)

        for card in self.report_cards.values():
            card.set_selected(False)

    def _find_report(self, report_id: str | None) -> ReportRecord | None:
        """Sucht einen Report anhand seiner ID."""
        if report_id is None:
            return None

        for report in self.filtered_reports:
            if report.report_id == report_id:
                return report

        return None

    def _update_stats(self) -> None:
        """Aktualisiert die Kennzahlenkarten."""
        total = len(self.filtered_reports)
        finished = sum(1 for report in self.filtered_reports if report.status == "Fertig")
        in_progress = sum(1 for report in self.filtered_reports if report.status == "In Arbeit")
        high_priority = sum(1 for report in self.filtered_reports if report.priority == "Hoch")

        self.total_reports_card.set_value_animated(total)
        self.finished_card.set_value_animated(finished)
        self.in_progress_card.set_value_animated(in_progress)
        self.high_priority_card.set_value_animated(high_priority)