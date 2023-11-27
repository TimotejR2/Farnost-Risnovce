from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)
wrong = 0
results = []
@app.route('/update', methods=['GET', 'POST'])
def update():
    global wrong, results
    if wrong < 5:
        if request.method == 'POST':
            if login(request.form['username'], request.form['password']):
                wrong = 0
                con = sqlite3.connect("data.db")
                db = con.cursor()
                db.execute("SELECT * FROM novinky;")
                results = db.fetchall()
                print (results)
                return ("Hotovo")
            else:
                wrong += 1
                return 'Login failed'

    if request.method == 'GET':
            return """
                <!DOCTYPE html>
                <html>
                <body>
                    <h1>Prihláste sa</h1>
                    <form method="post" action="/update">
                        <label for="username">Meno:</label>
                        <input type="text" id="username" name="username"><br><br>
                        <label for="password">Heslo:</label>
                        <input type="password" id="password" name="password"><br><br>
                        <input type="submit" value="Odoslať">
                    </form>
                </body>
                </html>
                """

def login(username, password):
    if username == 'root' and password == 'root':
        return True
    return False

@app.route('/')
def index():
    global results
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