import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    name = data["name"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT NOT NULL)"
    )
    cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id", (name,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_id, "name": name}), 201


@app.route("/items", methods=["GET"])
def list_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT NOT NULL)"
    )
    cur.execute("SELECT id, name FROM items ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{"id": r[0], "name": r[1]} for r in rows])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

