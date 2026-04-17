import sys
from dataclasses import dataclass
from typing import List

from PyQt6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, Qt, pyqtSignal
from PyQt6.QtGui import QAction, QColor, QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QSpinBox,
)


# =========================
# Demo-Daten / Platzhalter
# =========================

@dataclass
class InventoryItem:
    article_no: str
    name: str
    category: str
    stock: int
    min_stock: int
    location: str


DEMO_ITEMS: List[InventoryItem] = [
    InventoryItem("FG-001", "Protein Powder Vanilla", "Supplement", 42, 15, "Regal A1"),
    InventoryItem("FG-002", "Shaker Bottle", "Merch", 18, 10, "Regal B2"),
    InventoryItem("FG-003", "Resistance Band Set", "Equipment", 9, 12, "Lager C1"),
    InventoryItem("FG-004", "Gym Towels", "Consumables", 73, 30, "Textil T1"),
    InventoryItem("FG-005", "Cleaning Spray", "Hygiene", 25, 8, "Hygiene H3"),
    InventoryItem("FG-006", "Yoga Mat", "Equipment", 11, 6, "Regal C4"),
]


# =========================
# Hilfs-Widgets / Styling
# =========================

class GlassCard(QFrame):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("glassCard")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(18, 18, 18, 18)
        self.outer_layout.setSpacing(10)

        if title:
            label = QLabel(title)
            label.setObjectName("cardTitle")
            self.outer_layout.addWidget(label)

        self._add_shadow()

    def _add_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(shadow)


class StatCard(GlassCard):
    def __init__(self, title: str, value: str, accent: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("statCard")
        self.outer_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("statTitle")

        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setProperty("accent", accent)

        dot = QLabel()
        dot.setFixedSize(14, 14)
        dot.setStyleSheet(f"background:{accent}; border-radius:7px;")

        row = QHBoxLayout()
        row.addWidget(dot)
        row.addWidget(title_label)
        row.addStretch()

        self.outer_layout.addLayout(row)
        self.outer_layout.addWidget(value_label)


class AnimatedStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_animation = None

    def slide_to_index(self, index: int):
        if index == self.currentIndex() or index < 0 or index >= self.count():
            return

        next_widget = self.widget(index)
        current_widget = self.currentWidget()

        width = self.frameRect().width()
        height = self.frameRect().height()

        direction = 1 if index > self.currentIndex() else -1
        next_widget.setGeometry(direction * width, 0, width, height)
        next_widget.show()
        next_widget.raise_()

        current_anim = QPropertyAnimation(current_widget, b"pos", self)
        current_anim.setDuration(260)
        current_anim.setStartValue(current_widget.pos())
        current_anim.setEndValue(QPoint(-direction * width, 0))
        current_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        next_anim = QPropertyAnimation(next_widget, b"pos", self)
        next_anim.setDuration(260)
        next_anim.setStartValue(QPoint(direction * width, 0))
        next_anim.setEndValue(QPoint(0, 0))
        next_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self._current_animation = (current_anim, next_anim)
        current_anim.start()
        next_anim.start()
        self.setCurrentIndex(index)


class SidebarButton(QPushButton):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(48)
        self.setObjectName("sidebarButton")


# =========================
# Dialog
# =========================

class InventoryDialog(QDialog):
    submitted = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Artikel hinzufügen")
        self.setModal(True)
        self.resize(430, 320)
        self.setObjectName("inventoryDialog")

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(12)

        self.article_no = QLineEdit()
        self.name = QLineEdit()
        self.category = QComboBox()
        self.category.addItems(["Supplement", "Merch", "Equipment", "Consumables", "Hygiene"])
        self.stock = QSpinBox()
        self.stock.setMaximum(100000)
        self.min_stock = QSpinBox()
        self.min_stock.setMaximum(100000)
        self.location = QLineEdit()

        form.addRow("Artikelnummer", self.article_no)
        form.addRow("Name", self.name)
        form.addRow("Kategorie", self.category)
        form.addRow("Bestand", self.stock)
        form.addRow("Mindestbestand", self.min_stock)
        form.addRow("Lagerort", self.location)

        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("Abbrechen")
        save_btn = QPushButton("Speichern")
        cancel_btn.setObjectName("secondaryButton")
        save_btn.setObjectName("primaryButton")
        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self._submit)

        btn_row.addStretch()
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(save_btn)

        layout.addLayout(form)
        layout.addStretch()
        layout.addLayout(btn_row)

    def _submit(self):
        if not self.article_no.text().strip() or not self.name.text().strip():
            QMessageBox.warning(self, "Fehlende Daten", "Artikelnummer und Name sind Pflichtfelder.")
            return

        self.submitted.emit(
            {
                "article_no": self.article_no.text().strip(),
                "name": self.name.text().strip(),
                "category": self.category.currentText(),
                "stock": self.stock.value(),
                "min_stock": self.min_stock.value(),
                "location": self.location.text().strip(),
            }
        )
        self.accept()


