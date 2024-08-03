from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import Config
from models import db, User
from modules.auth import auth_bp
from modules.transcribe import transcribe_bp
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('auth.login'))

def delete_old_files():
    result_folder = app.config['RESULT_FOLDER']
    now = time.time()
    cutoff = now - 24*60*60  # 24 hours

    for filename in os.listdir(result_folder):
        file_path = os.path.join(result_folder, filename)
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if file_mtime < cutoff:
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_old_files, trigger="interval", hours=1)
scheduler.start()

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(transcribe_bp, url_prefix='/transcribe')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        delete_old_files()  # 删除旧文件的初始调用
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('server.crt', 'server.key'))
