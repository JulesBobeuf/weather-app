from datetime import datetime

from flask import Flask, render_template
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'Ma clé secrète'


@app.route('/', methods=['GET', 'POST'])
def accueil():
    form = CityForm()
    if form.validate_on_submit():
        nomVille = form.name.data
        dateDebut = form.dateDebut.data
        dateFin = form.dateFin.data
        return render_template('test.html', nom=nomVille, dateDebut=dateDebut, dateFin=dateFin)

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
    date = r['localObsDateTime'][0:9]
    heure = r['localObsDateTime'][11:19]
    return [temperature, humidte, pressionAtmos, date, heure]


def resReq(nomVille):
    maRequete = requeteToJson(nomVille)
    return [infosVille(maRequete), infosReleve(maRequete)]


class CityForm(FlaskForm):
    name = SelectField(u'Villes :', choices=[('Roubaix', 'Roubaix'), ('Paris', 'Paris'), ('Strasbourg', 'Strasbourg'),
                                             ('Lyon', 'Lyon'), ('Marseille', 'Marseille'), ('Montréal', 'Montréal')])
    dateDebut = DateField('Date',format='%Y-%m-%d')
    dateFin = DateField('Date',format='%Y-%m-%d',default=datetime.today())

if __name__ == '__main__':
    app.run()
