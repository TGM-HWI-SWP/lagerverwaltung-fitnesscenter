from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


class AuthService:
    """Verwaltet Benutzer, Login und Session über JSON-Dateien."""

    def __init__(self, path: str | None = None, session_path: str | None = None) -> None:
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

    # -------------------------------------------------
    # FILE HELPERS
    # -------------------------------------------------
    def _load_users(self) -> list[dict[str, Any]]:
        try:
            with self.path.open("r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_users(self, users: list[dict[str, Any]]) -> None:
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(users, file, indent=4, ensure_ascii=False)

    def _load_session(self) -> dict[str, Any]:
        try:
            with self.session_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, dict) else {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_session(self, session_data: dict[str, Any]) -> None:
        with self.session_path.open("w", encoding="utf-8") as file:
            json.dump(session_data, file, indent=4, ensure_ascii=False)

    # -------------------------------------------------
    # SESSION
    # -------------------------------------------------
    def save_session(self, username: str) -> None:
        self._save_session({"username": username.strip()})

    def clear_session(self) -> None:
        self._save_session({})

    def get_logged_in_user(self) -> str | None:
        session = self._load_session()
        username = session.get("username")

        if not username:
            return None

        user = self.get_user_by_username(username)
        return user["username"] if user else None

    # -------------------------------------------------
    # SECURITY
    # -------------------------------------------------
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    # -------------------------------------------------
    # LOOKUPS
    # -------------------------------------------------
    def get_user_by_username(self, username: str) -> dict[str, Any] | None:
        username = username.strip().lower()

        for user in self._load_users():
            if user.get("username", "").strip().lower() == username:
                return user

        return None

    def username_exists(self, username: str) -> bool:
        return self.get_user_by_username(username) is not None

    def employee_id_exists(self, employee_id: str) -> bool:
        employee_id = employee_id.strip().lower()

        for user in self._load_users():
            if user.get("employee_id", "").strip().lower() == employee_id:
                return True

        return False

    # -------------------------------------------------
    # REGISTER
    # -------------------------------------------------
    def register(
        self,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        role: str,
        employee_id: str,
    ) -> tuple[bool, str]:
        users = self._load_users()

        username = username.strip()
        password = password.strip()
        first_name = first_name.strip()
        last_name = last_name.strip()
        role = role.strip()
        employee_id = employee_id.strip()

        if not username or not password or not first_name or not role or not employee_id:
            return False, "Bitte alle Pflichtfelder ausfüllen."

        if self.username_exists(username):
            return False, "Dieser Benutzername existiert bereits."

        if self.employee_id_exists(employee_id):
            return False, "Diese Mitarbeiter-ID existiert bereits."

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        users.append(
            {
                "username": username,
                "password": self._hash_password(password),
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "employee_id": employee_id,
                "created_at": now,
                "last_login": None,
                "is_active": True,
            }
        )

        self._save_users(users)
        return True, "Konto erfolgreich erstellt."

    # -------------------------------------------------
    # LOGIN
    # -------------------------------------------------
    def login(self, username: str, password: str) -> bool:
        users = self._load_users()

        username = username.strip().lower()
        hashed_password = self._hash_password(password)

        for user in users:
            if (
                user.get("username", "").strip().lower() == username
                and user.get("password") == hashed_password
                and user.get("is_active", True)
            ):
                user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_users(users)
                return True

        return False

    # -------------------------------------------------
    # RESET PASSWORD
    # -------------------------------------------------
    def reset_password(
        self,
        username: str,
        employee_id: str,
        new_password: str,
    ) -> tuple[bool, str]:
        users = self._load_users()

        username = username.strip().lower()
        employee_id = employee_id.strip().lower()

        for user in users:
            if (
                user.get("username", "").strip().lower() == username
                and user.get("employee_id", "").strip().lower() == employee_id
            ):
                user["password"] = self._hash_password(new_password)
                self._save_users(users)
                return True, "Passwort wurde erfolgreich zurückgesetzt."

        return False, "Benutzername und Mitarbeiter-ID passen nicht zusammen."