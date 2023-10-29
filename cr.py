import asyncio
import websockets
import psycopg2
import os

conn = psycopg2.connect('postgresql://t:yOQkfZS9LoTsvPL4fozvaA@good-stag-12544.7tt.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full')
with conn.cursor() as cur:
    cur.execute(insert_data_sql, (label, sendload))
    conn.commit()
