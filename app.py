from flask import Flask, render_template, request, make_response
import sqlite3
app = Flask(__name__)
results = [] # List of all news from db + added after
wrong = 0 # Number of wrong attemps
new = [] #Dic of every new post added manualy
@app.route('/post')
def post(): 
    global results
    event = None
    id = int(request.args.get('id'))
    for row in results:
        if row[0] == id:
            event = row
            break
    if event == None:
        event = make_response(get_html('static/404.html'), 404)
        return event
    return render_template('post.html', text = event)


@app.route('/export')
def data():
    global new
    return new

@app.route('/import', methods=['GET', 'POST'])
def add():
    #FIXME: 
    if request.method == 'GET':
        return get_html('static/add.html')
    global results
    for row in (request.form['data']):
        print (row)
        row = [elem.strip(" '") for elem in row[1:-1].split(',')] 
        results.append(row)
    return ('Done')


@app.route('/update', methods=['GET', 'POST'])
def update():
    global wrong, results, new
    if wrong < 5:
        if request.method == 'POST':
            if login(request.form['password']):
                if 'read_db' in request.form:
                    read()
                output = insert(request.form['nazov'], request.form['image'], request.form['alt'], request.form['date'], request.form['text'])
                results.append(output)
                new.append(output)
                del output
                return ("Všetko prebehlo úspešne")
            wrong += 1
            return 'Prihlásenie zlyhalo'

        if request.method == 'GET':
            return (get_html('static/update.html'))
    
def get_html(path):
    with open(path, 'r') as file:
        html = file.read()
    return html

def read():
    global results
    con = sqlite3.connect("data.db")
    db = con.cursor()
    db.execute("SELECT * FROM novinky;")
    results = db.fetchall()
read()

def login(password):
    if password == 'root':
        global wrong
        wrong = 0
        return True
    return False

def insert(nazov, image, alt, date, text):
    list =  (123, nazov, image, alt, date, text)
    return list




@app.route('/')
def index():
    global results
    print (results)
    return render_template('index.html', list = results)

@app.route('/foto')
def foto():
    return render_template('foto.html')
@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/homilie')
def homilie():
    return render_template('homilie.html')

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')

@app.route('/oznamy')
def oznamy():
    return render_template('oznamy.html')

@app.route('/prednasky')
def prednasky():
    return render_template('prednasky.html')

@app.route('/publikacie')
def publikacie():
    return render_template('publikacie.html')