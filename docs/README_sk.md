# Farnost-Risnovce

## Úvod

Tento repozitár obsahuje zdrojový kód pre webovú stránku [risnovcefara.sk](https://risnovcefara.sk). Stránka ponúka základné funkcie, ako je pridávanie príspevkov, prihlasovanie a ďalšie. Je primárne určená na nasadenie na serveri Vercel.

## Požiadavky

Tento projekt si vyžaduje nasledovné:

- Python 3.8+
- PostgreSQL
- Flask
- Werkzeug
- psycopg2

## Inštalácia a používanie

Ak chcete nainštalovať požadované balíky, spustite nasledujúci príkaz:

```bash
pip install -r requirements.txt
```

Ak chcete spustiť aplikáciu, použite príkaz Flask run:

```bash
flask run
```

## Vercel a vzdialená databáza

Tento projekt používa vzdialenú databázu umiestnenú na serveri Vercel. Ak sa chcete pripojiť k vzdialenej databáze, použite premennú prostredia `POSTGRES_URL` alebo vytvorte súbor `postgres.sql` v priečinku config a vložte doň adresu URL.

Viac informácií nájdete v [dokumentácii Vercel](https://vercel.com/docs/storage/vercel-postgres).

## Licencia

Všetky práva vyhradené

## Autor

Tento projekt vytvoril [Timotej Ružička](https://github.com/TimotejR2).