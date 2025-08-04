import datetime
import uuid
oznamy = [
    [
        datetime.date(2025, 8, 6), 
        'Premenenie Pána', 
        [
            (datetime.time(18, 0), 'Rišňovce', '+ rodina Jamborových')
        ]
    ], 
    [
        datetime.date(2025, 8, 7), 
        'Štvrtok', 
        [
            (datetime.time(18, 0), 'Kľačany', 'Na úmysel')
        ]
    ], 
    [
        datetime.date(2025, 8, 8), 
        'Piatok', 
        [
            (datetime.time(18, 0), 'Rišňovce', '+ rodina Audyových')
        ]
    ], 
    [
        datetime.date(2025, 8, 9), 
        'Sobota', 
        [
            (datetime.time(18, 0), 'Kľačany', '+ rodičia Kalamenovi, bratia a celá rodina')
        ]
    ], 
    [
        datetime.date(2025, 8, 10), 
        "19. cezročná nedel'a 10.8.2025", 
        [
            (datetime.time(9, 0), 'Sasinkovo', '+ Ján a Magdaléna Slobodových a synov Viliama a Jožka'), 
            (datetime.time(10, 30), 'Rišňovce', 'Za veriacich')
        ]
    ]
]
icalendar_events = []
icalendar_events.append("""BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
PRODID:-//Farnosť Rišňovce//Oznamy//SK
""")

for ozn in oznamy:
    date = ozn[0]
    title = ozn[1]
    for time, location, description in ozn[2]:
        start_time = datetime.datetime.combine(date, time).strftime('%Y%m%dT%H%M%S')
        end_time = (datetime.datetime.combine(date, time) + datetime.timedelta(hours=1)).strftime('%Y%m%dT%H%M%S')
        uid = str(uuid.uuid4())
        
        event = f"BEGIN:VEVENT\n" \
                f"UID:{uid}\n" \
                f"DTSTART;TZID=Europe/Bratislava:{start_time}\n" \
                f"DTEND;TZID=Europe/Bratislava:{end_time}\n" \
                f"SUMMARY:Sv. omša - {location}\n" \
                f"LOCATION:{location}\n" \
                f"DESCRIPTION:{description}\n" \
                f"END:VEVENT"
        
        icalendar_events.append(event)

# Spojenie všetkých udalostí do jedného reťazca
icalendar_output = "\n\n".join(icalendar_events) + "\nEND:VCALENDAR"
print(icalendar_output)
