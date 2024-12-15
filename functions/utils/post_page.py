from flask import request
def get_oblast_and_miesto():
    oblast = request.args.get('oblast')
    if oblast:
        try:
            oblast = int(oblast)
            miesto = ['Rišňoviec', 'obce Kľačany', 'Sasinkova', 'Cirkvy'][oblast - 1]
            return oblast, miesto
        except (ValueError, IndexError):
            return None, None
    return None, None