from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


class AuthService:
    """Verwaltet Benutzer, Login und Session über JSON-Dateien."""

    def __init__(self, path: str | None = None, session_path: str | None = None) -> None:
        """Initialisiert Pfade für Benutzer- und Sessiondaten."""
        base_dir = Path(__file__).resolve().parent

        self.path = Path(path).resolve() if path else base_dir / "users.json"
        self.session_path = (
            Path(session_path).resolve() if session_path else base_dir / "session.json"
        )

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.session_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

        if not self.session_path.exists():
            self.session_path.write_text("{}", encoding="utf-8")

    def _load_users(self) -> list[dict[str, Any]]:
        """Lädt alle Benutzer aus der JSON-Datei."""
        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return []

    def _save_users(self, users: list[dict[str, Any]]) -> None:
        """Speichert alle Benutzer in der JSON-Datei."""
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(users, file, indent=4, ensure_ascii=False)

    def _load_session(self) -> dict[str, Any]:
        """Lädt die aktuelle Session."""
        try:
            with self.session_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, dict) else {}
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {}

    def _save_session(self, session_data: dict[str, Any]) -> None:
        """Speichert die aktuelle Session."""
        with self.session_path.open("w", encoding="utf-8") as file:
            json.dump(session_data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def _normalize_text(value: str) -> str:
        """Bereinigt einen Textwert."""
        return value.strip()

    @staticmethod
    def _normalize_key(value: str) -> str:
        """Bereinigt einen Vergleichswert und wandelt ihn in Kleinbuchstaben um."""
        return value.strip().lower()

    @staticmethod
    def _current_timestamp() -> str:
        """Liefert den aktuellen Zeitstempel."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_session(self, username: str) -> None:
        """Speichert den aktuell angemeldeten Benutzer."""
        self._save_session({"username": self._normalize_text(username)})

    def clear_session(self) -> None:
        """Löscht die gespeicherte Session."""
        self._save_session({})

    def get_logged_in_user(self) -> str | None:
        """Gibt den aktuell angemeldeten Benutzer zurück."""
        session = self._load_session()
        username = session.get("username")

        if not username:
            return None

        user = self.get_user_by_username(username)
        return user["username"] if user else None

    def _hash_password(self, password: str) -> str:
        """Erzeugt einen SHA-256-Hash für ein Passwort."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def get_user_by_username(self, username: str) -> dict[str, Any] | None:
        """Sucht einen Benutzer über den Benutzernamen."""
        normalized_username = self._normalize_key(username)

        for user in self._load_users():
            if self._normalize_key(user.get("username", "")) == normalized_username:
                return user

        return None

    def username_exists(self, username: str) -> bool:
        """Prüft, ob ein Benutzername bereits existiert."""
        return self.get_user_by_username(username) is not None

    def employee_id_exists(self, employee_id: str) -> bool:
        """Prüft, ob eine Mitarbeiter-ID bereits existiert."""
        normalized_employee_id = self._normalize_key(employee_id)

        for user in self._load_users():
            if self._normalize_key(user.get("employee_id", "")) == normalized_employee_id:
                return True

        return False

    def register(
        self,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        role: str,
        employee_id: str,
    ) -> tuple[bool, str]:
        """Registriert einen neuen Benutzer."""
        users = self._load_users()

        username = self._normalize_text(username)
        password = self._normalize_text(password)
        first_name = self._normalize_text(first_name)
        last_name = self._normalize_text(last_name)
        role = self._normalize_text(role)
        employee_id = self._normalize_text(employee_id)

        if not username or not password or not first_name or not role or not employee_id:
            return False, "Bitte alle Pflichtfelder ausfüllen."

        if self.username_exists(username):
            return False, "Dieser Benutzername existiert bereits."

        if self.employee_id_exists(employee_id):
            return False, "Diese Mitarbeiter-ID existiert bereits."

        users.append(
            {
                "username": username,
                "password": self._hash_password(password),
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "employee_id": employee_id,
                "created_at": self._current_timestamp(),
                "last_login": None,
                "is_active": True,
            }
        )

        self._save_users(users)
        return True, "Konto erfolgreich erstellt."

    def login(self, username: str, password: str) -> bool:
        """Prüft die Login-Daten eines Benutzers."""
        users = self._load_users()

        normalized_username = self._normalize_key(username)
        hashed_password = self._hash_password(password)

        for user in users:
            if (
                self._normalize_key(user.get("username", "")) == normalized_username
                and user.get("password") == hashed_password
                and user.get("is_active", True)
            ):
                user["last_login"] = self._current_timestamp()
                self._save_users(users)
                return True

        return False

    def reset_password(
        self,
        username: str,
        employee_id: str,
        new_password: str,
    ) -> tuple[bool, str]:
        """Setzt das Passwort eines Benutzers zurück."""
        users = self._load_users()

        normalized_username = self._normalize_key(username)
        normalized_employee_id = self._normalize_key(employee_id)
        new_password = self._normalize_text(new_password)

        if not new_password:
            return False, "Bitte ein neues Passwort eingeben."

        for user in users:
            if (
                self._normalize_key(user.get("username", "")) == normalized_username
                and self._normalize_key(user.get("employee_id", "")) == normalized_employee_id
            ):
                user["password"] = self._hash_password(new_password)
                self._save_users(users)
                return True, "Passwort wurde erfolgreich zurückgesetzt."

        return False, "Benutzername und Mitarbeiter-ID passen nicht zusammen."