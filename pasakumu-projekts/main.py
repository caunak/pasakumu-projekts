
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'your_secret_key'  

os.makedirs(app.instance_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.sqlite3.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Workshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop.id'))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = generate_password_hash(password)
        if User.query.filter_by(username=username).first():
            flash("Lietotājvārds jau eksistē.")
            return redirect(url_for('register'))
        new_user = User(username=username, password=hashed, role='user')
        db.session.add(new_user)
        db.session.commit()
        flash("Reģistrācija veiksmīga!")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Nepareizs lietotājvārds vai parole.")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date = request.form.get('date')
        capacity = request.form.get('capacity')
        new_event = Workshop(title=title, description=description, date=date, capacity=int(capacity))
        db.session.add(new_event)
        db.session.commit()
        flash("Meistarklase pievienota!")
        return redirect(url_for('dashboard'))
    return render_template('create.html')

@app.route('/register_workshop/<int:workshop_id>')
@login_required
def register_workshop(workshop_id):
    already_registered = Registration.query.filter_by(user_id=current_user.id, workshop_id=workshop_id).first()
    if already_registered:
        flash("Jūs jau esat pieteicies šai meistarklasei!")
        return redirect(url_for('dashboard'))
    new_registration = Registration(user_id=current_user.id, workshop_id=workshop_id)
    db.session.add(new_registration)
    db.session.commit()
    flash("Pieteikums veiksmīgi pievienots!")
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    workshops = Workshop.query.all()
    registrations = []
    if current_user.role == 'admin':
        registrations = db.session.query(Registration, User, Workshop)            .join(User, Registration.user_id == User.id)            .join(Workshop, Registration.workshop_id == Workshop.id)            .all()
    return render_template('dashboard.html', workshops=workshops, registrations=registrations)

def create_admin():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        hashed = generate_password_hash('admin123')
        admin = User(username='admin', password=hashed, role='admin')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin lietotājs izveidots: lietotājvārds = admin, parole = admin123")

@app.before_request
def before_request():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        create_admin()
        app.db_initialized = True

if __name__ == '__main__':
    if not os.path.exists('instance'):
        os.makedirs('instance')
    app.run(debug=True)
