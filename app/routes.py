from app import app,db
from flask import Flask, request, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os
from app.models import User,UserSchema, Todo, TodoSchema
from flask_cors import CORS
import random
import string


CORS(app)


def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None

    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']

    if not token:
      return jsonify({'message': 'Token is missing !'}), 401

    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
      current_user = User.query.filter_by(public_id=data['public_id']).first()
    except: 
      return jsonify({'message': 'Token is invalid !'}), 401
    
    return f(current_user, *args, **kwargs)
  
  return decorated 

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

  if not current_user.admin:
    return jsonify({'message':'Cannot perform that function ! '})

  users = User.query.all()

  output = []

  for user in users:
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    user_data['mail'] = user.mail
    output.append(user_data)

  return jsonify({'users': output})

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user,public_id):

  if not current_user.admin:
    return jsonify({'message':'Cannot perform that function ! '})


  user = User.query.filter_by(public_id=public_id).first()

  if not user:
    return jsonify({'message': 'No user found !'})

  user_data = {}
  user_data['public_id'] = user.public_id
  user_data['name'] = user.name
  user_data['password'] = user.password
  user_data['admin'] = user.admin
  user_data['mail'] = user.mail
  return jsonify({'user': user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):

  if not current_user.admin:
    return jsonify({'message':'Cannot perform that function ! '})

  data = request.get_json()

  hashed_password = generate_password_hash(data['password'],method='sha256')
 
  new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False, mail=data['mail'])
  db.session.add(new_user)
  db.session.commit()
  return jsonify({'message': 'new user created'})

# méthode qui permet de passer admin un utilisateur 
@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user,public_id):

  if not current_user.admin:
    return jsonify({'message':'Cannot perform that function ! '})


  user = User.query.filter_by(public_id=public_id).first()

  if not user:
    return jsonify({'message': 'No user found !'})

  user.admin = True
  db.session.commit()

  return jsonify({'message': 'The user has been promoted !'})


@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user,public_id):

  if not current_user.admin:
    return jsonify({'message':'Cannot perform that function ! '})

  user = User.query.filter_by(public_id=public_id).first()

  if not user:
    return jsonify({'message': 'No user found !'})
  
  db.session.delete(user)
  db.session.commit()
  
  return jsonify({'message': 'The user has been deleted !'})


@app.route('/login')
def login():
  auth = request.authorization

  if not auth or not auth.username or not auth.password:
    return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})

  user = User.query.filter_by(name=auth.username).first()

  if not user:
    return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})

  if check_password_hash(user.password, auth.password):
    token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)} , app.config['SECRET_KEY'])

    return jsonify({'token' : token.decode('UTF-8')})

  return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})


@app.route('/wasureta', methods=['PUT'])
def wasureta():

  data = request.get_json()

  user = User.query.filter_by(mail=data['mail']).first()

  if not user:
    return jsonify({'message': 'No user found with this mail !'})
  
  new_password = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(12))

  hashed_password = generate_password_hash(new_password,method='sha256')
 
  user.password = hashed_password
  db.session.commit()
  return jsonify({'new_password' : new_password})


@app.route('/todo',methods=['GET'])
@token_required
def get_all_todos(current_user):

  todos = Todo.query.filter_by(user_id=current_user.id).all()

  output = []

  for todo in todos:
    todo_data = {}
    todo_data['id'] = todo.id
    todo_data['text'] = todo.text
    todo_data['complete'] = todo.complete
    output.append(todo_data)
  
  return jsonify({'todos' : output})

@app.route('/todo/<todo_id>',methods=['GET'])
@token_required
def get_one_todo(current_user,todo_id):
  todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

  if not todo:
    return jsonify({'message': 'No todo found !'})
  
  todo_data = {}
  todo_data['id'] = todo.id
  todo_data['text'] = todo.text
  todo_data['complete'] = todo.complete

  return jsonify(todo_data)

@app.route('/todo',methods=['POST'])
@token_required
def create_todo(current_user):
  data = request.get_json()

  new_todo = Todo(text=data['text'],complete=False, user_id=current_user.id)
  db.session.add(new_todo)
  db.session.commit()

  return jsonify({'message':"Todo created !"})


@app.route('/todo/<todo_id>',methods=['PUT'])
@token_required
def complete_todo(current_user,todo_id):
  todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

  if not todo:
    return jsonify({'message': 'No todo found !'})
  
  todo.complete = True

  db.session.commit()


  return jsonify({'message': 'Todo item has been completed !'})


@app.route('/todo/<todo_id>',methods=['DELETE'])
@token_required
def delete_todo(current_user,todo_id):
  todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()

  if not todo:
    return jsonify({'message': 'No todo found !'})

  db.session.delete(todo)
  db.session.commit()

  return jsonify({'message': 'Todo item has been deleted !'})


# Run server
if __name__ == '__main__':
    app.run(debug=True)