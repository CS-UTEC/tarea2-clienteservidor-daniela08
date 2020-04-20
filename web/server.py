from flask import Flask, render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/saludar')
def saludar():
    return "HOLA2"


@app.route('/esprimo/<numero>')
def es_primo(numero):
    num = 0
    if int(numero) >1:
        for i in range(2, int(numero)):
            if (int(numero) % i == 0):
                num += 1
        return str(num == 0)
    return str(int(numero) == 2)


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


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


@app.errorhandler(404)
def page_not_found(e):
    return "NOT FOUND", 404



if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
