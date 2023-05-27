from subscription_manager import Subscription
from flask import render_template
from flask import make_response
from database import Database
from flask import redirect
from flask import request
from flask import Flask
import random
import json
import time

app = Flask(__name__)
db = Database(path="db.json")
alpha = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
stream = Subscription(db)

def load_json(data):
  return json.loads(data.decode('utf-8'))

@app.route('/')
def app_index():
  if request.cookies.get('Authorization'):
    return render_template('index.html')
  return render_template('signin.html')

@app.route('/chats/<id>')
def app_chatroom(id):
  auth = request.cookies.get('Authorization')
  if auth:
    if id in db.load()['chats']:
      chat = db.load()['chats'][id]
      username = auth.split('.')[0]
      if username in chat['members'] or username == chat['owner']:
        if stream.is_subscribed(username):
          stream.unsubscribe(username)
          stream.subscribe(username, id)
        else:
          stream.subscribe(username, id)
        return render_template('chatroom.html', id=id)
  return redirect('/', code=302)

@app.route('/invite/<id>')
def app_invite(id):
  if request.cookies.get('Authorization'):
    if id in db.load()['chats']:
      username = request.cookies.get('Authorization').split('.')[0]
      chat = db.load()['chats'][id]
      if not username in chat['members'] and username != chat['owner']:
        account_data = db.load()['accounts']
        chat_data = db.load()['chats']
        account_data[username]['chats'].append(id)
        chat_data[id]['members'].append(username)
        db.set('chats', chat_data)
        db.set('accounts', account_data)
      return redirect('/chats/'+id, code=302)
  return redirect('/', code=302)

@app.route('/chats/<id>/leave')
def api_chat_leave(id):
  if id in db.load()['chats']:
    username = request.cookies.get('Authorization').split('.')[0]
    chat = db.load()['chats'][id]
    if username in chat['members'] or username == chat['owner']:
      chat_data = db.load()['chats']
      account_data = db.load()['accounts']

      account_data[username]['chats'].remove(id)
      if username == chat['owner']:
        for member in chat['members']:
          account_data[member]['chats'].remove(id)
        del chat_data[id]
      else:
        chat_data[id]['members'].remove(username)

      db.set('chats', chat_data)
      db.set('accounts', account_data)
      return {'success': True}
      
  return {'success': False, 'message': 'Invalid chatroom ID or user not in chatroom'}

@app.route('/chats/<id>/details')
def api_chat_details(id):
  if id in db.load()['chats']:
    data = db.load()['chats'][id]
    del data['history']
    return data
  else:
    return {'success': False, 'message': 'Invalid chatroom ID'}

@app.route('/chats/<id>/message', methods=['POST'])
def api_chat_message(id):
  chat_data = db.load()['chats']
  if id in chat_data:
    username = request.cookies.get('Authorization').split('.')[0]
    message = {
      'author': username,
      'content': load_json(request.data)['content']
    }
    chat_data[id]['history'].append(message)
    db.set('chats', chat_data)
    stream.dispatch(id, message)
    return {'success': True, 'data': message}
  return {'success': False, 'message': 'Invalid chat ID'}

@app.route('/chats/<id>/history')
def api_chat_history(id):
  chat_data = db.load()['chats']
  if id in chat_data:
    account_data = db.load()['accounts']
    if request.args.get('cursor'):
      pass
    else:
      messages = chat_data[id]['history'][-50:]
      
    for i, message in enumerate(messages):
      messages[i]['author'] = {
        'username': message['author'],
        'avatar': account_data[message['author']]['avatar']
      }
    return {'success': True, 'data': messages}
  return {'success': False, 'message': 'Invalid chat ID'}

@app.route('/logout')
def api_logout():
  response = make_response(redirect('/', code=302))
  response.set_cookie('Authorization', '', expires=0)
  return response

@app.route('/callback')
def api_callback():
  token = request.args.get('token')
  response = make_response(redirect('/', code=302))
  response.set_cookie('Authorization', token)
  return response

@app.route('/login', methods=['POST'])
def api_login():
  data = load_json(request.data)
  account_data = db.load()['accounts']
  if data['username'] in account_data:
    if data['password'] == account_data[data['username']]['password']:
      return {
        'success': True,
        'token': f'{data["username"]}.{hash(data["username"]+data["password"])}'
      }
  return {'success': False}

@app.route('/signup', methods=['POST'])
def api_signup():
  data = load_json(request.data)
  account_data = db.load()['accounts']
  if data['username'] in account_data:
    return {'success': False, 'message': 'Username already exists'}
  else:
    if data['username'] == '' or data['password'] == '':
      return {'success': False, 'message': 'Username or password cannot be empty'}
    else:
      for char in data['username']:
        if not char in list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'):
          return {'success': False, 'message': 'Only characters a-z, A-Z, 0-9 are allowed'}
      if not len(data['username']) >= 4 and len(data['username']) <= 20:
        return {'success': False, 'message': 'Usernames must be between 4 and 20 chars'}
      else:
        account_data[data['username']] = {
          'password': data['password'],
          'avatar': None,
          'joined': time.time(),
          'chats': []
        }
        
        database = db.load()
        database['accounts'] = account_data
        db.save(database)
        
        return {
          'success': True, 
          'token': f'{data["username"]}.{hash(data["username"]+data["password"])}'
        }

@app.route('/create', methods=['POST'])
def api_create():
  data = load_json(request.data)
  chat_data = db.load()['chats']

  if len(data['name']) >= 4 and len(data['name']) <= 15:
    id = ''.join([random.choice(alpha) for i in range(15)])
    while id in chat_data:
      id = ''.join([random.choice(alpha) for i in range(15)])

    username = request.cookies.get('Authorization').split('.')[0]
    chat_data[id] = {
      'id': id,
      'name': data['name'],
      'owner': username,
      'members': [],
      'history': []
    }

    account_data = db.load()['accounts']
    account_data[username]['chats'].append(id)
    
    db.set('chats', chat_data)
    db.set('accounts', account_data)
    return {
      'success': True,
      'id': id
    }
  return {'success': False, 'message': 'Chat names must be between 4 and 15 chars'}

@app.route('/<username>/chats')
def api_userchats(username):
  if request.cookies.get('Authorization').split('.')[0] == username:
    data = []
    for chat in db.load()['accounts'][username]['chats']:
      chat = db.load()['chats'][chat]
      del chat['history']
      data.append(chat)
    return data
  else:
    return {'success': False, 'message': 'Unauthorized'}

@app.route('/avatars/batch', methods=['POST'])
def api_avatars_batch():
  data = load_json(request.data)
  account_data = db.load()['accounts']
  avatars = {'data': {}}
  for member in data['members']:
    avatars['data'][member] = account_data[member]['avatar']
  return avatars

@app.route('/stream/<id>')
def api_stream(id):
  username = request.cookies.get('Authorization').split('.')[0]
  if stream.is_subscribed(username):
    queue = stream.get_stream(username)
    stream.ack(username)
    return {'data': queue}
  else:
    stream.subscribe(username, id)
    return {'data': []}
  

app.run(host='0.0.0.0', port=8080)
