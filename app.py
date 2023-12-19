from flask_session import Session
from flask import Flask, render_template, request, redirect, session
from functions import *

app = Flask(__name__)
wrong = 0 # Number of wrong attemps
new = [] #Dic of every new post added manualy
results = read() # List of all news from db + added after

log = [] # Track suspicious activity
def error_log(code):
    global log
    log.append((error(code))[0])
    return (error(code))[1]

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/root', methods=['GET', 'POST']) #TODO:
@login_required
def root():
    if request.method == 'GET':
        global wrong
        return str(wrong)



@app.route("/logout")
def logout():
    # Forget user_id
    session.clear()
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def authenticate():
    # Forget user_id
    session.clear()

    if request.method == "POST":
        # Ensure username and password were submitted
        if not request.form.get("username") or not request.form.get("password"):
            return error(422)

        # Verify username and password
        if login(request.form.get("password"), request.form.get("username")):

            # Remember which user has logged in
            session["user_id"] = request.form.get("username")
            return redirect("/")

        #TODO: if password is wrong return error and track logs
    # If method is GET
    else:
        return get_html('static/login.html')

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
            wrong = 0
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
                wrong = 0
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