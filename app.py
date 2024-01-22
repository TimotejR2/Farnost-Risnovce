from flask import Flask, render_template, request, redirect, make_response
import os
from datetime import timedelta, datetime

from functions import *
from config.config import HOMILIE_LIMIT, POSTS_LIMIT, OZNAMY_LIMIT, DELAY_BETWEEN_WRONG_LOGINS, SESSION_AGE_LIMIT, HOMILIE_SEARCH_DAYS


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
    # Check if there were not too many login attemps in past 3 days
    wrong = db.execute_file('sql_scripts/security/get_wrong_count.sql', (datetime.now() - timedelta(days=DELAY_BETWEEN_WRONG_LOGINS),))[0][0]
    if wrong > 2:
        return error(429)
    
    if request.method == "POST":
        # Ensure username and password were submitted
        if not request.form.get("username") or not request.form.get("password"):
            return error(422)

        # Verify username and password
        if login(request.form.get("password"), request.form.get("username")):
            # Set session cookie
            resp = redirect("/")
            resp.set_cookie('session', generate_session(request.form.get("username")), max_age=SESSION_AGE_LIMIT)
            return resp

        # If password is wrong, save it in db
        db.execute('INSERT INTO wrong (cas) VALUES (%s)', (datetime.now(), ))
        return error(401)

    # If method is GET
    else:
        return get_html('static/login.html')

@app.route('/post')
def post():
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
        # Insert
        db.execute_file('sql_scripts/user_insert/insert_posts.sql',
           (request.form['nazov'], request.form['image'], request.form['alt'],request.form['date'], request.form['text'], 'None'))
           
        return "Všetko prebehlo úspešne"

@app.route('/oznamy')
def oznamy():
    oznamy_list = db.execute_file('sql_scripts/select/oznamy.sql', (OZNAMY_LIMIT, ))
    oznamy_list = str_to_list(oznamy_list)
    return render_template('oznamy.html', oznamy_list = oznamy_list)

@app.route('/oznamy/update', methods=['POST', 'GET'])
def get_events():
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
            
        oznamy_list = make_oznamy_list()
        db.execute('INSERT INTO oznamy (list) VALUES (%s);', (str(oznamy_list), ) )
        return str(oznamy_list)

@app.route('/') 
def index():
    list = db.read_table("posts", limit = POSTS_LIMIT)
    return render_template('index.html', list = list)

@app.route('/homilie',  methods=["GET", "POST"])
def homilie():
    if request.method == 'POST':
        datum = request.form['date']
        if datum == '':
            return error(422)
        datum = datetime.strptime(datum, '%Y-%m-%d')
        datum1 = datum + timedelta(days=HOMILIE_SEARCH_DAYS)
        datum2 = datum - timedelta(days=HOMILIE_SEARCH_DAYS)
        list = db.execute('SELECT * FROM homilie WHERE datum < %s::timestamp AND datum > %s::timestamp', (str(datum1), str(datum2)))
        if len(list) == 0:
            return error(404)
        return render_template('homilie.html', list=list)

    list = db.read_table("homilie", limit = HOMILIE_LIMIT)
    return render_template('homilie.html', list=list)

@app.route('/homilie/update', methods=["GET", "POST"])
def homilie_update():
    if not authorised(1):
        return redirect("/login")

    if request.method == 'GET':
        return get_html('static/homilie_input.html')

    elif request.method == 'POST':
        # Insert
        db.execute_file('sql_scripts/user_insert/insert_homilie.sql',
           (request.form['datum'], request.form['citanie'], request.form['nazov'],request.form['text']))
           
        return "Všetko prebehlo úspešne"

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