# backend/app/database.py

import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from dotenv import load_dotenv
from sqlmodel import create_engine

load_dotenv()


def _ensure_pg_sslmode_require(db_url: str) -> str:
    """
    Neon / managed Postgres often requires SSL.
    If sslmode is missing, enforce sslmode=require to avoid random SSL drops.
    """
    if not db_url:
        return db_url

    if not (db_url.startswith("postgresql://") or db_url.startswith("postgres://")):
        return db_url

    parsed = urlparse(db_url)
    q = parse_qs(parsed.query)

    # if sslmode already exists, keep it
    if "sslmode" not in q:
        q["sslmode"] = ["require"]

    new_query = urlencode(q, doseq=True)
    return urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment)
    )


DATABASE_URL = _ensure_pg_sslmode_require(os.getenv("DATABASE_URL", ""))

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing. Set it in .env or deployment env vars.")

# ✅ pool_pre_ping avoids stale connections ("SSL connection closed unexpectedly")
# ✅ pool_recycle prevents long-idle SSL connections
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=1800,
)
