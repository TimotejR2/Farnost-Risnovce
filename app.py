from flask import Flask, render_template, request, redirect, make_response, send_file
from datetime import datetime
import json
from functions import add_oznamy

from functions import *
from config.config import (
    HOMILIE_LIMIT,
    POSTS_LIMIT,
    OZNAMY_LIMIT,
    DELAY_BETWEEN_WRONG_LOGINS,
    SESSION_AGE_LIMIT,
    CREATE_NEW_DB
)

with open('content/books.json', 'r') as f:
    books = json.load(f)

app = Flask(__name__)

# Set routes for databases
db = Database()

# Create database for all posts and remove old if needed
if CREATE_NEW_DB:
    db.create()

@app.context_processor
def inject_file_map():
    file_map = json.load(open('static/data/file_map.json', 'r'))
    return dict(file_map=file_map)

@app.errorhandler(404)
def not_found_error(e):
    return get_html('static/html/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return get_html('static/html/500.html'), 500


@app.route("/logout", methods=["GET"])
def logout():
    # Forget user by clearing session cookie
    resp = make_response(redirect('/'))
    resp.set_cookie('session', '', expires=0)
    return resp


@app.route("/login", methods=["GET", "POST"])
@security_delay
def authenticate():
    """
    Checks login attempts and verifies username and password.
    Returns error if too many attempts, sets session cookie and redirects
    if POST, saves wrong attempt time if password incorrect, returns login page.
    """
    if request.method == "GET":
        return get_html('static/html/login.html')

    # Ensure username and password were submitted
    if not request.form.get("username") or not request.form.get("password"):
        return error(422)

    # Verify username and password
    if login(request.form.get("password"), request.form.get("username")):
        # Set session cookie
        resp = redirect("/")

        resp.set_cookie('session',
            generate_session(request.form.get("username")),
            max_age=SESSION_AGE_LIMIT,
            samesite='Lax',
            secure=True,
            httponly=True)

        return resp

    # If password is wrong, save time of this incident in db
    db.execute('INSERT INTO wrong (cas) VALUES (%s)', (datetime.now(), ))
    return error(401)    

@app.route('/post', methods=["GET"])
def post():
    # Get post data from database
    try:
        post_id = int(request.args.get('id'))
        event = db.read_table(table_name='posts', limit=1, id=post_id)
    
    # Handle invalid or missing post ID   
    except (ValueError, IndexError):
        return error(404)

    # Add more images if possible
    event = list(event)
    event[2] = all_photos(event[2])
    event = tuple(event)

    # Render the post template with the retrieved post data
    return render_template('post.html', text=event)

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'GET':
        # Render the HTML form for updating
        return get_html('static/html/update.html')

    if request.method == 'POST':
        if not request.form['oblast']:
            return error(422)

        # Insert inputed data to database
        db.execute_file(
            'sql_scripts/user_insert/insert_posts.sql',
            (request.form['nazov'],
            image_formater(request.form['image'], db),
            request.form['alt'],
            request.form['date'],
            request.form['text'],
            request.form['oblast'])
        )

        return "Všetko prebehlo úspešne"

@app.route('/oznamy', methods=["GET"])
def oznamy():
    # Get oznamy from database
    oznamy_raw = db.execute_file('sql_scripts/select/oznamy.sql')
    oznamy = [interpretate_oznamy(oznamy_raw).values()]
    val = db.execute('SELECT nadpis, popis FROM oznamy_tyzden order by id DESC LIMIT 1;', fetchone=True)
    nazov = val[0]
    popis = val[1]
    return render_template('oznamy.html', oznamy = oznamy, nazov = nazov, popis = popis)

@app.route('/oznamy/update', methods=['POST', 'GET'])
@login_required
def get_events():
    if request.method == 'GET':
        return render_template('oznamy_input.html')

    if request.method == 'POST':
        
        # Get multi dimentional list of all oznamy
        
        #oznamy_list = make_oznamy_list()

        add_oznamy.add_oznamy()
        # Insert inputed data to database
        #db.execute('INSERT INTO oznamy (list) VALUES (%s);', (str(oznamy_list), ) )

        return "Všetko prebehlo úspešne"



@app.route('/', methods=["GET"])
def index():
    oblast, miesto = get_oblast_and_miesto()
    posts_list = db.execute_file("sql_scripts/select/posts.sql", (oblast, oblast, POSTS_LIMIT, 0))
    miesto = None
    if oblast != None:
        miesto = ['Rišňoviec', 'obce Kľačany', 'Sasinkova', 'Cirkvy'][oblast - 1]
    return render_template('index.html', list=posts_list, oblast=request.args.get('oblast'), page=1, miesto=miesto)

@app.route('/page/<page>', methods=["GET"])
def page(page):
    oblast, miesto = get_oblast_and_miesto()
    posts_list = db.execute_file("sql_scripts/select/posts.sql", (oblast, oblast, POSTS_LIMIT, (int(page) - 1) * POSTS_LIMIT))
    miesto = None
    if oblast != None:
        miesto = ['Rišňoviec', 'obce Kľačany', 'Sasinkova', 'Cirkvy'][oblast - 1]
    return render_template('index.html', list=posts_list, oblast=request.args.get('oblast'), page=int(page), miesto=miesto)



@app.route('/homilie',  methods=["GET", "POST"])
def homilie():
    if request.method == 'POST':
        return search_homilie()

    # Get list of all homilie and render template with them
    homilie_list = db.read_table("homilie", limit = HOMILIE_LIMIT)
    return render_template('homilie.html', list=homilie_list)

@app.route('/homilie/<datum>', methods=["GET"])
def kazen(datum):
    try:
        homilia = db.execute_file('sql_scripts/select/homilia_based_on_date.sql', args=(datum, ))[0]

    except:
        return error(404)
        
    return render_template('homilie.html', data=homilia)

@app.route('/homilie/update', methods=["GET", "POST"])
@login_required
def homilie_update():
    if request.method == 'GET':
        return get_html('static/html/homilie_input.html')

    # Insert inputed data to database
    db.execute_file('sql_scripts/user_insert/insert_homilie.sql',
        (request.form['datum'],
            request.form['citanie'],
            request.form['nazov'],
            request.form['text']))

    return "Všetko prebehlo úspešne"

@app.route('/historia/<place>', methods=["GET"])
def historia(place):
    try:
        return render_template(f'historia_{place}.html')

    except:
        return error(404)

@app.route('/publikacie', methods=["GET"])
def publikacie_main():
    return render_template('publikacie.html', books = books['publikacie'])

@app.route('/publikacie/<place>', methods=["GET"])
def publikacie(place):
    if place not in ['monografie', 'ucebne_materialy']:
        return error(404)

    return render_template(f'publikacie.html', books = books['publikacie'], category=place)

@app.route('/publikacie/kniha/<selected_book>', methods=["GET"])
def book(selected_book):
    for book in books['publikacie']:
        
        if book['id'] == selected_book:
            return render_template('kniha.html', book = book)
    return error(404)


@app.route('/kontakt', methods=["GET"])
def kontakt():
    return render_template('kontakt.html')

@app.route('/robots.txt', methods=["GET"])
def robots():
    return get_html('static/data/robots.txt')

@app.route('/krizovacesta', methods=["GET"])
def krizovacesta():
    return render_template('krizovacesta.html')

@app.route('/kalendar', methods=["GET"])
def kalendar():
    return render_template('kalendar.html')

@app.route('/cal.isc', methods=["GET"])
def cal_isc():
    return send_file('static/data/cal.isc', as_attachment=True, mimetype='text/calendar')
