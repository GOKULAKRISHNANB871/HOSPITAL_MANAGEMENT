from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "secret"

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/hospitalDB"
mongo = PyMongo(app)

db = mongo.db.users  # Collection for storing users

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # Patient, Doctor, Admin

        # Insert into MongoDB
        db.insert_one({"name": name, "email": email, "password": password, "role": role})
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.find_one({"email": email, "password": password})
        
        if user:
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            return "Login Failed! Invalid credentials."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        users = db.find()
        return render_template('dashboard.html', users=users, user_name=session['user_name'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)