from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SECRET_KEY'] = 'kunci-rahasia-yang-super-aman!'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat')
def chat():
    username = session.get('username')
    if not username:
        return redirect(url_for('index'))
    return render_template('chat.html', username=username)

@socketio.on('join')
def on_join(data):
    username = session.get('username')
    room = 'ruang_chat_utama'
    join_room(room)
    emit('status', {'msg': f'{username} telah bergabung.'}, room=room)

@socketio.on('message')
def handle_message(data):
    username = session.get('username')
    room = 'ruang_chat_utama'
    pesan = data['data']
    time = data.get('time')
    emit('response', {
        'username': username,
        'message': pesan,
        'time': time
    }, room=room)

@socketio.on('disconnect')
def on_disconnect():
    username = session.get('username')
    room = 'ruang_chat_utama'
    leave_room(room)
    emit('status', {'msg': f'{username} telah keluar.'}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
