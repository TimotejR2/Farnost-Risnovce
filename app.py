from datetime import timedelta, datetime
from flask import Flask, render_template, request, redirect, make_response

from functions import *
from config.config import (
    HOMILIE_LIMIT,
    POSTS_LIMIT,
    OZNAMY_LIMIT,
    DELAY_BETWEEN_WRONG_LOGINS,
    SESSION_AGE_LIMIT,
)


app = Flask(__name__)

# Set routes for databases
db = Database()

# Create database for all posts and remove old if needed
db.create()

@app.errorhandler(404)
def not_found_error(e):
    return get_html('static/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return get_html('static/500.html'), 500


@app.route("/logout", methods=["GET"])
def logout():
    # Forget user by clearing session cookie
    resp = make_response(redirect('/'))
    resp.set_cookie('session', '', expires=0)
    return resp

@app.route("/login", methods=["GET", "POST"])
def authenticate():
    """
    Checks login attempts and verifies username and password.
    Returns error if too many attempts, sets session cookie and redirects
    if POST, saves wrong attempt time if password incorrect, returns login page.
    """
    # Check if there were not too many login attempts in the past
    delay = timedelta(days=DELAY_BETWEEN_WRONG_LOGINS)
    now = datetime.now()
    wrong = db.execute_file('sql_scripts/security/get_wrong_count.sql', (now - delay,))[0][0]

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

            resp.set_cookie('session',
             generate_session(request.form.get("username")),
              max_age=SESSION_AGE_LIMIT)

            return resp

        # If password is wrong, save time of this incident in db
        db.execute('INSERT INTO wrong (cas) VALUES (%s)', (datetime.now(), ))
        return error(401)

    # If method is GET
    return get_html('static/login.html')

@app.route('/post', methods=["GET"])
def post():
    # Attempt to retrieve a specific post from the database based on the ID in the request
    try:
        post_id = int(request.args.get('id'))
        event = db.read_table(table_name='posts', limit=1, id=post_id)
        event = list(event)
        event[2] = all_photos(event[2])
        event = tuple(event)
        print(event)
    except (ValueError, IndexError):
        # Handle invalid or missing post ID
        return error(404)

    if not event:
        # Handle case where no post is found for the given ID
        return error(404)

    # Render the post template with the retrieved post data
    return render_template('post.html', text=event)

@app.route('/update', methods=['GET', 'POST'])
def update():
    # Check if user is authorized to access (role 1)
    if not authorised(1):
        return redirect("/login")

    if request.method == 'GET':
        # Render the HTML form for updating
        return get_html('static/update.html')

    if request.method == 'POST':
        # Insert submited data to database
        if not request.form['oblast']:
            return error(422)

        image = request.form['image']

        # If image is not url, search for it in images folder
        if not '/' in image and image:
            image = '/static/images/' + image

        # If not image, add image with same id as post    
        if not image:
            id = db.execute_file('sql_scripts/select/last_post_id.sql')[0][0] + 1
            image = '/static/images/' + str(id) + '.jpg'

        # Insert inputed data to database
        db.execute_file(
            'sql_scripts/user_insert/insert_posts.sql',
            (request.form['nazov'],
            image,
            request.form['alt'],
            request.form['date'],
            request.form['text'],
            request.form['oblast'])
        )

        return "Všetko prebehlo úspešne"

@app.route('/oznamy', methods=["GET"])
def oznamy():
    # Get oznamy from database
    oznamy_list = db.execute_file('sql_scripts/select/oznamy.sql', (OZNAMY_LIMIT, ))
    # Convert oznamy to list and render template with them
    oznamy_list = str_to_list(oznamy_list)
    return render_template('oznamy.html', oznamy_list = oznamy_list)

@app.route('/oznamy/update', methods=['POST', 'GET'])
def get_events():
    # Check if user is authorized to access (role 1)
    if not authorised(1):
        return redirect("/login")

    if request.method == 'GET':
        return render_template('oznamy_input.html')

    if request.method == 'POST':
        # Get multi dimentional list of all oznamy and write it to database as string
        oznamy_list = make_oznamy_list()
        db.execute('INSERT INTO oznamy (list) VALUES (%s);', (str(oznamy_list), ) )

        return "Všetko prebehlo úspešne"

@app.route('/', methods=["GET"])
def index():
    # Get list of all news and render template with them
    if not request.args.get('oblast'):
        posts_list = db.execute_file("sql_scripts/select/posts_all.sql", (POSTS_LIMIT, ))
        return render_template('index.html', list = posts_list)

    try:
        oblast = int(request.args.get('oblast'))
    except (ValueError, IndexError):
        return error(404)

    posts_list = db.execute_file("sql_scripts/select/posts.sql", (oblast, POSTS_LIMIT))
    return render_template('index.html', list = posts_list)

@app.route('/homilie',  methods=["GET", "POST"])
def homilie():
    if request.method == 'POST':
        return search_homilie()

    # Get list of all homilie and render template with them
    homilie_list = db.read_table("homilie", limit = HOMILIE_LIMIT)
    return render_template('homilie.html', list=homilie_list)

@app.route('/homilie/update', methods=["GET", "POST"])
def homilie_update():
    # Check if user is authorized to access (role 1)
    if not authorised(1):
        return redirect("/login")

    if request.method == 'GET':
        return get_html('static/homilie_input.html')

    # Insert inputed data to database
    db.execute_file('sql_scripts/user_insert/insert_homilie.sql',
        (request.form['datum'],
            request.form['citanie'],
            request.form['nazov'],
            request.form['text']))

    return "Všetko prebehlo úspešne"

@app.route('/historia', methods=["GET"])
def historia():
    return redirect('/historia/risnovce')

@app.route('/historia/risnovce', methods=["GET"])
def historia_risnovce():
    return render_template('historia_risnovce.html')

@app.route('/historia/klacany', methods=["GET"])
def historia_klacany():
    return render_template('historia_klacany.html')

@app.route('/historia/sasinkovo', methods=["GET"])
def historia_sasinkovo():
    return render_template('historia_sasinkovo.html')


@app.route('/publikacie/monografie', methods=["GET"])
def monografie():
    return render_template('monografie.html')

@app.route('/publikacie/ucebnematerialy', methods=["GET"])
def ucebm():
    return render_template('ucebne_materialy.html')

@app.route('/kontakt', methods=["GET"])
def kontakt():
    return render_template('kontakt.html')

@app.route('/prednasky', methods=["GET"])
def prednasky():
    return render_template('prednasky.html')

@app.route('/publikacie', methods=["GET"])
def publikacie():
    return render_template('publikacie.html')

@app.route('/sitemap.xml')
def sitemap():
    return get_html('static/sitemap.xml')
