import json
import sqlite3
import time
from pathlib import Path

from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Andromeda Dashboard")

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
DB_PATH = Path("/var/lib/andromeda/insights.db")

# Make sure folders exist
STATIC_DIR.mkdir(exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Serve /static/*
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ---------- DB SETUP ----------

def init_db() -> None:
    """Create the insights table if it doesn't exist yet."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS insights (
            id TEXT PRIMARY KEY,
            ts INTEGER,
            severity TEXT,
            title TEXT,
            summary TEXT,
            evidence TEXT,
            recommended_actions TEXT,
            source TEXT,
            confidence REAL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


def row_to_insight(row: tuple) -> dict:
    return {
        "id": row[0],
        "ts": row[1],
        "severity": row[2],
        "title": row[3],
        "summary": row[4],
        "evidence": json.loads(row[5] or "{}"),
        "recommended_actions": json.loads(row[6] or "[]"),
        "source": row[7],
        "confidence": row[8],
    }


# ---------- ROUTES ----------

@app.get("/health")
def health():
    return {"ok": True, "service": "andromeda-dashboard"}


@app.get("/")
def root():
    """
    Root of the dashboard.

    If static/index.html exists, serve it (your big HUD).
    Otherwise just return a JSON status.
    """
    index = STATIC_DIR / "index.html"
    if index.exists():
        return FileResponse(index, media_type="text/html")
    return {"ok": True, "service": "andromeda-dashboard", "has_index": False}


@app.get("/insights")
def insights_page():
    """
    Simple HTML page that calls /api/insights and renders JSON.
    """
    html = STATIC_DIR / "insights.html"
    if html.exists():
        return FileResponse(html, media_type="text/html")
    return {"ok": False, "error": "insights.html not found"}


@app.post("/api/insights")
def add_insight(payload: dict = Body(...)):
    """
    Store a single insight in the SQLite DB.
    Called by your Mac helper (andromeda_insight_example).
    """
    now_s = int(time.time())

    payload.setdefault("id", f"ins-{now_s}")
    payload.setdefault("ts", now_s)
    payload.setdefault("severity", "info")
    payload.setdefault("title", "")
    payload.setdefault("summary", "")
    payload.setdefault("evidence", {})
    payload.setdefault("recommended_actions", [])
    payload.setdefault("source", "mac")
    payload.setdefault("confidence", 0.6)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        """
        INSERT OR REPLACE INTO insights
        (id, ts, severity, title, summary,
         evidence, recommended_actions, source, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload["id"],
            int(payload["ts"]),
            payload["severity"],
            payload["title"],
            payload["summary"],
            json.dumps(payload["evidence"]),
            json.dumps(payload["recommended_actions"]),
            payload["source"],
            float(payload["confidence"]),
        ),
    )
    conn.commit()
    conn.close()

    return {"ok": True, "id": payload["id"]}


@app.get("/api/insights")
def list_insights(limit: int = 20):
    """
    Return most recent insights, newest first.
    """
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.execute(
        """
        SELECT id, ts, severity, title, summary,
               evidence, recommended_actions, source, confidence
        FROM insights
        ORDER BY ts DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()

    items = [row_to_insight(r) for r in rows]
    return {"items": items}
