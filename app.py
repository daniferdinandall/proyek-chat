from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kunci-rahasia-yang-super-aman!'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Halaman untuk login (memasukkan username)."""
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat')
def chat():
    """Halaman utama chat."""
    username = session.get('username')
    if not username:
        return redirect(url_for('index'))
    return render_template('chat.html', username=username)

@socketio.on('join')
def on_join(data):
    """Dijalankan saat klien bergabung ke ruang chat."""
    username = session.get('username')
    room = 'ruang_chat_utama'
    join_room(room)
    print(f'{username} telah bergabung ke ruang {room}')
    emit('status', {'msg': f'{username} telah bergabung.'}, room=room)

@socketio.on('message')
def handle_message(data):
    """Menerima pesan dari klien dan menyiarkannya."""
    username = session.get('username')
    room = 'ruang_chat_utama'
    pesan = data['data']
    print(f'Pesan dari {username}: {pesan}')
    # Siarkan pesan ke semua orang di ruangan yang sama
    emit('response', {'msg': f'<strong>{username}</strong>: {pesan}'}, room=room)

@socketio.on('disconnect')
def on_disconnect():
    """Dijalankan saat klien terputus."""
    username = session.get('username')
    room = 'ruang_chat_utama'
    leave_room(room)
    print(f'{username} telah terputus.')
    emit('status', {'msg': f'{username} telah keluar.'}, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)