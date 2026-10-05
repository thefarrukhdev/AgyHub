"""
SQLite caching backend for AgyChat sessions.

Uses Python's built-in sqlite3 only — zero external dependencies.
DB location: ~/.gemini/agychat_cache.db
"""

import sqlite3
import os
from pathlib import Path
from typing import List, Dict

from agychat.core.config import BRAIN_DIR

DB_PATH = Path.home() / '.gemini' / 'agychat_cache.db'

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_DDL = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    prompt     TEXT NOT NULL DEFAULT '',
    mtime      REAL NOT NULL DEFAULT 0.0,
    tag        TEXT,
    pinned     INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_sessions_mtime ON sessions(mtime DESC);
"""


def _connect() -> sqlite3.Connection:
    """Return an open connection with WAL mode for better concurrency."""
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


_EXPECTED_COLUMNS = {'session_id', 'prompt', 'mtime', 'tag', 'pinned'}


def init_db() -> None:
    """
    Create the DB file and schema.  If an incompatible schema is detected
    (e.g. left over from an older version), the table is dropped and rebuilt.
    The cache is always reconstructable from disk, so this is safe.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _connect() as conn:
        # Check if existing table has the right columns
        cols = {
            row[1]
            for row in conn.execute("PRAGMA table_info(sessions)").fetchall()
        }
        if cols and not _EXPECTED_COLUMNS.issubset(cols):
            # Stale schema — nuke and rebuild
            conn.execute("DROP TABLE IF EXISTS sessions")
            conn.execute("DROP INDEX IF EXISTS idx_sessions_mtime")
        conn.executescript(_DDL)


# ---------------------------------------------------------------------------
# Sync logic
# ---------------------------------------------------------------------------

def _disk_sessions() -> Dict[str, Dict]:
    """
    Fast scan of BRAIN_DIR.  Returns a dict keyed by session_id with only
    the fields needed for comparison: mtime, pinned, tag.
    Does NOT parse transcript files — that's done lazily below.
    """
    result: Dict[str, Dict] = {}
    if not BRAIN_DIR.exists():
        return result

    for conv_dir in BRAIN_DIR.iterdir():
        if not conv_dir.is_dir():
            continue
        log_file = conv_dir / '.system_generated' / 'logs' / 'transcript.jsonl'
        if not log_file.exists():
            continue

        try:
            mtime = log_file.stat().st_mtime
        except OSError:
            continue

        pinned = (conv_dir / '.agy_pinned').exists()

        tag_file = conv_dir / '.agy_tag'
        tag = None
        try:
            if tag_file.exists():
                tag = tag_file.read_text(encoding='utf-8').strip() or None
        except Exception:
            pass

        result[conv_dir.name] = {
            'session_id': conv_dir.name,
            'mtime': mtime,
            'pinned': int(pinned),
            'tag': tag,
        }

    return result


def sync_cache() -> None:
    """
    Startup sync:
    1. Compare disk sessions to DB.
    2. Upsert new/modified entries (re-parse prompt only when mtime changed).
    3. Prune ghost entries (sessions deleted from disk).
    """
    from agychat.core.session import extract_user_prompt  # local import to avoid circular

    init_db()
    disk = _disk_sessions()

    with _connect() as conn:
        # ── Load existing DB rows ──────────────────────────────────────────
        rows = conn.execute(
            "SELECT session_id, mtime, pinned, tag FROM sessions"
        ).fetchall()
        db_map: Dict[str, sqlite3.Row] = {r['session_id']: r for r in rows}

        # ── Prune ghosts ──────────────────────────────────────────────────
        ghost_ids = [sid for sid in db_map if sid not in disk]
        if ghost_ids:
            conn.executemany(
                "DELETE FROM sessions WHERE session_id = ?",
                [(sid,) for sid in ghost_ids],
            )

        # ── Upsert changed / new ──────────────────────────────────────────
        to_upsert: List[tuple] = []

        for sid, info in disk.items():
            db_row = db_map.get(sid)

            mtime_changed = db_row is None or abs(db_row['mtime'] - info['mtime']) > 0.001
            pin_changed   = db_row is not None and db_row['pinned'] != info['pinned']
            tag_changed   = db_row is not None and db_row['tag'] != info['tag']

            if not (mtime_changed or pin_changed or tag_changed):
                continue  # nothing changed — skip expensive prompt parse

            if mtime_changed:
                log_file = (
                    BRAIN_DIR / sid / '.system_generated' / 'logs' / 'transcript.jsonl'
                )
                prompt = extract_user_prompt(log_file)
            else:
                # keep existing prompt — only pin/tag changed
                prompt = db_row['prompt'] if db_row else ''

            to_upsert.append((
                sid,
                prompt,
                info['mtime'],
                info['tag'],
                info['pinned'],
            ))

        if to_upsert:
            conn.executemany(
                """
                INSERT INTO sessions (session_id, prompt, mtime, tag, pinned)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    prompt = excluded.prompt,
                    mtime  = excluded.mtime,
                    tag    = excluded.tag,
                    pinned = excluded.pinned
                """,
                to_upsert,
            )

        conn.commit()


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def query_sessions(search_query: str = "") -> List[Dict]:
    """
    Return session dicts from the DB, sorted pinned-first then newest-first.
    Each dict has the same keys that session.py previously produced from disk,
    except 'path' and 'relative' which are computed by the caller.
    """
    init_db()
    with _connect() as conn:
        if search_query:
            sq = f"%{search_query.lower()}%"
            rows = conn.execute(
                """
                SELECT session_id, prompt, mtime, tag, pinned
                FROM sessions
                WHERE lower(prompt) LIKE ? OR lower(coalesce(tag,'')) LIKE ?
                ORDER BY pinned DESC, mtime DESC
                """,
                (sq, sq),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT session_id, prompt, mtime, tag, pinned
                FROM sessions
                ORDER BY pinned DESC, mtime DESC
                """,
            ).fetchall()

    return [
        {
            'id':     row['session_id'],
            'prompt': row['prompt'],
            'mtime':  row['mtime'],
            'tag':    row['tag'],
            'pinned': bool(row['pinned']),
        }
        for row in rows
    ]


def invalidate_session(session_id: str) -> None:
    """Remove a single session from the cache (called after deletion)."""
    try:
        with _connect() as conn:
            conn.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
            conn.commit()
    except Exception:
        pass


def update_session_meta(session_id: str, *, tag=None, pinned=None) -> None:
    """
    Lightweight update for tag/pin changes without re-parsing the transcript.
    Pass only the fields you want to change.
    """
    try:
        with _connect() as conn:
            if tag is not None:
                conn.execute(
                    "UPDATE sessions SET tag = ? WHERE session_id = ?",
                    (tag or None, session_id),
                )
            if pinned is not None:
                conn.execute(
                    "UPDATE sessions SET pinned = ? WHERE session_id = ?",
                    (int(pinned), session_id),
                )
            conn.commit()
    except Exception:
        pass
