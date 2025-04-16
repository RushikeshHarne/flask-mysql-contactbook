from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'contactbook'

mysql = MySQL(app)

@app.route('/contacts', methods=['GET'])
def get_contacts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    contacts = [{"id": r[0], "name": r[1], "email": r[2], "phone": r[3]} for r in rows]
    return jsonify(contacts)

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE id = %s", (id,))
    row = cur.fetchone()
    if row:
        return jsonify({"id": row[0], "name": row[1], "email": row[2], "phone": row[3]})
    return jsonify({"error": "Not found"}), 404

@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO contacts (name, email, phone) VALUES (%s, %s, %s)",
                (data['name'], data['email'], data['phone']))
    mysql.connection.commit()
    return jsonify({"message": "Contact added"}), 201

@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE contacts SET name=%s, email=%s, phone=%s WHERE id=%s",
                (data['name'], data['email'], data['phone'], id))
    mysql.connection.commit()
    return jsonify({"message": "Contact updated"})

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts WHERE id=%s", (id,))
    mysql.connection.commit()
    return jsonify({"message": "Contact deleted"})

if __name__ == '__main__':
    app.run(debug=True)
