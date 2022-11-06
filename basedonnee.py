from datetime import datetime

from flask import Flask
import sqlite3 as sql

def deleteDatabase():
    con = sql.connect('bd.sqlite')
    cur = con.cursor()
    cur.execute('''DROP TABLE IF EXISTS VILLE''')
    cur.execute('''DROP TABLE IF EXISTS RELEVE''')
    cur.execute('''DROP TABLE IF EXISTS PAYS''')
    con.commit()
    con.close()
def createDatabase():
    con = sql.connect('bd.sqlite')
    cur = con.cursor()
    cur.execute('''CREATE TABLE VILLE ( idVille INTEGER primary key AUTOINCREMENT, nomVille varchar);''')
    cur.execute('''CREATE TABLE PAYS ( idPays INTEGER primary key AUTOINCREMENT, nomPays varchar);''')
    cur.execute('''CREATE TABLE RELEVE ( idReleve INTEGER primary key AUTOINCREMENT, temperature INT, humidite INT, pression INT, dateDuReleve VARCHAR, heure VARCHAR, idVille INTEGER REFERENCES VILLE(idVille));''')
    con.commit()
    con.close()

def ajoutVille(ville):
    data = [(ville)]
    con = sql.connect('bd.sqlite')
    cur = con.cursor()
    cur.execute("INSERT INTO VILLE(nomVille) VALUES (?)", data)
    con.commit()
    con.close()


def ajoutPays(pays):
    data = [(pays)]
    con = sql.connect('bd.sqlite')
    cur = con.cursor()
    cur.execute("INSERT INTO PAYS(nomPays) VALUES (?)", data)
    con.commit()
    con.close()

def ajoutReleve(temperature,humidite,pression,dateDuReleve,heure,ville ):
    dateDuReleve = datetime.strptime(dateDuReleve, "%Y-%m-%d").date()
    data = [temperature,humidite,pression,dateDuReleve,heure,ville]
    con = sql.connect('bd.sqlite')
    cur = con.cursor()
    cur.execute("INSERT INTO RELEVE(temperature,humidite,pression,dateDuReleve,heure,idVille) VALUES (?,?,?,?,?,?)", data)
    con.commit()
    con.close()

def getIdVille(ville):
    data = [(ville)]
    con = sql.connect('bd.sqlite')
    cur = con.cursor()
    cur.execute("SELECT idVille FROM VILLE WHERE nomVille=(?)", data)
    id = cur.fetchone()
    con.close()
    return id[0]

def getIdPays(pays):
    data = [(pays)]
    con = sql.connect('bd.sqlite')
    cur = con.cursor()
    cur.execute("SELECT idPays FROM PAYS WHERE nomPays=(?)", data)
    id = cur.fetchone()
    con.close()
    return id[0]

def getVille(ville):
    data = [(ville)]
    con = sql.connect('bd.sqlite')
    cur = con.cursor()
    cur.execute("SELECT idVille FROM VILLE WHERE nomVille=(?)", data)
    id = cur.fetchone()
    con.close()
    return id

def getPays(pays):
    data = [(pays)]
    con = sql.connect('bd.sqlite')
    cur = con.cursor()
    cur.execute("SELECT idPays FROM PAYS WHERE nomPays=(?)", data)
    id = cur.fetchone()
    con.close()
    return id

def relevePourUneVille(ville):
    data = [(ville)]
    con = sql.connect('bd.sqlite')
    cur = con.cursor()
    cur.execute("SELECT idVille FROM VILLE WHERE nomVille=(?)", data)
    id = cur.fetchone()
    id = id[0]
    idv=[(id)]
    cur.execute("SELECT * FROM RELEVE WHERE idVille=(?)",idv)
    tab = cur.fetchall()
    con.close()
    return tab

def relevePourUneVilleEtDate(ville,dateDebut,dateFin):
    data = [(ville)]
    dateDebut = dateDuReleve = datetime.strptime(dateDebut, "%Y-%m-%d").date()
    dateFin = dateDuReleve = datetime.strptime(dateFin, "%Y-%m-%d").date()
    con = sql.connect('bd.sqlite')
    cur = con.cursor()
    cur.execute("SELECT idVille FROM VILLE WHERE nomVille=(?)", data)
    id = cur.fetchone()
    id = id[0]
    datas=[(id),(dateDebut),(dateFin)]
    cur.execute("SELECT * FROM RELEVE WHERE idVille=(?) AND dateDuReleve BETWEEN (?) AND (?) ",datas)
    tab = cur.fetchall()
    con.close()
    return tab

