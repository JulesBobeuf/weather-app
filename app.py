import atexit
from datetime import datetime

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField
import os

import basedonnee as bd
import visualisationDonnees


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'Ma clé secrète'

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
        )
    else:
        app.config.from_mapping(test_config)

    @app.route('/', methods=['GET', 'POST'])
    def accueil():
        form = CityForm()
        if form.validate_on_submit():
            nomVille = form.name.data
            dateDebut = form.dateDebut.data
            dateFin = form.dateFin.data

            tabReleveVille = bd.relevePourUneVille(nomVille)
            visualisationDonnees.temperatureVisu([x[4] for x in tabReleveVille], [x[1] for x in tabReleveVille])
            visualisationDonnees.humiditeVisu([x[4] for x in tabReleveVille], [x[2] for x in tabReleveVille])
            visualisationDonnees.pressionVisu([x[4] for x in tabReleveVille], [x[3] for x in tabReleveVille])

            return render_template('infosVille.html', nom=nomVille, dateDebut=dateDebut, dateFin=dateFin,
                                   tabReleveVille=tabReleveVille)

        return render_template('form.html', form=form)

    def requeteToJson(ville):
        r = requests.get(f'https://wttr.in/{ville}?format=j1')
        infosJson = r.json()
        return infosJson

    def infosVille(jsonRequest):
        r = jsonRequest['nearest_area'][0]
        nomVille = r['areaName'][0]['value']
        nomPays = r['country'][0]['value']
        return [nomVille, nomPays]

    def infosReleve(jsonRequest):
        r = jsonRequest['current_condition'][0]
        temperature = r['temp_C']
        humidte = r['humidity']
        pressionAtmos = r['pressure']
        date = r['localObsDateTime'][0:10]
        heure = r['localObsDateTime'][11:19]
        return [temperature, humidte, pressionAtmos, date, heure]

    def resReq(nomVille):
        maRequete = requeteToJson(nomVille)
        return [infosVille(maRequete), infosReleve(maRequete)]

    def resetDatabase():
        bd.deleteDatabase()
        bd.createDatabase()

    def getData(ville):
        tab = resReq(ville)
        if (tab[0][0] == "Montreal"):
            ville = "Montreal"
        elif (tab[0][0] == "Saint-Merri"):
            ville = "Paris"
        elif (tab[0][0] == "Strassbourg"):
            ville = "Strasbourg"
        elif (tab[0][0] == "Madrague De la Ville"):
            ville = "Marseille"
        elif (tab[0][0] == "Fourviere"):
            ville = "Lyon"

        y = bd.getVille(ville)
        if not y:
            bd.ajoutVille(ville)
        x = bd.getPays(tab[0][1])
        if not x:
            bd.ajoutPays(tab[0][1])
        x = bd.getIdVille(ville)
        bd.ajoutReleve(tab[1][0], tab[1][1], tab[1][2], tab[1][3], x)

    def automatization():
        getData("Montreal")
        print("done Montreal")
        getData("Roubaix")
        print("done Roubaix")
        getData("Paris")
        print("done Paris")
        getData("Strasbourg")
        print("done Strasbourg")
        getData("Marseille")
        print("done Marseille")
        getData("Lyon ")
        print("done Lyon")

    # print(bd.relevePourUneVille("Montreal")) A TESTER ( avec une route web maybe et une fonction + return
    # resetDatabase()
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=automatization, trigger="interval", seconds=10)
    # scheduler.start()

    atexit.register(lambda: scheduler.shutdown())
    """

    class CityForm(FlaskForm):
        name = SelectField(u'Villes :',
                           choices=[('Roubaix', 'Roubaix'), ('Paris', 'Paris'), ('Strasbourg', 'Strasbourg'),
                                    ('Lyon', 'Lyon'), ('Marseille', 'Marseille'), ('Montréal', 'Montréal')])
        dateDebut = DateField('Date', format='%Y-%m-%d')
        dateFin = DateField('Date', format='%Y-%m-%d', default=datetime.today())

    return app
