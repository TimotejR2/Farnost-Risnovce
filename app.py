from flask import Flask, render_template, request
app = Flask(__name__)
from functions import *

wrong = 0 # Number of wrong attemps
new = [] #Dic of every new post added manualy
results = read() # List of all news from db + added after

log = []
def error_log(code):
    global log
    log.append((error(code))[0])
    return (error(code))[1]


@app.route('/post')
def post(): 
    global results
    try:
        id = int(request.args.get('id'))
    except ValueError:
        return error(404)
    event = next((row for row in results if row[0] == id), None)

    if event is None:
        return error(404)
    return render_template('post.html', text = event)

@app.route('/export')
def data():
    global new
    return new

@app.route('/import', methods=['GET', 'POST'])
def add():
    global wrong
    if wrong > 3:
        return error_log (403)
    if request.method == 'GET':
        return get_html('static/add.html')

    if request.method == 'POST':
        if login(request.form['password']):
            global results
            data = request.form['data']
            try:
                parsed_data = strtolist(data)
            except ValueError:
                return error_log(400)
            results.extend(parsed_data)
            return 'Done'
        wrong += 1
        return error_log(401)

@app.route('/update', methods=['GET', 'POST'])
def update():
    global wrong, results, new
    if wrong < 5:
        if request.method == 'GET':
            return (get_html('static/update.html'))
        if request.method == 'POST':
            if login(request.form['password']):
                if 'read_db' in request.form:
                    results = read()
                output = insert(request.form['nazov'], request.form['image'], request.form['alt'], request.form['date'], request.form['text'])
                results.append(output)
                new.append(output)
                return ("Všetko prebehlo úspešne")
            wrong += 1
            return error_log(401)
    return error_log (403)

@app.route('/oznamy')
def oznamy():

    pondelok = [[ 'Omsa za ...', '18:00', 'Risnovce'], ['Omsa za ...', '19:00', 'Risnovce'], ['Omsa za ...', '20:00', 'Risnovce'], '1.1.2023']
    utorok = [['Omsa za ...', '10:00', 'Risnovce'], ['Omsa za ...', '11:00', 'Risnovce'], '2.1.2023']
    streda = [['Omsa za ...', '10:00', 'Risnovce'], ['Omsa za ...', '11:00', 'Risnovce'], '3.1.2023']
    
    list = [pondelok, utorok, streda]
    return render_template('oznamy.html', list = list)

@app.route('/')
def index():
    global results
    return render_template('index.html', list = results)

@app.route('/logs')
def logs(): 
    global log
    return (log)

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/homilie')
def homilie():
    return render_template('homilie.html')

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')



@app.route('/prednasky')
def prednasky():
    return render_template('prednasky.html')

@app.route('/publikacie')
def publikacie():
    return render_template('publikacie.html')