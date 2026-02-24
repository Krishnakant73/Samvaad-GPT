from __future__ import annotations

import sqlite3
import threading
import uuid
from datetime import datetime
from typing import Iterable, List, Tuple

_lock = threading.Lock()
_conn: sqlite3.Connection | None = None


def init_db(path: str = "chat_history.db") -> None:
    global _conn
    with _lock:
        if _conn is None:
            _conn = sqlite3.connect(path, check_same_thread=False)
            _conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at TEXT
                )
                """
            )
            _conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp TEXT
                )
                """
            )
            _conn.commit()


def create_new_chat(title: str = "New Chat") -> str:
    assert _conn is not None, "Database not initialized"
    chat_id = str(uuid.uuid4())
    with _lock:
        _conn.execute(
            "INSERT INTO conversations (id, title, created_at) VALUES (?,?,?)",
            (chat_id, title, datetime.now().isoformat()),
        )
        _conn.commit()
    return chat_id


def update_chat_title(chat_id: str, title: str) -> None:
    assert _conn is not None, "Database not initialized"
    with _lock:
        _conn.execute(
            "UPDATE conversations SET title=? WHERE id=?",
            (title, chat_id),
        )
        _conn.commit()


def save_message(chat_id: str, role: str, content: str) -> None:
    assert _conn is not None, "Database not initialized"
    with _lock:
        _conn.execute(
            "INSERT INTO messages (conversation_id, role, content, timestamp) VALUES (?,?,?,?)",
            (chat_id, role, content, datetime.now().isoformat()),
        )
        _conn.commit()


def get_messages(chat_id: str) -> List[Tuple[str, str]]:
    assert _conn is not None, "Database not initialized"
    with _lock:
        cur = _conn.execute(
            "SELECT role, content FROM messages WHERE conversation_id=? ORDER BY id",
            (chat_id,),
        )
        return list(cur.fetchall())


def get_all_chats() -> List[Tuple[str, str]]:
    assert _conn is not None, "Database not initialized"
    with _lock:
        cur = _conn.execute(
            "SELECT id, title FROM conversations ORDER BY created_at DESC"
        )
        return list(cur.fetchall())


def delete_chat(chat_id: str) -> None:
    assert _conn is not None, "Database not initialized"
    with _lock:
        _conn.execute("DELETE FROM messages WHERE conversation_id=?", (chat_id,))
        _conn.execute("DELETE FROM conversations WHERE id=?", (chat_id,))
        _conn.commit()

