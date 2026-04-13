from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from ui.auth.auth_service import AuthService
from ui.main_window import MainWindow


class ForgotPasswordDialog(QDialog):
    """Dialog zum Zurücksetzen des Passworts."""

    def __init__(self, auth_service: AuthService, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.auth_service = auth_service

        self.setWindowTitle("Passwort vergessen")
        self.setMinimumWidth(430)
        self.setModal(True)

        self._load_styles()
        self._build_ui()

    def _load_styles(self) -> None:
        qss_path = Path(__file__).resolve().parent.parent / "styles" / "auth.qss"
        if qss_path.exists():
            with qss_path.open("r", encoding="utf-8") as file:
                self.setStyleSheet(file.read())

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Passwort zurücksetzen")
        title.setObjectName("authTitle")

        subtitle = QLabel("Geben Sie Benutzername und ein neues Passwort ein.")
        subtitle.setObjectName("authSubtitle")
        subtitle.setWordWrap(True)

        self.message_label = QLabel("")
        self.message_label.setObjectName("messageLabel")
        self.message_label.setWordWrap(True)

        form = QFormLayout()
        form.setSpacing(12)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Benutzername")

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Neues Passwort")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Passwort bestätigen")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.returnPressed.connect(self.handle_reset)

        form.addRow("Benutzername:", self.username_input)
        form.addRow("Neues Passwort:", self.new_password_input)
        form.addRow("Bestätigen:", self.confirm_password_input)

        button_row = QHBoxLayout()

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.setObjectName("secondaryButton")
        self.cancel_button.clicked.connect(self.reject)

        self.reset_button = QPushButton("Zurücksetzen")
        self.reset_button.setObjectName("primaryButton")
        self.reset_button.clicked.connect(self.handle_reset)

        button_row.addWidget(self.cancel_button)
        button_row.addWidget(self.reset_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.message_label)
        layout.addLayout(form)
        layout.addLayout(button_row)

    def handle_reset(self) -> None:
        username = self.username_input.text().strip()
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not username or not new_password or not confirm_password:
            self._set_message("Bitte alle Felder ausfüllen.", "error")
            return

        if new_password != confirm_password:
            self._set_message("Die Passwörter stimmen nicht überein.", "error")
            return

        strength, _rules = LoginWindow.evaluate_password_strength_static(new_password)
        if strength == "Schwach":
            self._set_message("Das neue Passwort ist zu schwach.", "error")
            return

        user = self.auth_service.get_user_by_username(username)
        if not user:
            self._set_message("Benutzer nicht gefunden.", "error")
            return

        success, message = self.auth_service.reset_password(
            username=username,
            employee_id=user.get("employee_id", ""),
            new_password=new_password,
        )

        if success:
            self._set_message(message, "success")
            QTimer.singleShot(900, self.accept)
        else:
            self._set_message(message, "error")

    def _set_message(self, text: str, msg_type: str) -> None:
        self.message_label.setText(text)
        self.message_label.setProperty("state", "success" if msg_type == "success" else "error")
        self.message_label.style().unpolish(self.message_label)
        self.message_label.style().polish(self.message_label)


