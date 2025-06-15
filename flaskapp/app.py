from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

db_config = {
    "host": "db.frodo.local",
    "user": "frodo",
    "password": "Frodo5020!!",
    "database": "frodo",
    "cursorclass": pymysql.cursors.DictCursor
}

@app.route("/api/members", methods=["GET"])
def get_members():
    filters = []
    params = []
    for field in ["id", "name", "gender", "age"]:
        value = request.args.get(field)
        if value:
            filters.append(f"{field} = %s")
            params.append(value)

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""
    sql = f"SELECT * FROM members {where_clause}"

    with pymysql.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
    return jsonify(rows)

@app.route("/api/members", methods=["POST"])
def create_member():
    data = request.get_json()
    sql = "INSERT INTO members (id, name, gender, age) VALUES (%s, %s, %s, %s)"
    with pymysql.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (data["id"], data["name"], data["gender"], data["age"]))
            conn.commit()
    return jsonify({"message": "created"}), 201

@app.route("/api/members/<int:member_id>", methods=["PUT"])
def update_member(member_id):
    data = request.get_json()
    sql = "UPDATE members SET name=%s, gender=%s, age=%s WHERE id=%s"
    with pymysql.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (data["name"], data["gender"], data["age"], member_id))
            conn.commit()
    return jsonify({"message": "updated"})

@app.route("/api/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    sql = "DELETE FROM members WHERE id=%s"
    with pymysql.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (member_id,))
            conn.commit()
    return jsonify({"message": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
