from flask import Flask, render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

##########CRUD users##########
# 1. CREATE
@app.route('/users', methods = ['POST'])
def create_users():
    body = json.loads(request.data)
    user = entities.User(
        username = body['username'],
        name = body['name'],
        fullname = body['fullname'],
        password = body['password']
    )
    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()
    message = {'msg': 'User created'}
    json_message = json.dumps(message, cls=connector.AlchemyEncoder)
    return Response(json_message, status=201, mimetype='application/json')


# 2. READ
@app.route('/users', methods = ['GET'])
def read_users():
    db_session = db.getSession(engine)
    response = db_session.query(entities.User)
    users = response[:]
    json_message = json.dumps(users, cls=connector.AlchemyEncoder)
    return Response(json_message, status = 200, mimetype='application/json')

#por default el status ya es 200


# 3. UPDATE
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    # Buscar al usuario con ese id
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == \
    id).first()

    #Actualizamos los datos del usuario
    body = json.loads(request.data)
    for key in body.keys():
        setattr(user, key, body[key])

    #si no hago for hacer esto:
    #user.username = body['username']
    #user.name = body['name']
    #user.fullname = body['fullname']
    #user.password = body['password']
    #user.id = body['id'] ??

    #Guardamos la actualización
    db_session.add(user)
    db_session.commit()

    #Responder al cliente
    message = {'msg': 'User Updated'}
    json_message = json.dumps(message, cls=connector.AlchemyEncoder)
    return Response(json_message, status = 201, mimetype='application/json')

# 4. DELETE
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == \
    id).first()
    db_session.delete(user)
    db_session.commit()

    #Responder al cliente
    message = {'msg':'User Deleted'}
    json_message = json.dumps(message, cls=connector.AlchemyEncoder)
    return Response(json_message, status=201, mimetype='application/json')





if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
