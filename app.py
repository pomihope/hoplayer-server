#!/usr/bin/env python3

from flask import Flask, redirect, render_template
from flask_socketio import SocketIO, send, emit

import time

# 宣告 Flask 實體並載入設定
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# 套用 SocketIO 至 Flask 實體
socket = SocketIO(app)

@app.route('/')
def index_page():
    return redirect('/test')

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