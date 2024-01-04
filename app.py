from flask import Flask, render_template, request, redirect, make_response
from functions import *
import os

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the PostgreSQL database URL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://default:NPV3x8mtnvGw@ep-rough-mode-91105827.us-east-1.postgres.vercel-storage.com:5432/verceldb"


# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your database model
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    nazov = db.Column(db.Text)
    obrazok = db.Column(db.Text)
    alt = db.Column(db.Text)
    datum = db.Column(db.Date)
    text = db.Column(db.Text)
    autor = db.Column(db.Text, default='Neznámy')

# Create the table in the database
db.create_all()


# Set routes for databases
POSTS_DB_PATH = '/tmp/posts.db'
POSTS_DB = Database(POSTS_DB_PATH)

# Create database for all posts and remove old
POSTS_DB.create('config/posts_db_schema.sql')

@app.route('/root', methods=['GET', 'POST'])
def root():
    if not user_logged_in("root"):
        return redirect("/login")

    dynamic_values = {
        'placeholder1': 'Default Value',
        'placeholder2': 'Value 2',
    }
    html = get_html('static/root.html', dynamic_values)
    return read_text_file()

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
            resp.set_cookie('session', get_session_from_csv(request.form.get("username")), max_age=15768000)
            return resp

        # If password is wrong, log error and track logs
        global wrong_attempts
        wrong_attempts += 1
        return log_error(401)

    # If method is GET
    else:
        return get_html('static/login.html')

@app.route('/post')
def post():
    
    global all_news_list
    print("all_news_list", all_news_list)
    try:
        post_id = int(request.args.get('id'))
        print ("id", post_id)
    except ValueError:
        return error(404)
    event = None
    for row in all_news_list:
        print("row0",row[0])
        if row[0] == post_id:
            event = row
            print("event",event)
            break
    if event is None:
        print('none')
        return error(404)
    return render_template('post.html', text=event)

@app.route('/export')
def data():
    if not user_logged_in("root"):
        return redirect("/login")
    global all_news_list
    return all_news_list

@app.route('/import', methods=['GET', 'POST'])
def add():
    if not user_logged_in("root"):
        return redirect("/login")

    if request.method == 'GET':
        return get_html('static/add.html')

    if request.method == 'POST':
        global news_list, all_news_list
        data = request.form['data']
        try:
            parsed_data = strtolist(data)
        except ValueError:
            return error_log(400)
        news_list.extend(parsed_data)
        all_news_list.append(parsed_data)
        return 'Done'

@app.route('/update', methods=['GET', 'POST'])
def update():
    if not user_logged_in():
        return redirect("/login")

    if request.method == 'GET':
        return (get_html('static/update.html'))

    if request.method == 'POST':
        global POSTS_DB
        db = POSTS_DB

        # Insert
        db.execute('INSERT INTO posts (nazov, obrazok, alt, datum, text) VALUES (?, ?, ?, ?, ?)',
           request.form['nazov'], request.form['image'], request.form['alt'],
           request.form['date'], request.form['text'])
           
        return "Všetko prebehlo úspešne"

@app.route('/oznamy')
def oznamy():
    global oznamy_list
    return render_template('oznamy.html', list = oznamy_list)

@app.route('/oznamy/update', methods=['POST', 'GET'])
def get_events():
    if not user_logged_in():
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
    db = Database('/tmp/posts.db')
    list = db.read_table('posts', limit = 5)
    return render_template('index.html', list = list)

@app.route('/logs')
def logs(): 
    if not user_logged_in("root"):
        return redirect("/login")
    global log
    return (log)

@app.route('/homilie',  methods=["GET", "POST"])
def homilie():
    if request.method == 'POST':
        return 'Na tejto funkcii sa ešte stále pracuje. Ďakujem za porozumenie.'
    global homilie_data
    return render_template('homilie.html', list=homilie_data)

@app.route('/homilie/update', methods=["GET", "POST"])
def homilie_update():
    if not user_logged_in("root"):
        return redirect("/login")

    if request.method == 'GET':
        return get_html('static/homilie_input.html')

    elif request.method == 'POST':
        global homilie_data
        list = []
        list.append(request.form['datum'])
        list.append(request.form['citanie'])
        list.append(request.form['nazov'])
        list.append(request.form['text'])
        homilie_data.append(list)
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
