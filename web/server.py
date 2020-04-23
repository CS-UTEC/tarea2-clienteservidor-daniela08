from flask import Flask, render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)


@app.route('/esprimo/<numero>')
def es_primo(numero):
    num = 0
    if int(numero) >1:
        for i in range(2, int(numero)):
            if (int(numero) % i == 0):
                num += 1
        return str(num == 0)
    return str(int(numero) == 2)


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


@app.route('/create_user/<nombre>/<apellido>/<passwd>/<uname>')
def create_user(nombre, apellido, passwd, uname):
    #Crear un objeto (instancia de una entidad)
    user = entities.User(
        name = nombre,
        fullname = apellido,
        password = passwd,
        username = uname
    )

    #Guardar el objeto en la capa de ersistencia
    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()

    return "User created!"

@app.route('/read_users')
def read_users():
    db_session = db.getSession(engine)
    respuesta = db_session.query(entities.User)
    users = respuesta[:]
    i = 0
    pr1nt = ""
    for user in users:
        pr1nt += "Nombre: " + str(user.name) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"\
        + "Apellido: " + str(user.fullname) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"\
        + "Contraseña: " + str(user.password) + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"\
        + "Usuario: " + str(user.username) + "<br>"
        print(i, "NAME:\t", user.name, "\t\t", "FULLNAME:\t", user.fullname,
        "\t\t", "PASSWORD:\t", user.password, "\t\t", "USERNAME:\t",
        user.username)
        i += 1
    return pr1nt


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))


@app.route('/saludar')
def saludar():
    return "HOLA2"


@app.route('/palindrome/<palabra>')
def es_palindromo(palabra):
    letras = list(palabra)
    n = len(letras)
    reverso = ""
    for i in range (1, n + 1):
        reverso += letras[n - i]
    return str(reverso == palabra)


@app.route('/multiplo/<numero1>/<numero2>')
def es_multiplo(numero1, numero2):
    return str(int(numero1) % int(numero2) == 0)


@app.errorhandler(404)
def page_not_found(e):
    return "NOT FOUND", 404
