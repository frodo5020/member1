from flask import Flask, request, jsonify, url_for, make_response
from flask_mysqldb import MySQL
from flask_cors import CORS  
from pymysql.err import IntegrityError  # ID 중복 처리용

app = Flask(__name__)
CORS(app)                 

# MySQL config
app.config['MYSQL_HOST'] = 'db.frodo.local'
app.config['MYSQL_USER'] = 'frodo'
app.config['MYSQL_PASSWORD'] = 'Frodo5020!!'
app.config['MYSQL_DB'] = 'frodo'

mysql = MySQL(app)

@app.route('/api/members', methods=['GET'])
def get_members():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM members WHERE 1=1"
    filters = []

    id = request.args.get('id')
    name = request.args.get('name')
    gender = request.args.get('gender')
    age = request.args.get('age')

    if id:
        query += " AND id = %s"
        filters.append(id)
    if name:
        query += " AND name LIKE %s"
        filters.append(f"%{name}%")
    if gender:
        query += " AND gender = %s"
        filters.append(gender)
    if age:
        query += " AND age = %s"
        filters.append(age)

    cur.execute(query, filters)
    rows = cur.fetchall()
    cur.close()

    members = [
        {"id": row[0], "name": row[1], "gender": row[2], "age": row[3]}
        for row in rows
    ]
    return jsonify(members)

@app.route('/api/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM members WHERE id = %s", (member_id,))
    row = cur.fetchone()
    cur.close()
    if row:
        return jsonify({"id": row[0], "name": row[1], "gender": row[2], "age": row[3]})
    return jsonify({"error": "Member not found"}), 404

@app.route('/api/members', methods=['POST'])
def create_member():
    data = request.get_json()
    id = data.get('id')
    name = data.get('name')
    gender = data.get('gender')
    age = data.get('age')

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO members (id, name, gender, age) VALUES (%s, %s, %s, %s)", (id, name, gender, age))
        mysql.connection.commit()
        cur.close()
    except IntegrityError as e:
        if "Duplicate entry" in str(e):
            return jsonify({"error": f"Member with ID {id} already exists"}), 409
        return jsonify({"error": "Database error"}), 500

    response = make_response(jsonify({"message": "Member created"}), 201)
    response.headers["Location"] = url_for('get_member', member_id=id, _external=True)
    return response

@app.route('/api/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.get_json()
    name = data.get('name')
    gender = data.get('gender')
    age = data.get('age')

    cur = mysql.connection.cursor()
    cur.execute("UPDATE members SET name=%s, gender=%s, age=%s WHERE id=%s", (name, gender, age, member_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Member updated"})

@app.route('/api/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM members WHERE id=%s", (member_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Member deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