# =========================
# Pages
# =========================

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(20)

        header = QLabel("FitnessGym Lager-Dashboard")
        header.setObjectName("pageTitle")
        subtitle = QLabel("Echtzeit-Übersicht über Bestand, kritische Artikel und Lagerstatus")
        subtitle.setObjectName("pageSubtitle")

        layout.addWidget(header)
        layout.addWidget(subtitle)

        stats_grid = QGridLayout()
        stats_grid.setHorizontalSpacing(16)
        stats_grid.setVerticalSpacing(16)
        stats_grid.addWidget(StatCard("Artikel gesamt", "186", "#4CC9F0"), 0, 0)
        stats_grid.addWidget(StatCard("Kritische Artikel", "07", "#F72585"), 0, 1)
        stats_grid.addWidget(StatCard("Lagerwert", "€ 12.480", "#90BE6D"), 0, 2)
        stats_grid.addWidget(StatCard("Heute gebucht", "23", "#F9C74F"), 0, 3)
        layout.addLayout(stats_grid)

        alerts = GlassCard("Warnungen")
        for text in [
            "Resistance Band Set unterschreitet Mindestbestand.",
            "Pre-Workout Mango erreicht Nachbestellgrenze.",
            "Hygiene-Regal H3 benötigt Bestandsprüfung.",
        ]:
            row = QLabel(f"• {text}")
            row.setObjectName("listItem")
            alerts.outer_layout.addWidget(row)
        layout.addWidget(alerts)

        quick = GlassCard("Schnellaktionen")
        btn_row = QHBoxLayout()
        for text in ["Wareneingang", "Warenausgang", "Inventur starten", "PDF-Report"]:
            b = QPushButton(text)
            b.setObjectName("secondaryButton")
            btn_row.addWidget(b)
        quick.outer_layout.addLayout(btn_row)
        layout.addWidget(quick)
        layout.addStretch()


class InventoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.items = list(DEMO_ITEMS)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(18)

        title = QLabel("Lagerbestand")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Artikelverwaltung für Supplements, Merchandise und Studio-Ausstattung")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        toolbar = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Artikel suchen ...")
        self.search.textChanged.connect(self.refresh_table)

        self.category_filter = QComboBox()
        self.category_filter.addItems(["Alle Kategorien", "Supplement", "Merch", "Equipment", "Consumables", "Hygiene"])
        self.category_filter.currentTextChanged.connect(self.refresh_table)

        add_btn = QPushButton("+ Artikel hinzufügen")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.open_add_dialog)

        toolbar.addWidget(self.search, 1)
        toolbar.addWidget(self.category_filter)
        toolbar.addWidget(add_btn)
        layout.addLayout(toolbar)

        card = GlassCard()
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Artikel-Nr.", "Name", "Kategorie", "Bestand", "Min.", "Lagerort"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        card.outer_layout.addWidget(self.table)
        layout.addWidget(card)

        self.refresh_table()

    def open_add_dialog(self):
        dialog = InventoryDialog(self)
        dialog.submitted.connect(self.add_item)
        dialog.exec()

    def add_item(self, data: dict):
        self.items.append(
            InventoryItem(
                article_no=data["article_no"],
                name=data["name"],
                category=data["category"],
                stock=data["stock"],
                min_stock=data["min_stock"],
                location=data["location"],
            )
        )
        self.refresh_table()
        QMessageBox.information(self, "Erfolg", "Artikel wurde hinzugefügt.")

    def refresh_table(self):
        search_text = self.search.text().strip().lower()
        category = self.category_filter.currentText()

        filtered = []
        for item in self.items:
            if category != "Alle Kategorien" and item.category != category:
                continue
            if search_text and search_text not in f"{item.article_no} {item.name} {item.location}".lower():
                continue
            filtered.append(item)

        self.table.setRowCount(len(filtered))
        for row, item in enumerate(filtered):
            values = [
                item.article_no,
                item.name,
                item.category,
                str(item.stock),
                str(item.min_stock),
                item.location,
            ]
            for col, value in enumerate(values):
                twi = QTableWidgetItem(value)
                if col == 3 and item.stock < item.min_stock:
                    twi.setForeground(QColor("#F72585"))
                self.table.setItem(row, col, twi)


class MovementsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(18)

        title = QLabel("Lagerbewegungen")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Wareneingänge, Verbrauch, Umlagerungen und Inventurkorrekturen")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        card = GlassCard()
        table = QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(5)
        table.setHorizontalHeaderLabels(["Zeit", "Artikel", "Typ", "Menge", "Grund"])
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        rows = [
            ["08:10", "Protein Powder Vanilla", "Eingang", "+20", "Lieferung"],
            ["09:25", "Gym Towels", "Ausgang", "-8", "Studioverbrauch"],
            ["10:40", "Cleaning Spray", "Ausgang", "-3", "Reinigung"],
            ["11:05", "Shaker Bottle", "Eingang", "+12", "Shopbestand"],
            ["12:30", "Resistance Band Set", "Korrektur", "+2", "Inventur"],
        ]
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                table.setItem(r, c, QTableWidgetItem(value))

        card.outer_layout.addWidget(table)
        layout.addWidget(card)
        layout.addStretch()


class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(18)

        title = QLabel("Berichte & Analysen")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Export, Reportgenerierung und Management-Übersicht")
        subtitle.setObjectName("pageSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)

        reports = [
            ("Lagerbestandsbericht", "Kompletter Überblick über alle Artikel inklusive Mindestbestände."),
            ("Nachbestellliste", "Zeigt nur kritische Artikel für schnelle Disposition."),
            ("Bewegungsreport", "Warenein- und -ausgänge eines gewählten Zeitraums."),
            ("Studioverbrauch", "Analyse des internen Verbrauchs im Fitnessbetrieb."),
        ]

        for i, (headline, text) in enumerate(reports):
            card = GlassCard(headline)
            desc = QLabel(text)
            desc.setWordWrap(True)
            desc.setObjectName("bodyText")
            btn = QPushButton("Öffnen")
            btn.setObjectName("primaryButton")
            btn.clicked.connect(lambda _, h=headline: QMessageBox.information(self, "Report", f"{h} wird später mit der Businesslogik verbunden."))
            card.outer_layout.addWidget(desc)
            card.outer_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignLeft)
            grid.addWidget(card, i // 2, i % 2)

        layout.addLayout(grid)
        layout.addStretch()


# =========================
# Main Window
# =========================

class FitnessGymInventoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FitnessGym Inventory Suite")
        self.resize(1450, 860)
        self.setMinimumSize(1200, 760)

        self._setup_ui()
        self._apply_styles()
        self._animate_window_entry()

    def _setup_ui(self):
        root = QWidget()
        self.setCentralWidget(root)

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = self._build_sidebar()
        content = self._build_content_area()

        root_layout.addWidget(sidebar)
        root_layout.addWidget(content, 1)

        self.statusBar().showMessage("Bereit – Demo-Oberfläche aktiv")

    def _build_sidebar(self) -> QWidget:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(270)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(22, 24, 22, 24)
        layout.setSpacing(14)

        logo = QLabel("FITNESSGYM\nINVENTORY")
        logo.setObjectName("logoLabel")

        section = QLabel("Navigation")
        section.setObjectName("sectionLabel")

        self.nav_buttons = []
        labels = ["Dashboard", "Lagerbestand", "Lagerbewegungen", "Reports"]
        for index, text in enumerate(labels):
            btn = SidebarButton(text)
            btn.clicked.connect(lambda _, i=index: self.switch_page(i))
            self.nav_buttons.append(btn)
            layout.addWidget(btn)

        layout.insertWidget(0, logo)
        layout.insertWidget(1, section)
        layout.addSpacing(10)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        quick_card = QFrame()
        quick_card.setObjectName("quickInfoCard")
        quick_layout = QVBoxLayout(quick_card)
        quick_layout.setContentsMargins(14, 14, 14, 14)
        quick_layout.setSpacing(8)
        quick_layout.addWidget(QLabel("Aktive Warnung"))
        warning = QLabel("7 kritische Artikel")
        warning.setObjectName("warningStrong")
        quick_layout.addWidget(warning)
        quick_layout.addWidget(QLabel("Prüfe die Nachbestellliste im Report-Bereich."))
        layout.addWidget(quick_card)

        self.nav_buttons[0].setChecked(True)
        return sidebar

    def _build_content_area(self) -> QWidget:
        wrapper = QWidget()
        wrapper.setObjectName("contentWrapper")
        outer = QVBoxLayout(wrapper)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(18)

        topbar = QHBoxLayout()
        title_box = QVBoxLayout()
        app_title = QLabel("Smart Warehouse UI")
        app_title.setObjectName("topTitle")
        app_sub = QLabel("Modernes Lager-Frontend für ein Fitnessstudio")
        app_sub.setObjectName("topSubtitle")
        title_box.addWidget(app_title)
        title_box.addWidget(app_sub)

        profile = QPushButton("Manager View")
        profile.setObjectName("secondaryButton")

        topbar.addLayout(title_box)
        topbar.addStretch()
        topbar.addWidget(profile)

        self.stack = AnimatedStackedWidget()
        self.stack.addWidget(DashboardPage())
        self.stack.addWidget(InventoryPage())
        self.stack.addWidget(MovementsPage())
        self.stack.addWidget(ReportsPage())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(self.stack)

        outer.addLayout(topbar)
        outer.addWidget(scroll, 1)
        return wrapper

    def switch_page(self, index: int):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        self.stack.slide_to_index(index)

    def _animate_window_entry(self):
        self._opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self._opacity_anim.setDuration(400)
        self._opacity_anim.setStartValue(0.0)
        self._opacity_anim.setEndValue(1.0)
        self._opacity_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._opacity_anim.start()

    def _apply_styles(self):
        self.setStyleSheet(
            """
            * {
                font-family: 'Segoe UI';
                color: #EAF4F4;
            }
            QMainWindow {
                background: #0B1320;
            }
            #sidebar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #121D30, stop:1 #0F1727);
                border-right: 1px solid rgba(255,255,255,0.06);
            }
            #contentWrapper {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #0C1424, stop:1 #121B2E);
            }
            #logoLabel {
                font-size: 24px;
                font-weight: 800;
                letter-spacing: 1px;
                color: #4CC9F0;
                margin-bottom: 12px;
            }
            #sectionLabel {
                color: rgba(234,244,244,0.55);
                font-size: 12px;
                font-weight: 700;
                text-transform: uppercase;
                margin-top: 10px;
            }
            #sidebarButton {
                text-align: left;
                padding: 12px 16px;
                border-radius: 14px;
                background: transparent;
                border: none;
                font-size: 15px;
                font-weight: 600;
            }
            #sidebarButton:hover {
                background: rgba(76, 201, 240, 0.10);
            }
            #sidebarButton:checked {
                background: rgba(76, 201, 240, 0.16);
                border: 1px solid rgba(76, 201, 240, 0.35);
            }
            #quickInfoCard, #glassCard, #statCard {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.07);
                border-radius: 24px;
            }
            #warningStrong {
                color: #F72585;
                font-size: 20px;
                font-weight: 800;
            }
            #topTitle {
                font-size: 28px;
                font-weight: 800;
            }
            #topSubtitle {
                font-size: 13px;
                color: rgba(234,244,244,0.6);
            }
            #pageTitle {
                font-size: 26px;
                font-weight: 800;
            }
            #pageSubtitle {
                font-size: 14px;
                color: rgba(234,244,244,0.60);
                margin-bottom: 8px;
            }
            #cardTitle {
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 4px;
            }
            #statTitle {
                font-size: 14px;
                font-weight: 600;
                color: rgba(234,244,244,0.75);
            }
            #statValue {
                font-size: 30px;
                font-weight: 900;
            }
            #listItem, #bodyText {
                font-size: 14px;
                color: rgba(234,244,244,0.84);
            }
            QLineEdit, QComboBox, QSpinBox {
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 14px;
                padding: 10px 12px;
                min-height: 20px;
                selection-background-color: #4CC9F0;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 1px solid #4CC9F0;
            }
            QPushButton {
                border: none;
                border-radius: 14px;
                padding: 11px 18px;
                font-weight: 700;
            }
            #primaryButton {
                background: #4CC9F0;
                color: #08111F;
            }
            #primaryButton:hover {
                background: #67D6F4;
            }
            #secondaryButton {
                background: rgba(255,255,255,0.07);
                border: 1px solid rgba(255,255,255,0.10);
                color: #EAF4F4;
            }
            #secondaryButton:hover {
                background: rgba(255,255,255,0.12);
            }
            QTableWidget {
                background: transparent;
                border: none;
                border-radius: 18px;
                gridline-color: transparent;
                alternate-background-color: rgba(255,255,255,0.02);
                selection-background-color: rgba(76, 201, 240, 0.25);
                font-size: 14px;
            }
            QHeaderView::section {
                background: transparent;
                border: none;
                border-bottom: 1px solid rgba(255,255,255,0.08);
                padding: 12px 8px;
                font-weight: 800;
                color: rgba(234,244,244,0.85);
            }
            QTableCornerButton::section {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 12px;
                margin: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255,255,255,0.12);
                min-height: 24px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                height: 0;
                background: none;
            }
            QStatusBar {
                background: #101929;
                color: rgba(234,244,244,0.60);
            }
            #inventoryDialog {
                background: #121B2E;
            }
            QMessageBox {
                background: #121B2E;
            }
            """
        )


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = FitnessGymInventoryWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
