#!/usr/bin/env python3

from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

# 宣告 Flask 實體並載入設定
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# 套用 SocketIO 至 Flask 實體
socket = SocketIO(app)

@app.route('/')
def index_page():
    return render_template('index.html')

@socket.on('myevent', namespace='/test')
def handle_my_custom_event(data):
    print('==========================================')
    print('received: ' + data['data'])
    print('==========================================')
    emit('myevent', {'data': 'server ok'})

@socket.on('connect', namespace='/test')
def test_connect():
    print("Connected!")

@socket.on('disconnect', namespace='/test')
def test_disconnect():
    print('Disconnected!')

def main():
    socket.run(app, '0.0.0.0', port=44411)

if __name__ == '__main__':
    main()