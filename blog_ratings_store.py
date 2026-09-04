"""Persistencia de votos de papers (SQLite local + GitHub data/blog-ratings.json)."""

from __future__ import annotations

import base64
import json
import os
import sqlite3
import urllib.error
import urllib.request
from typing import Any

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, "certificados.db")
LOCAL_JSON = os.path.join(ROOT_DIR, "data", "blog-ratings.json")
GITHUB_REPO = os.getenv("GITHUB_RATINGS_REPO", "IOR14/METABOLICFITNESS")
GITHUB_PATH = os.getenv("GITHUB_RATINGS_PATH", "data/blog-ratings.json")
GITHUB_BRANCH = os.getenv("GITHUB_RATINGS_BRANCH", "main")


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_ratings_db() -> None:
    conn = _conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS blog_paper_votes (
            slug TEXT NOT NULL,
            voter_id TEXT NOT NULL,
            score INTEGER NOT NULL CHECK(score BETWEEN 1 AND 5),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            PRIMARY KEY (slug, voter_id)
        )
        """
    )
    conn.commit()
    conn.close()


def _github_token() -> str:
    token = (os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN") or "").strip()
    if token:
        return token
    # Intento local con GitHub CLI
    try:
        import subprocess

        out = subprocess.check_output(["gh", "auth", "token"], text=True, timeout=8)
        return (out or "").strip()
    except Exception:
        return ""


def _http_json(method: str, url: str, headers: dict[str, str], body: dict | None = None) -> dict[str, Any]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {exc.code}: {detail[:300]}") from exc


def _load_json_file(path: str) -> dict[str, Any]:
    if not os.path.isfile(path):
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _save_json_file(path: str, payload: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _load_github_ratings() -> tuple[dict[str, Any], str | None]:
    token = _github_token()
    if not token:
        return _load_json_file(LOCAL_JSON), None
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_PATH}?ref={GITHUB_BRANCH}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "MetabolicFitnessRatings/1.0",
    }
    try:
        meta = _http_json("GET", url, headers)
        content = base64.b64decode(meta.get("content") or "").decode("utf-8")
        data = json.loads(content) if content.strip() else {}
        return data, meta.get("sha")
    except Exception:
        return _load_json_file(LOCAL_JSON), None


def _save_github_ratings(payload: dict[str, Any], sha: str | None) -> None:
    token = _github_token()
    _save_json_file(LOCAL_JSON, payload)
    if not token:
        return
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_PATH}"
    body = {
        "message": "chore: update blog paper ratings",
        "content": base64.b64encode(
            (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        ).decode("ascii"),
        "branch": GITHUB_BRANCH,
    }
    if sha:
        body["sha"] = sha
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "MetabolicFitnessRatings/1.0",
    }
    _http_json("PUT", url, headers, body)


def _recompute(entry: dict[str, Any]) -> dict[str, Any]:
    votes = entry.get("votes") or {}
    scores = [int(v) for v in votes.values() if isinstance(v, (int, float)) and 1 <= int(v) <= 5]
    entry["votes"] = {str(k): int(v) for k, v in votes.items() if 1 <= int(v) <= 5}
    entry["sum"] = int(sum(scores))
    entry["count"] = len(scores)
    return entry


def get_slug_stats(slug: str) -> dict[str, Any]:
    init_ratings_db()
    data, _sha = _load_github_ratings()
    entry = data.get(slug) or {"sum": 0, "count": 0, "votes": {}, "editorial": 0}
    entry = _recompute(entry)
    return {
        "slug": slug,
        "sum": entry.get("sum", 0),
        "count": entry.get("count", 0),
        "editorial": entry.get("editorial", 0),
        "average": round(entry["sum"] / entry["count"], 2) if entry.get("count") else None,
    }


def upsert_vote(slug: str, voter_id: str, score: int, editorial: float | None = None) -> dict[str, Any]:
    if not slug or not voter_id:
        raise ValueError("slug y voter_id son obligatorios")
    score = int(score)
    if score < 1 or score > 5:
        raise ValueError("score debe estar entre 1 y 5")

    init_ratings_db()
    conn = _conn()
    conn.execute(
        """
        INSERT INTO blog_paper_votes (slug, voter_id, score, updated_at)
        VALUES (?, ?, ?, datetime('now'))
        ON CONFLICT(slug, voter_id) DO UPDATE SET
            score = excluded.score,
            updated_at = datetime('now')
        """,
        (slug, voter_id, score),
    )
    conn.commit()
    conn.close()

    data, sha = _load_github_ratings()
    entry = data.get(slug) or {"sum": 0, "count": 0, "votes": {}, "editorial": 0}
    if not isinstance(entry.get("votes"), dict):
        entry["votes"] = {}
    entry["votes"][voter_id] = score
    if editorial is not None:
        entry["editorial"] = float(editorial)
    entry = _recompute(entry)
    data[slug] = entry
    _save_github_ratings(data, sha)

    return {
        "slug": slug,
        "sum": entry["sum"],
        "count": entry["count"],
        "editorial": entry.get("editorial", 0),
        "average": round(entry["sum"] / entry["count"], 2) if entry["count"] else None,
        "saved": True,
    }
