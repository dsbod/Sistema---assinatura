
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
import os
import fitz  # PyMuPDF

app = Flask(__name__)
app.secret_key = 'supersecret'

login_manager = LoginManager()
login_manager.init_app(app)

# Usuário de exemplo
class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {'admin': {'password': 'admin'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        return 'Login inválido'
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    docs = os.listdir('documentos_prontos')
    return render_template('dashboard.html', docs=docs)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/documento/<nome>')
@login_required
def visualizar_documento(nome):
    path = os.path.join('documentos_prontos', nome)
    return send_file(path, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
