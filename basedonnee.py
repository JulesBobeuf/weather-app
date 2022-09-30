from flask import Flask
import sqlite3 as sql

def createDatabase():
    con = sql.connect('bd.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE DC ( idVille int primary key, nomVille varchar);''')
    cur.execute('''CREATE TABLE VILLE ( insee int primary key, nomVille varchar, CodePostal VARCHAR, idPays INT REFERENCES PAYS(idPays));''')
    cur.execute('''CREATE TABLE PAYS ( idPays int primary key, nomPays varchar);''')
    cur.execute('''CREATE TABLE RELEVE ( idReleve int primary key, temperature INT, humidite INT, pression INT, dateDuReleve date, idVille varchar REFERENCES VILLE(idVille));''')
    con.commit()
    con.close()

def ajoutDC(ville):
    values = "\'"+ville
    con = sql.connect('bd.db')
    cur = con.cursor()
    cur.execute("INSERT INTO VILLE(nomVille) VALUES ( " + values + ");")
    con.commit()
    con.close()


def ajoutPays(pays):
    values = "\'"+pays
    con = sql.connect('bd.db')
    cur = con.cursor()
    cur.execute("INSERT INTO PAYS(nomPays) VALUES ( " + pays + ");")
    con.commit()
    con.close()

def ajoutReleve(temperature,humidite,pression,date,ville ):
    idville = getIdVille(ville)
    values = "\'"+temperature+"\',\'"+humidite+"\',\'"+pression+"\',\'"+date
    con = sql.connect('bd.db')
    cur = con.cursor()
    cur.execute("INSERT INTO VILLE(nomVille) VALUES ( " + values + ");")
    con.commit()
    con.close()

def getIdVille(ville):
    con = sql.connect('bd.db')
    cur = con.cursor()
    id = cur.execute("SELECT idVille FROM VILLE WHERE idVille=\',\'"+ville+"")
    con.close()
    return id