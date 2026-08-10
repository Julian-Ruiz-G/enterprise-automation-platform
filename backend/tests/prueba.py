import psycopg

conn = psycopg.connect(
    dbname="postgres",
    user="postgres",
    password="postgres123",
    host="127.0.0.1",
    port=5432
)

cur = conn.cursor()

cur.execute("SELECT datname FROM pg_database")

print(cur.fetchall())