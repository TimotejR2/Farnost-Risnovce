from flask import Flask, render_template, request, redirect, make_response
from functions import *
import os
import psycopg2

app = Flask(__name__)

# Set routes for databases
db = Database()

# Create database for all posts and remove old if needed
db.create()

@app.route("/logout")
def logout():
    # Forget user by clearing session cookie
    resp = make_response(redirect('/'))
    resp.set_cookie('session', '', expires=0)
    return resp

@app.route("/login", methods=["GET", "POST"])
def authenticate():
    if request.method == "POST":
        # Ensure username and password were submitted
        if not request.form.get("username") or not request.form.get("password"):
            return error(422)

        # Verify username and password
        if login(request.form.get("password"), request.form.get("username")):
            # Set session cookie
            resp = redirect("/")
            resp.set_cookie('session', generate_session(request.form.get("username")), max_age=15768000)
            return resp

        # If password is wrong, log error and track logs
        #TODO:
        #global wrong_attempts
        #wrong_attempts += 1
        return error(401)

    # If method is GET
    else:
        return get_html('static/login.html')

@app.route('/post')
def post():
    db=Database()
    try:
        event = db.read_table(table_name='posts', limit=1, id=int(request.args.get('id')))
    except (IndexError, ValueError):
        return error(404)
    if event == []:
        return error(404)
    return render_template('post.html', text=event)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if not authorised(1):
        return redirect("/login")

    if request.method == 'GET':
        return (get_html('static/update.html'))

    if request.method == 'POST':
        db = Database()

        # Insert
        db.execute_file('sql_scripts/insert_posts.sql',
           (request.form['nazov'], request.form['image'], request.form['alt'],request.form['date'], request.form['text'], 'None'))
           
        return "Všetko prebehlo úspešne"

@app.route('/oznamy')
def oznamy():
    return 'Not done'
    #return render_template('oznamy.html', list = oznamy_list)

@app.route('/oznamy/update', methods=['POST', 'GET'])
def get_events():
    return 'Not done'
    if not authorised(1):
        return redirect("/login")
    if request.method == 'GET':
        return render_template('oznamy_input.html')

    elif request.method == 'POST':
        # Get number of days submited
        days_submited = 7
        for i in range (days_submited):
            if request.form[('datum'+str(i))] == "":
                if i == 0:
                    return error(422)
                days_submited = i
                break
            
        global oznamy_list
        oznamy_list = []
        events_in_day = 5
        oznamy_list.append(request.form['datum'])
        for i in range (days_submited):
            var = [] # All events in day
            for j in range (events_in_day):
                if request.form['blok'+str(i)+'-cas'+str(j)] == "":
                    break
                
                text1 = request.form['blok'+str(i)+'-text'+str(j)+'-1']
                text2 = request.form['blok'+str(i)+'-text'+str(j)+'-2']
                time = request.form['blok'+str(i)+'-cas'+str(j)]
                var.append([text1, time, text2])
            var.append(request.form['datum'+str(i)])
            oznamy_list.append(var)
        oznamy_list.append(request.form['notes'])
        return str(oznamy_list)

@app.route('/') 
def index():
    db = Database()
    list = db.read_table("posts", limit = 5)
    return render_template('index.html', list = list)

@app.route('/homilie',  methods=["GET", "POST"])
def homilie():
    if request.method == 'POST':
        return request.form['date']
        return 'Na tejto funkcii sa ešte stále pracuje. Ďakujem za porozumenie.'

    db = Database()
    try:
        list = db.read_table("homilie", limit = 3)
    except IndexError:
        return error(404)
    if len(list) == 1:
        list = [list]
    print(list)
    return render_template('homilie.html', list=list)

@app.route('/homilie/update', methods=["GET", "POST"])
def homilie_update():
    if not authorised(1):
        return redirect("/login")

    if request.method == 'GET':
        return get_html('static/homilie_input.html')

    elif request.method == 'POST':
        db = Database()

        # Insert
        db.execute_file('sql_scripts/insert_homilie.sql',
           (request.form['datum'], request.form['citanie'], request.form['nazov'],request.form['text']))
           
        return "Všetko prebehlo úspešne"

#TODO:
@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')

@app.route('/prednasky')
def prednasky():
    return render_template('prednasky.html')

@app.route('/publikacie')
def publikacie():
    return render_template('publikacie.html')