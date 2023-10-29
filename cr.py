import asyncio
import websockets
import psycopg2
import os


conn = psycopg2.connect(os.environ['DATABASE_URL']  )
print(conn)
with conn.cursor() as cur:
    cur.execute('INSERT INTO accounts (id, balance) VALUES (1, 1000), (2, 250)')