from flask import Flask
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

def requeteToJson(ville):
    r = requests.get(f'https://wttr.in/{ville}?format=j1')
    return r.json()

@app.route('/json')
def affichage():
    return requeteToJson('Lens')


if __name__ == '__main__':
    app.run()
