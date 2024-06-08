from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@socketio.on('file_list')
def handle_file_list():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    emit('file_list', files)

if __name__ == '__main__':
    ssl_context = ('cert.pem', 'key.pem')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, ssl_context=ssl_context)
