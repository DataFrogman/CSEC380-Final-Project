from flask import Flask, flash, jsonify, render_template, request, session, redirect, url_for
import mysql.connector
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime
import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import shutil
import json
import time
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin


time.sleep(25)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def connection():
    conn = mysql.connector.connect(host = "database",
                  user = 'root',
                  password = 'root',
                  database = 'db',
                  auth_plugin='mysql_native_password')

    c = conn.cursor(buffered=True)
    return c , conn

app = Flask(__name__, template_folder='templates')
limiter = Limiter (app,
        key_func=get_remote_address,
        default_limits=["24000 per day", "1000 per hour", "100 per minute"])
secretKey = os.urandom(24)
app.secret_key = secretKey

app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)

testuser1 = 'admin'
testuser1hashedpass = generate_password_hash('admin')
cursor, conn = connection()
cursor.execute("INSERT INTO users(Username, Password, TotalVids, DateCreated) VALUES \
            ('{}', '{}', 0, '{}')".format(testuser1, testuser1hashedpass, datetime.datetime.now().strftime('%Y-%m-%d')))

testuser2 = 'test'
testuser2hashedpass = generate_password_hash('test')
#cursor, conn = connection()
cursor.execute("INSERT INTO users(Username, Password, TotalVids, DateCreated) VALUES \
            ('{}', '{}', 0, '{}')".format(testuser2, testuser2hashedpass, datetime.datetime.now().strftime('%Y-%m-%d')))

cursor.close()
conn.commit()
conn.close()


@app.route("/")
def home():
    return render_template('login.html')

@app.route("/homepage", methods=['GET','POST'])
def mainpage():
    cursor, conn = connection()
    if 'username' in session:
        videos=[]
        videos = getvideos(cursor, conn)
        # videos.append(getothervideos())
        if request.method == "POST":
            target = "static"
            link = request.form.get('linkupload', None)
            if link != "" and link is not None:
                localfile = link.split('/')[-1]
                print(localfile + link, file=sys.stderr)
                destination = "/".join([target, localfile])
                r = requests.get(link, stream=True)
                with open(destination, 'wb') as f:
                    if not localfile.endswith(".mp4"):
                        flash("Only MP4 files are supported, sorry!")
                        return render_template('homepage.html', username = session['username'], videos = videos)
                    destination = "/".join([target, localfile])
                    print("Storing in database . . . " + destination, file=sys.stderr)
                    shutil.copyfileobj(r.raw, f)
                    cursor.execute("SELECT UserID FROM users WHERE Username='{}'".format((session['username'])))
                    userid = cursor.fetchone()
                    print(userid, file=sys.stderr)
                    cursor.execute("INSERT INTO videos(UserID, VideoTitle, VideoURL, VideoUser, DateUploaded) VALUES \
                        ('{}', '{}', '{}', '{}', '{}')".format(userid[0], localfile, \
                        str(destination), session['username'], datetime.datetime.now().strftime('%Y-%m-%d')))
                    cursor.execute("UPDATE users SET TotalVids = TotalVids + \
                        1 WHERE Username = '{}'".format(str(session['username'])))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return render_template('homepage.html', username = session['username'], videos = videos)
            else:
                for f in request.files.getlist("file"):
                    filename = f.filename
                    if not filename.endswith(".mp4"):
                        flash("Please upload a file with .mp4 extension.")
                        return render_template('homepage.html', username = session['username'], videos = videos)
                    destination = "/".join([target, filename])
                    print("Storing in database . . . " + destination, file=sys.stderr)
                    f.save(destination)
                    cursor.execute("SELECT UserID FROM users WHERE Username='{}'".format((session['username'])))
                    userid = cursor.fetchone()
                    print(session['username'])
                    cursor.execute("INSERT INTO videos(UserID, VideoTitle, VideoURL, VideoUser, DateUploaded) VALUES \
                        ('{}', '{}', '{}', '{}', '{}')".format(userid[0], filename, \
                        str(destination), session['username'], datetime.datetime.now().strftime('%Y-%m-%d')))
                    cursor.execute("UPDATE users SET TotalVids = TotalVids + \
                        1 WHERE Username = '{}'".format(str(session['username'])))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    return render_template('homepage.html', username = session['username'], videos = videos)
        cursor.close()
        conn.close()
        return render_template('homepage.html', username = session['username'], videos = videos)
        #return render_template('homepage.html')
    else:
        cursor.close()
        conn.close()
    return redirect(url_for('login'))

