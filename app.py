# -*- coding: utf-8 -*-
import os
from flask import Flask, abort
from flask import render_template, send_from_directory
from flask import redirect, url_for
from flask import request, make_response
import subprocess
import urllib
import requests, split, json
import sqlite3 as sql
from flask import jsonify
import math


app = Flask(__name__)

#app.config.from_object('app.default_settings')
app.config.from_pyfile('local_settings.cfg')
BASE_DIR = app.config['PATH']
# Configure database
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
))

def request_db(fd, params=()):
    con = sql.connect(app.config['DATABASE'])
    con.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
    #sql.Row
    cur = con.cursor()
    with open(fd) as fd:
        try:
            cur.execute(fd.read(), params)
            return cur.fetchall()
        except Exception as e:
            con.rollback()
            raise
    con.close()

def write_db(fd, params=None):
    con = sql.connect(app.config['DATABASE'])
    con.row_factory = sql.Row
    cur = con.cursor()
    with open(fd) as fd:
        try:
            cur.execute(fd.read(), params)
            con.commit()
        except Exception as e:
            con.rollback()
            raise
    con.close()

# Custom static data
@app.route('/statics/<path:filename>')
def custom_sound(filename):
    return send_from_directory(BASE_DIR, filename)

def dir_listing(req_path):
    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return [] if path doesn't exist
    if not os.path.exists(abs_path):
        return []

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return files


@app.route('/week/<weekid>')
def week(weekid=1):
    words = request_db('sql/listWords.sql', (weekid,))
    currentWeek = request_db('sql/getWeek.sql', (weekid,))[0]
    return render_template('week.html', words = words, week=currentWeek)

@app.route('/test/<weekId>')
def test(weekId=1):
    words = request_db('sql/getNewWords.sql', (weekId,))
    currentWeek = request_db('sql/getWeek.sql', (weekId,))[0]
    return render_template('test.html', words = words, week=currentWeek)



@app.route('/createWord/<weekid>', methods=['POST'])
def createwordPost(weekid):
    name = request.form.get('name')
    write_db('sql/createWord.sql', (name, weekid))
    wordid = request_db('sql/getLastWord.sql')[0]['id']
    subprocess.call(["pwd", str(wordid),  name])
    subprocess.call(["./tts.sh", str(wordid),  name])
    return json.dumps({'success':True, 'weekid':weekid}), 200, {'ContentType':'application/json'}

@app.route('/deleteWord/<weekid>', methods=['POST'])
def deletewordPost(weekid):
    wordid = request.form.get('toDelete')
    write_db('sql/deleteWord.sql', (wordid))
    return json.dumps({'success':True, 'weekid':weekid}), 200, {'ContentType':'application/json'}

@app.route('/validateWord/<wordid>', methods=['POST'])
def validateWordPost(wordid):
    word = request_db('sql/getWord.sql', (wordid,))[0]
    if word['success']==1:
        write_db('sql/updateWord.sql', (1, 1, wordid))
    else:
        write_db('sql/updateWord.sql', (1, 0, wordid))
    return json.dumps({'success':True, 'wordid':wordid}), 200, {'ContentType':'application/json'}

@app.route('/reloadWord/<wordid>', methods=['POST'])
def reloadWordPost(wordid):
    word = request_db('sql/getWord.sql', (wordid,))[0]
    subprocess.call(["./tts.sh", str(wordid),  word['name']])
    return json.dumps({'success':True, 'wordid':wordid}), 200, {'ContentType':'application/json'}

@app.route('/unvalidateWord/<wordid>', methods=['POST'])
def unvalidateWordPost(wordid):
    write_db('sql/updateWord.sql', (0, 0, wordid))
    return json.dumps({'success':True, 'wordid':wordid}), 200, {'ContentType':'application/json'}


@app.route('/')
def index():
    weeks = request_db('sql/listWeeks.sql')
    return render_template('index.html', weeks = weeks)


@app.route('/createWeek')
def createWeek():
    return render_template('createWeek.html')


@app.route('/createWeek', methods=['POST'])
def createWeekPost():
    name = request.form.get('name')
    write_db('sql/createWeek.sql', (name,))
    map = request_db('sql/getLastWeek.sql')
    return json.dumps({'success':True, 'weekid':map[0]['id']}), 200, {'ContentType':'application/json'}


if __name__ == "__main__":
    app.run(host="localhost", port=5003)
#    app.run(host="10.0.160.54")
