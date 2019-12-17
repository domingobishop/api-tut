from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/")
def home():
    return "Hello World!"


# endpoint to show all organisations
@app.route("/organisations/all", methods=["GET"])
def api_get_orgs():
    conn = sqlite3.connect('organisations.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute('SELECT * FROM ORGANISATIONS;').fetchall()
    return jsonify(results)


# endpoint to show all users
@app.route("/users/all", methods=["GET"])
def api_get_users():
    conn = sqlite3.connect('organisations.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute('SELECT * FROM USERS;').fetchall()
    return jsonify(results)


# endpoint to filter organisations
@app.route('/organisations', methods=['GET'])
def api_filter_organisations():
    query_parameters = request.args

    id = query_parameters.get('id')
    name = query_parameters.get('name')

    query = "SELECT * FROM ORGANISATIONS WHERE"
    to_filter = []

    if id:
        query += ' org_id=? AND'
        to_filter.append(id)
    if name:
        query += ' org_name=? AND'
        to_filter.append(name)
    if not (id or name):
        return '404'

    query = query[:-4] + ';'

    conn = sqlite3.connect('organisations.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


# endpoint to create new organisation
@app.route("/organisations/add", methods=["GET"])
def add_organisation():
    query_parameters = request.args

    id = query_parameters.get('id')
    name = query_parameters.get('name')
    date = query_parameters.get('date')
    data = [id,name,date]

    sql = ''' INSERT INTO ORGANISATIONS(org_id,org_name,date)
                  VALUES(?,?,?) '''

    conn = sqlite3.connect('organisations.db')
    cur = conn.cursor()
    try:
        cur.execute(sql, data)
        results = 200
    except sqlite3.IntegrityError as e:
        results = 'sqlite error: ' + e.args[0]
    conn.commit()
    return results


if __name__ == '__main__':
    app.run(debug=True)