@app.route("/video", methods=['POST'])
def video():
    cursor, conn = connection()
    if 'username' in session:
        url = request.form["videoURL"]
        
        return render_template("video_viewer.html", videoURL=url)
    else:
        return redirect(url_for("login"))

def getvideos(cursor, conn):
    json_data=[]
    cursor.execute("SELECT * FROM videos")
    rows = cursor.fetchall()
    row_headers=[x[0] for x in cursor.description]
    for result in rows:
        json_data.append(dict(zip(row_headers,result)))
    print(json_data, file=sys.stderr)
    return json_data

def getothervideos():
    cursor, conn = connection()
    if 'username' in session:

        username = request.get_json(force=True)
        username = username['username']
        cursor.execute("SELECT UserID FROM users WHERE Username='{}'".format(username))
        userid = cursor.fetchone()
        cursor.execute("SELECT * FROM video WHERE UserID!={}".format(userid[0]))
        rows = cursor.fetchall()
        row_headers=[x[0] for x in cursor.description]
        json_data=[]
        for result in rows:
            json_data.append(dict(zip(row_headers,result)))
        print(json_data, file=sys.stderr)
        cursor.close()
        conn.close()
        return jsonify(json_data)
    cursor.close()
    conn.close()
    return redirect(url_for('login'))

@app.route('/delete/<videoid>')
def delete(videoid):
    cursor, conn = connection()
    print(videoid, file=sys.stderr)
    cursor.execute("SELECT VideoUser FROM video WHERE VideoID={}".format(videoid))
    tempVideoUser = cursor.fetchone()[0]
    if 'username' in session:
        if session['username'] != tempVideoUser:
            cursor.close()
            conn.close()
            return redirect(url_for('homepage'))
        cursor.execute("SELECT VideoTitle FROM video WHERE VideoID={}".format(videoid))
        tempFile = cursor.fetchone()
        tempFile = tempFile[0]
        print(tempFile, file=sys.stderr)
        if tempFile == '':
            return redirect(url_for('homepage'))
        cursor.execute("SELECT VideoUser FROM video WHERE VideoID={}".format(videoid))
        tempVideoUser = cursor.fetchone()[0]
        if session['username'] != tempVideoUser:
            flash('Cannot delete video uploaded by someone else')
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('homepage'))
        cursor.execute("DELETE FROM video WHERE VideoID={}".format(videoid))
        cursor.execute("SELECT UserID FROM users WHERE Username='{}'".format((session['username'])))
        userid = cursor.fetchone()
        cursor.execute("UPDATE users SET TotalVideoCount = TotalVideoCount - \
                    1 WHERE Username = '{}'".format(str(session['username'])))
        conn.commit()
        os.remove("static/"+tempFile)
        cursor.close()
        conn.close()
        return redirect(url_for('homepage'))
    cursor.close()
    conn.close()
    return redirect(url_for('login'))

@app.route("/invalidcreds", methods=['GET','POST'])
def invalidcreds():
    return render_template('invalidcreds.html')

@app.route("/login", methods=['GET','POST'])
@limiter.limit("14400/day;600/hour;10/minute")
def login():
    if request.method == 'GET':
        return redirect("http://127.0.0.1:8080/")
    username = request.form['username']
    password = request.form['password']
    hashedpass = generate_password_hash(password)
    cursor, conn = connection()
    #switched to Username, Password
    cursor.execute("SELECT Username, Password FROM users WHERE Username='{}'".format(str(username)))
    #switched to fetchall
    result = cursor.fetchall()
    for item in result:
        if item[0] == username and item[1] == hashedpass:
            hashedpass = item[1]
            break
    #print(userid, file=sys.stderr)
    #print(password, file=sys.stderr)
    #print(hashedpass, file=sys.stderr)
    
    if result == None:
        cursor.close()
        conn.commit()
        conn.close()
        return render_template('invalidcreds.html')
    elif check_password_hash(item[1], password):
        cursor.close()
        conn.close()
        session['username'] = username
        return redirect(url_for('mainpage'))
    cursor.close()
    conn.commit()
    conn.close()
    if str(username) in result:
        return render_template('invalidcreds.html')
    return render_template('invalidcreds.html', error=result)

@app.route("/logout", methods=['GET','POST'])
def logout():
    session.pop('username', None)
    flash('You were logged out.')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