class LoginWindow(QWidget):
    """Reduziertes, modernes Login-/Registrierungsfenster."""

    def __init__(self) -> None:
        super().__init__()

        self.auth = AuthService()
        self.main_window: MainWindow | None = None

        self.setWindowTitle("FitnessCenter Lagerverwaltung - Anmeldung")
        self.setMinimumSize(1100, 760)
        self.resize(1280, 820)

        self.stack = QStackedLayout()

        self._build_ui()
        self._load_styles()
        self._show_initial_page()

    def _build_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(40, 30, 40, 30)
        root_layout.setSpacing(0)
        root_layout.addStretch()

        self.auth_container = QWidget()
        self.auth_container.setObjectName("authContainer")
        self.auth_container.setMinimumWidth(520)
        self.auth_container.setMaximumWidth(580)

        container_layout = QVBoxLayout(self.auth_container)
        container_layout.setContentsMargins(40, 32, 40, 32)
        container_layout.setSpacing(0)

        self.brand_label = QLabel("FITNESSCENTER MANAGEMENT")
        self.brand_label.setObjectName("brandLabel")
        self.brand_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.session_page = self._create_session_page()
        self.login_page = self._create_login_page()
        self.register_page = self._create_register_page()

        self.stack.addWidget(self.session_page)
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)

        container_layout.addWidget(self.brand_label)
        container_layout.addSpacing(18)
        container_layout.addLayout(self.stack)

        root_layout.addWidget(self.auth_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        root_layout.addStretch()

    def _load_styles(self) -> None:
        qss_path = Path(__file__).resolve().parent.parent / "styles" / "auth.qss"

        if qss_path.exists():
            with qss_path.open("r", encoding="utf-8") as file:
                self.setStyleSheet(file.read())

    def _show_initial_page(self) -> None:
        remembered_user = self.auth.get_logged_in_user()

        if remembered_user:
            self.session_welcome_label.setText(f"Weiter als {remembered_user}?")
            self.session_username_label.setText(f"Benutzername: {remembered_user}")
            self.stack.setCurrentIndex(0)
        else:
            self.stack.setCurrentIndex(1)
            self.login_user.setFocus()

    def _create_session_page(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(14)

        icon = QLabel("◉")
        icon.setObjectName("topIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title = QLabel("Willkommen zurück")
        title.setObjectName("authTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        subtitle = QLabel("Es wurde ein gespeicherter Benutzer gefunden.")
        subtitle.setObjectName("authSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.session_message_label = QLabel("")
        self.session_message_label.setObjectName("messageLabel")

        self.session_welcome_label = QLabel("Weiter als letzter Benutzer?")
        self.session_welcome_label.setObjectName("sessionMainLabel")
        self.session_welcome_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.session_username_label = QLabel("")
        self.session_username_label.setObjectName("sessionInfoLabel")
        self.session_username_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.session_role_label = QLabel("")
        self.session_role_label.setObjectName("sessionInfoLabel")
        self.session_role_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.continue_button = QPushButton("Weiter")
        self.continue_button.setObjectName("primaryButton")
        self.continue_button.clicked.connect(self._continue_as_remembered_user)

        self.switch_user_button = QPushButton("Mit anderem Benutzer anmelden")
        self.switch_user_button.setObjectName("secondaryButton")
        self.switch_user_button.clicked.connect(self._switch_user)

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.session_message_label)
        layout.addWidget(self.session_welcome_label)
        layout.addWidget(self.session_username_label)
        layout.addWidget(self.session_role_label)
        layout.addSpacing(12)
        layout.addWidget(self.continue_button)
        layout.addWidget(self.switch_user_button)

        return widget

    def _create_login_page(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(14)

        icon = QLabel("◉")
        icon.setObjectName("topIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title = QLabel("Secure Login")
        title.setObjectName("authTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        subtitle = QLabel("Melden Sie sich mit Ihren Zugangsdaten an.")
        subtitle.setObjectName("authSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.login_msg = QLabel("")
        self.login_msg.setObjectName("messageLabel")

        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Benutzername")

        self.login_pass = QLineEdit()
        self.login_pass.setPlaceholderText("Passwort")
        self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_pass.returnPressed.connect(self.handle_login)

        self.login_toggle_btn = QPushButton("👁")
        self.login_toggle_btn.setObjectName("iconButton")
        self.login_toggle_btn.clicked.connect(self._toggle_login_password)

        pass_layout = QHBoxLayout()
        pass_layout.setSpacing(10)
        pass_layout.addWidget(self.login_pass, 1)
        pass_layout.addWidget(self.login_toggle_btn)

        self.remember_me_checkbox = QCheckBox("Angemeldet bleiben")
        self.remember_me_checkbox.setObjectName("rememberCheckBox")

        self.login_button = QPushButton("Anmelden")
        self.login_button.setObjectName("primaryButton")
        self.login_button.clicked.connect(self.handle_login)

        self.forgot_password_button = QPushButton("Passwort vergessen?")
        self.forgot_password_button.setObjectName("secondaryButton")
        self.forgot_password_button.clicked.connect(self.open_forgot_password_dialog)

        switch_btn = QPushButton("Noch kein Konto? Registrieren")
        switch_btn.setObjectName("secondaryButton")
        switch_btn.clicked.connect(lambda: self._switch_page(2))

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.login_msg)
        layout.addWidget(self.login_user)
        layout.addLayout(pass_layout)
        layout.addWidget(self.remember_me_checkbox)
        layout.addWidget(self.login_button)
        layout.addWidget(self.forgot_password_button)
        layout.addWidget(switch_btn)

        return widget

    def _create_register_page(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(14)

        icon = QLabel("◉")
        icon.setObjectName("topIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title = QLabel("Konto registrieren")
        title.setObjectName("authTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        subtitle = QLabel("Erstellen Sie ein neues Mitarbeiterkonto.")
        subtitle.setObjectName("authSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.reg_msg = QLabel("")
        self.reg_msg.setObjectName("messageLabel")

        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("Benutzername")

        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("Passwort")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass.textChanged.connect(self.update_password_strength)

        self.reg_toggle_btn = QPushButton("👁")
        self.reg_toggle_btn.setObjectName("iconButton")
        self.reg_toggle_btn.clicked.connect(self._toggle_register_passwords)

        pass_layout = QHBoxLayout()
        pass_layout.setSpacing(10)
        pass_layout.addWidget(self.reg_pass, 1)
        pass_layout.addWidget(self.reg_toggle_btn)

        self.reg_pass_confirm = QLineEdit()
        self.reg_pass_confirm.setPlaceholderText("Passwort bestätigen")
        self.reg_pass_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass_confirm.returnPressed.connect(self.handle_register)

        self.password_strength_label = QLabel("Passwort-Stärke: -")
        self.password_strength_label.setObjectName("strengthLabel")

        self.password_rule_length = QLabel("✓ Mindestens 8 Zeichen")
        self.password_rule_length.setObjectName("ruleLabel")

        self.password_rule_upper = QLabel("✓ Mindestens 1 Großbuchstabe")
        self.password_rule_upper.setObjectName("ruleLabel")

        self.password_rule_number = QLabel("✓ Mindestens 1 Zahl")
        self.password_rule_number.setObjectName("ruleLabel")

        self.password_rule_special = QLabel("✓ Mindestens 1 Sonderzeichen")
        self.password_rule_special.setObjectName("ruleLabel")

        self.register_button = QPushButton("Registrieren")
        self.register_button.setObjectName("primaryButton")
        self.register_button.clicked.connect(self.handle_register)

        switch_btn = QPushButton("Schon ein Konto? Zum Login")
        switch_btn.setObjectName("secondaryButton")
        switch_btn.clicked.connect(lambda: self._switch_page(1))

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.reg_msg)
        layout.addWidget(self.reg_user)
        layout.addLayout(pass_layout)
        layout.addWidget(self.reg_pass_confirm)
        layout.addWidget(self.password_strength_label)
        layout.addWidget(self.password_rule_length)
        layout.addWidget(self.password_rule_upper)
        layout.addWidget(self.password_rule_number)
        layout.addWidget(self.password_rule_special)
        layout.addSpacing(6)
        layout.addWidget(self.register_button)
        layout.addWidget(switch_btn)

        return widget

    def _switch_page(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        self._clear_messages()

    def _clear_messages(self) -> None:
        self.login_msg.setText("")
        self.reg_msg.setText("")
        self.session_message_label.setText("")

    def _toggle_login_password(self) -> None:
        if self.login_pass.echoMode() == QLineEdit.EchoMode.Password:
            self.login_pass.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)

    def _toggle_register_passwords(self) -> None:
        if self.reg_pass.echoMode() == QLineEdit.EchoMode.Password:
            self.reg_pass.setEchoMode(QLineEdit.EchoMode.Normal)
            self.reg_pass_confirm.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
            self.reg_pass_confirm.setEchoMode(QLineEdit.EchoMode.Password)

    def _continue_as_remembered_user(self) -> None:
        remembered_user = self.auth.get_logged_in_user()

        if remembered_user:
            self._set_message(self.session_message_label, f"Anmeldung als {remembered_user} ...", "success")
            QTimer.singleShot(600, self._open_main_window)
        else:
            self._set_message(self.session_message_label, "Keine gespeicherte Sitzung gefunden.", "error")
            self._switch_page(1)

    def _switch_user(self) -> None:
        self.auth.clear_session()
        self.login_user.clear()
        self.login_pass.clear()
        self.remember_me_checkbox.setChecked(False)
        self._switch_page(1)
        self.login_user.setFocus()

    @staticmethod
    def evaluate_password_strength_static(password: str) -> tuple[str, dict[str, bool]]:
        rules = {
            "length": len(password) >= 8,
            "upper": any(char.isupper() for char in password),
            "number": any(char.isdigit() for char in password),
            "special": any(not char.isalnum() for char in password),
        }

        score = sum(rules.values())

        if score <= 1:
            strength = "Schwach"
        elif score in (2, 3):
            strength = "Mittel"
        else:
            strength = "Stark"

        return strength, rules

    def update_password_strength(self) -> None:
        password = self.reg_pass.text()
        strength, rules = self.evaluate_password_strength_static(password)

        self.password_strength_label.setText(f"Passwort-Stärke: {strength}")
        self.password_strength_label.setProperty("strength", strength.lower())
        self.password_strength_label.style().unpolish(self.password_strength_label)
        self.password_strength_label.style().polish(self.password_strength_label)

        self._update_rule_label(self.password_rule_length, rules["length"])
        self._update_rule_label(self.password_rule_upper, rules["upper"])
        self._update_rule_label(self.password_rule_number, rules["number"])
        self._update_rule_label(self.password_rule_special, rules["special"])

    def _update_rule_label(self, label: QLabel, fulfilled: bool) -> None:
        label.setProperty("fulfilled", fulfilled)
        label.style().unpolish(label)
        label.style().polish(label)

    def open_forgot_password_dialog(self) -> None:
        dialog = ForgotPasswordDialog(self.auth, self)
        dialog.exec()

    def handle_login(self) -> None:
        user = self.login_user.text().strip()
        pw = self.login_pass.text().strip()

        if not user or not pw:
            self._set_message(self.login_msg, "Bitte Benutzername und Passwort eingeben.", "error")
            return

        self.login_button.setEnabled(False)
        self.login_button.setText("Anmeldung läuft ...")
        self._set_message(self.login_msg, "Zugangsdaten werden geprüft ...", "success")

        QTimer.singleShot(900, lambda: self._finish_login(user, pw))

    def _finish_login(self, user: str, pw: str) -> None:
        if self.auth.login(user, pw):
            self._set_message(self.login_msg, "Erfolgreich eingeloggt.", "success")

            if self.remember_me_checkbox.isChecked():
                self.auth.save_session(user)
            else:
                self.auth.clear_session()

            QTimer.singleShot(350, self._open_main_window)
        else:
            self.auth.clear_session()
            self._set_message(self.login_msg, "Benutzername oder Passwort ist falsch.", "error")
            self.login_button.setEnabled(True)
            self.login_button.setText("Anmelden")

    def handle_register(self) -> None:
        username = self.reg_user.text().strip()
        password = self.reg_pass.text().strip()
        confirm_password = self.reg_pass_confirm.text().strip()
        role = "Mitarbeiter"

        if not username or not password or not confirm_password:
            self._set_message(self.reg_msg, "Bitte alle Felder ausfüllen.", "error")
            return

        if len(username) < 3:
            self._set_message(self.reg_msg, "Der Benutzername muss mindestens 3 Zeichen lang sein.", "error")
            return

        if password != confirm_password:
            self._set_message(self.reg_msg, "Die Passwörter stimmen nicht überein.", "error")
            return

        strength, _rules = self.evaluate_password_strength_static(password)
        if strength == "Schwach":
            self._set_message(self.reg_msg, "Das Passwort ist zu schwach.", "error")
            return

        success, message = self.auth.register(
            username=username,
            password=password,
            first_name=username,
            last_name="",
            role=role,
            employee_id=username,
        )

        if success:
            self._set_message(self.reg_msg, message, "success")
            self.reg_user.clear()
            self.reg_pass.clear()
            self.reg_pass_confirm.clear()
            self.password_strength_label.setText("Passwort-Stärke: -")
            self.login_user.setText(username)

            QTimer.singleShot(800, lambda: self._switch_page(1))
        else:
            self._set_message(self.reg_msg, message, "error")

    def _open_main_window(self) -> None:
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def _set_message(self, label: QLabel, text: str, msg_type: str) -> None:
        label.setText(text)
        label.setProperty("state", "success" if msg_type == "success" else "error")
        label.style().unpolish(label)
        label.style().polish(label)