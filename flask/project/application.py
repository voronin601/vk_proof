from flask import Flask, render_template, redirect, request, session, url_for
import json
import datetime
import time
app = Flask(__name__)
app.secret_key = 'its my life'
app.permanent_session_lifetime = datetime.timedelta(hours = 1)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/", methods = ['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('table'))
        else:
            return render_template('./start.html')
    elif request.method == 'POST':
        if (request.form.get('log') == 'sad.gpp@gmail.com' and request.form.get('pas') == '1QAZ.1712.blocked') or 'user' in session:
            session['user'] = True
            return redirect(url_for('table'))

@app.route("/table", methods = ['GET', 'POST'])
def table():
    if request.method == 'GET':
        if 'user' in session and session['user'] == True:
            with open('./static/json/user-key.json', 'r') as spis:
                data = json.load(spis)
            return render_template('./tab_key.html', spis = data)
        else:
            return redirect(url_for('hello'))
    elif request.method == 'POST':
        if 'key_add' in request.form:
            us = request.form.get('user')
            key = request.form.get('key')
            if key == "" or key == " ":
                return "ERROR KEY"
            with open('./static/json/user-key.json', 'r') as spis:
                data = json.load(spis)
            if us in data:
                return "This user already has a key"
            date = str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + " " + str(datetime.datetime.now().day) + "." + str(datetime.datetime.now().month) + "." + str(datetime.datetime.now().year)
            data[us] = [key, date]
            with open('./static/json/user-key.json', 'w') as spis:
                json.dump(data, spis)
            return redirect(url_for('table'))
        elif 'key_del' in request.form:
            us = request.form.get('user')
            with open('./static/json/user-key.json', 'r') as spis:
                data = json.load(spis)
            if us in data:
                data.pop(us)
            else: return "No such USER ID"
            with open('./static/json/user-key.json', 'w') as spis:
                json.dump(data, spis)
            return redirect(url_for('table'))

@app.route('/table/<idd>', methods = ['GET'])  
def proof(idd = None):
    with open('./static/json/user-key.json', 'r') as spis:
        if idd in json.load(spis):
            return 'True'
        else: 
            return 'False'

@app.route('/download/<wer>', methods = ['GET'])
def download_proof(wer = None):
    v = '1.0'               ####поменять версию
    if wer != v:
        return 'False'
    else:
        return 'True'

@app.route('/download', methods = ['GET'])
def download():
    if request.method == 'GET':
        href = ""                                   #поменять ссылку
        return '''<a href='%s'>Скачать</a>''' %href               


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 80)