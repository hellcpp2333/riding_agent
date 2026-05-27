import os
import sqlite3

DB_PATH = "checkpoints.db"


def list_sessions(db_path: str = DB_PATH) -> list[dict]:
    if not os.path.exists(db_path):
        return []
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT thread_id, COUNT(*) AS turns FROM checkpoints "
        "WHERE checkpoint_ns = '' "
        "GROUP BY thread_id ORDER BY thread_id"
    ).fetchall()
    conn.close()
    return [{"thread_id": r[0], "turns": r[1]} for r in rows]
