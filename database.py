import os
import logging
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Any
from contextlib import contextmanager

from dotenv import load_dotenv
import psycopg2
import psycopg2.extras

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database config
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', 5432)),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password'),
    'database': os.getenv('POSTGRES_DB', 'postgres')
}

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        conn.autocommit = False
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

@contextmanager
def get_db_cursor():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        yield cursor, conn
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

def serialize_datetime(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj

def serialize_row(row):
    return {k: serialize_datetime(v) for k, v in row.items()} if row else None

def serialize_rows(rows):
    return [serialize_row(row) for row in rows] if rows else []

def execute_query(conn, query: str, params: Tuple = None) -> List[Dict]:
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, params)
        return serialize_rows(cursor.fetchall())
    except Exception as e:
        logger.error(f"Query failed: {e}\nQuery: {query}\nParams: {params}")
        raise

def execute_query_one(conn, query: str, params: Tuple = None) -> Optional[Dict]:
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, params)
        return serialize_row(cursor.fetchone())
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise

def execute_insert(conn, query: str, params: Tuple = None) -> Optional[int]:
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if 'RETURNING' in query.upper():
            return cursor.fetchone()[0]
        return cursor.rowcount
    except Exception as e:
        logger.error(f"Insert failed: {e}")
        raise

def execute_update(conn, query: str, params: Tuple = None) -> int:
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.rowcount
    except Exception as e:
        logger.error(f"Update failed: {e}")
        raise

def execute_delete(conn, query: str, params: Tuple = None) -> int:
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.rowcount
    except Exception as e:
        logger.error(f"Delete failed: {e}")
        raise

def test_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        logger.info("Database connection successful ✅")
        return True
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False

def init_database():
    logger.info("Initializing DB connection...")
    logger.info(f"Using host={DB_CONFIG['host']}, db={DB_CONFIG['database']}")
    if test_connection():
        logger.info("Database initialized ✅")
        return True
    else:
        logger.error("Database failed ❌")
        return False

if __name__ == "__main__":
    init_database()
