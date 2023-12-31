from flask import Flask, render_template, request, redirect, make_response
from functions import *
app = Flask(__name__)
wrong = 0 # Number of wrong attemps
new = [] #Dic of every new post added manualy
results = read() # List of all news from db + added after
oznamy_list = [] # 
log = [] # Track suspicious activity
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

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/homilie')
def homilie():
    a = ['Prvá adventná nedeľa', '(Mk 13, 33-37)', 'Otvorte srdcia...', '''        Keď odchádza syn alebo dcéra z domu rodičov na dlhší čas, rodičia sa snažia dať im primerané napomenutie, poučenie alebo nejakú radu, podľa ktorej sa majú riadiť. „Dávaj si pozor, dcéra moja, hlavne na zlé kamarátky!“, lúči sa matka s dcérou, ktorá ide na štúdiá. „Buď čestný, statočný a hlavne chlap!“, podáva ruku otec synovi, ktorý odchádza do zahraničia za prácou.
        Cirkev je nám starostlivou matkou, ktorá chce do našich sŕdc vložiť isté poučenie, napomenutie, ktoré by nám pomohlo, aby sme nezišli zo správnej životnej cesty a aby sme vytrvali v dobrom až do konca.
        Cirkev nám dnes predkladá v evanjeliu slová Pána Ježiša: „Bedlite a modlite sa, aby vás Pán nenašiel spať, ak príde nečakane!“ Tieto slová sú pre nás veľkou múdrosťou. Bedliť neznamená spať, váľať sa a leňošiť, ale každý deň si plniť povinnosti, žiť v zhode a láske s Bohom a ľuďmi.
        Mnohí kresťania chcú bedliť tak, že zostanú stáť a nepohnute čakajú, kedy príde koniec sveta. Aké by to bolo smiešne v rodine, keby si otec sadol, zobral noviny a čakal na koniec sveta. Čo by to bola za matka, keby si zobrala štrikovanie a čakala na svoju smrť. Čo by to bol za mladík, ktorý by šiel do krčmy a tam čakal na Kristov príchod. Zdá sa nám to smiešne, ale povedzme si bolestnú pravdu. Mnohokrát to v našom živote skutočne takto vyzerá.
        Určite ste už stretli rodinu, kde členovia žijú vedľa seba ako cudzinci. Jedia spoločne ten istý chlieb pri tom istom stole, ale navzájom sú si cudzí. Duševne sú si na kilometre vzdialení. A stačilo by len trochu sa usmiať a otvoriť ústa a hneď by sa v dome rozľahlo teplo a srdečnosť. Prečo sa stane, že manželia po niekoľkých rokoch sú už unudení, nemajú si čo povedať, nevedia sa tešiť. Vari čakajú na svoju smrť či koniec sveta?
        Alebo dvadsaťročný mládenec každý večer nepozná nič iné len bar. Nezaujíma ho láska, úsmev dievčaťa, dotyk jej ruky. Už dávno všetko prežil. Mal dievča a bez lásky, bez hanby. Najedol sa a teraz potrebuje len zapiť sklamanie, žiaľ, nudu, smútok. Sadne do baru a víno, pivo či alkohol je jeho začiatok i koniec.
       Prečo takto žijeme? Prečo si takto ničíme vzťahy? Prečo sa oberáme o radosť a šťastie? Je pravda, že záhaľka a postávanie má svoje čaro. V bare nájdeme kľud, pokoj i priateľov. Ale iba dočasne a veľmi povrchne. Zničíme si srdce, zničíme v sebe to, čo je tam ešte dobré. Možno tu nie ste tí, ktorí takto robia, ale odkážme to všetkým, ktorí takto konajú.
        Čo my ostatní? V tomto týždni bude spoveď. Je to pre nás prvá možnosť ako by sme sa Kristovi otvorili. Ten Ježiš, ktorý má prísť na Vianoce, nech príde do našich sŕdc, ktoré sa takto otvoria. Tak veľmi vám prajem, aby sa každé srdce, nech by bolo akokoľvek zavreté, v tejto chvíli otvorilo. Prichádza Kristus. Nech sa uskutoční advent v nás, v našom vnútri.''']
    b = ['Druhá adventná nedeľa', '(Mk 1, 1-8)', 'Vyrovnať cestu', '''        Akonáhle sa otvorili hranice po revolúcii, mnohí ľudia sa rozhodli cestovať do zahraničia a zoznámiť sa s krásou a životom iných krajov a národov. Vycestovať to znamenalo urobiť kvalitnú prípravu, zodpovedne sa prichystať na niečo nové.
        „Pripravte cestu Pánovi!“, znie v dnešnom evanjeliu. Kam nás to posiela predchodca Pána, Ján Krstiteľ? Kam to máme pripraviť cestu?
        Máme si dnes predovšetkým urovnať cestu do svojho vnútra. Ku svojmu ja máme cestu dobre známu, tá je dobre vychodená. Sme zatarasení sebou, svojimi problémami, ťažkosťami, radosťami. Ten vonkajšok máme pripravený. Mali by sme sa však pustiť iným smerom. Pozrieť sa do svojho kresťanského vnútra, do srdca. Mali by sme sa pozrieť na seba bez príkras, bez spoločenskej masky, bez divadielka, ktoré ľuďom predkladáme.
        Každá dolina..., to je zamyslenie nad sebou, ak zotrvávame v hriechu, treba sa namáhať, pracovať na sebe. Modlitbou a pevnou vierou vyrovnávam cestu. Hora a pahorok, to je pýcha, vynášanie sa nad druhých. Krivé cesty..., to sú všetky pokrytectvá, farizejstvo, to sú myšlienky, slová a činy, ktoré nenesú v sebe nijakú úprimnosť.
        Ďalej máme vyrovnať cestu k blížnemu. Nie blížneho využiť vo svoj prospech. Ján nás vyzýva, aby sme sa obrátili opačne, na cestu služby blížnemu. Ďalej máme urovnať svoju cestu k Bohu. Akú poznáme cestu k Bohu doteraz? Mnohí sa uspokoja s tým, že patria krstom do cirkvi, iným stačí, že prijali všetky sviatosti. Mnohí sa obrátia k Bohu len vtedy, keď im tečie do topánok: „Bože, pomôž!“ Mnohým cesta do kostola je akýmsi tajomným obchodom: „Ja som prišiel do kostola a ty mi, Bože, za to daj...!“
        Ján Krstiteľ nás vyzýva, aby sme takéto cesty zanechali, aby sme nehľadali Boha ako obchodného partnera alebo agenta poisťovne pri pohrome a ťažkostiach, ale aby sme sa k nemu vydali cestou pokory a lásky ako jeho milované deti. Ide o to, aby sme sa Kristovi naplno oddali, otvorili, zmenili svoj život. A to je prijať nový životný štýl, pustiť Krista do svojho srdca a to zmení všetko a to je kresťanstvo. To predpokladá, že moja duša bude pohotovo oddaná Bohu a srdce bude nastavené na zmenu života. A to je to najťažšie. To chce urobiť jasný krok. A preto mnohí ľudia ostanú len pred touto bránou a nikdy nenájdu radosť a požehnanie s kresťanstva.
        Urobme teda jasný krok: Prestaňme so starým spôsobom života, pomáhajme, pretrhnime hriešne známosti, buďme verní v manželstvách, zoberme za seba zodpovednosť pri výchove detí, hľadajme pravdu a Kristovo evanjelium.
        Keď Bohu oddáme našu slobodu, až vtedy zostaneme slobodní. Keď Bohu oddáme naše srdce, až vtedy začneme milovať.''']
    list = [a,b]
    return render_template('homilie.html', list=list)

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')

@app.route('/prednasky')
def prednasky():
    return render_template('prednasky.html')

@app.route('/publikacie')
def publikacie():
    return render_template('publikacie.html')