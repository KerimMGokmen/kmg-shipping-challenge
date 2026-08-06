import os
import socket
import psycopg2
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "kmg-db"),
        dbname=os.getenv("DB_NAME", "kmg_milestone2"),
        user=os.getenv("DB_USER", "kmg_admin"),
        password=os.getenv("DB_PASSWORD", "kmg_pw123"),
        connect_timeout=3,
    )

@app.get("/user")
def get_user():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM users ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return {"name": row[0] if row else "Unknown"}

@app.get("/container-id")
def get_container_id():
    return {"container_id": socket.gethostname()}

@app.get("/health")
def health(response: Response):
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "healthy"}
    except Exception as e:
        print(f"HEALTH CHECK FAILED: {e}", flush=True)
        response.status_code = 500
        return {"status": "unhealthy", "error": str(e)}
