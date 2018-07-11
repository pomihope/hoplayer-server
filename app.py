#!/usr/bin/env python3

from flask import Flask, redirect, render_template
from flask_socketio import SocketIO, send, emit

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

@socket.on('test')
def test_handler(data):
    print('==========================================')
    print('received: ' + data['data'])
    print('==========================================')
    emit('test', data)

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