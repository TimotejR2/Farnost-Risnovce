from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

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

