#!/usr/bin/env python3

from flask import Flask, Response, request, redirect, render_template
from flask_socketio import SocketIO, send, emit
from flask_login import LoginManager, UserMixin

import json
import time

# 宣告 Flask 實體並載入設定
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# 套用 SocketIO 至 Flask 實體
socket = SocketIO(app)
# 套用 LoginManager 至 Flask 實體
login_manager = LoginManager(app)

# 儲存使用者資訊
users = {}  

class User(UserMixin):      
    def __init__(self, userid):
        super()
        self.id = userid

@login_manager.user_loader
def user_loader(userid):
    if userid in users:    
        return User(userid)
    else:
        return None

@app.route('/')
def index_page():
    return redirect('/test')

@app.route('/users', methods=['GET', 'POST'])
def users_api():
    if request.method == 'GET':
        return Response(json.dumps({'status': 200}, ensure_ascii=False), content_type='application/json; charset=utf-8')
    if request.method == 'POST':
        # 取得使用者名稱
        username = request.json['name']
        return Response(json.dumps({'status': 201}, ensure_ascii=False), content_type='application/json; charset=utf-8'), 201

@app.route('/test')
def test_page():
    return render_template('test.html')

def test_time():
    print('==========================================')
    print('ack')
    print('==========================================')
    print(time.time())

@socket.on('test')
def test_handler(data):
    print('==========================================')
    print('received: ' + data['data'])
    print('==========================================')
    print(time.time())
    emit('test', data, callback=test_time)

@socket.on('connect')
def connect_handler():
    print("Connected!")

@socket.on('disconnect')
def disconnect_handler():
    print('Disconnected!')

def main():
    socket.run(app, '0.0.0.0', port=44411)

if __name__ == '__main__':
    main()