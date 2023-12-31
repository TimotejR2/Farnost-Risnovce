from flask import Flask, render_template, request, redirect, make_response
from functions import *
app = Flask(__name__)
wrong = 0 # Number of wrong attemps
new = [] #Dic of every new post added manualy
results = read() # List of all news from db + added after
oznamy_list = [] # 
log = [] # Track suspicious activity
homilie_data=[] # Všetky homílie vo forme list s viacrými lists
def error_log(code):
    global log
    log.append((error(code))[0])
    return (error(code))[1]

@app.route('/root', methods=['GET', 'POST'])
def root():
    if not user_logged_in("root"):
        return redirect("/login")

    dynamic_values = {
        'placeholder1': 'Default Value',
        'placeholder2': 'Value 2',
    }
    html = get_html('static/root.html', dynamic_values)
    return html 

@app.route("/logout")
def logout():
    # Forget user
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

            # Set session
            resp = redirect("/")
            resp.set_cookie('session', get_session_from_csv(request.form.get("username")), max_age=15768000)
            return resp

        # If password is wrong return error and track logs
        global wrong
        wrong += 1
        return error_log(401)

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
    if not user_logged_in("root"):
        return redirect("/login")
    global new
    return new

@app.route('/import', methods=['GET', 'POST'])
def add():
    if not user_logged_in("root"):
        return redirect("/login")
    if request.method == 'GET':
        return get_html('static/add.html')

    if request.method == 'POST':
        global results
        data = request.form['data']
        try:
            parsed_data = strtolist(data)
        except ValueError:
            return error_log(400)
        results.extend(parsed_data)
        return 'Done'

@app.route('/update', methods=['GET', 'POST'])
def update():
    if not user_logged_in():
        return redirect("/login")
    if request.method == 'GET':
        return (get_html('static/update.html'))

    if request.method == 'POST':
        global results, new
        output = insert(request.form['nazov'], request.form['image'], request.form['alt'], request.form['date'], request.form['text'])
        results.append(output)
        new.append(output)
        return ("Všetko prebehlo úspešne")

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
    global results
    return render_template('index.html', list = results)

@app.route('/logs')
def logs(): 
    if not user_logged_in("root"):
        return redirect("/login")
    global log
    return (log)

@app.route('/homilie')
def homilie():
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