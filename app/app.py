from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'snakesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Anik'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM snakes_count_100 order by Game_Number ASC')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, games=result)


@app.route('/view/<int:GameNumber>', methods=['GET'])
def record_view(GameNumber):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM snakes_count_100 WHERE Game_Number=%s', GameNumber)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', game=result[0])


@app.route('/edit/<int:GameNumber>', methods=['GET'])
def form_edit_get(GameNumber):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM snakes_count_100 WHERE Game_Number=%s', GameNumber)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', game=result[0])


@app.route('/edit/<int:GameNumber>', methods=['POST'])
def form_update_post(GameNumber):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Game_Length'), GameNumber)
    sql_update_query = """ UPDATE snakes_count_100 t SET t.Game_Length = %s WHERE t.Game_Number = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/game/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Game Form')


@app.route('/game/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Game_Number'), request.form.get('Game_Length'))
    sql_insert_query = """INSERT INTO snakes_count_100 (Game_Number, Game_Length) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:GameNumber>', methods=['POST'])
def form_delete_post(GameNumber):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM snakes_count_100 WHERE Game_Number = %s """
    cursor.execute(sql_delete_query, GameNumber)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/games', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM snakes_count_100')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/games/<int:GameNumber>', methods=['GET'])
def api_retrieve(Game_Number) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM snakes_count_100 WHERE Game_Number=%s', GameNumber)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/games/', methods=['POST'])
def api_add() -> int:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/games/<int:GameNumber>', methods=['PUT'])
def api_edit(GameNumber) -> int:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/games/<int:GameNumber>', methods=['DELETE'])
def api_delete(GameNumber) -> int:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
