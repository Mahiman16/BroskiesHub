from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = 'users.json'

# ---------------------------
# Utility Functions
# ---------------------------
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

users = load_users()

# ---------------------------
# Auth Decorator
# ---------------------------
def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('x-api-key')
        if token != "mysecuretoken":
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# ---------------------------
# API Endpoints
# ---------------------------
@app.route('/api/users', methods=['GET'])
@token_required
def api_get_users():
    return jsonify(users)

@app.route('/api/users/<username>', methods=['GET'])
@token_required
def api_get_user(username):
    user = users.get(username)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/users', methods=['POST'])
@token_required
def api_create_user():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Username required'}), 400
    if username in users:
        return jsonify({'error': 'User already exists'}), 400
    users[username] = data
    save_users(users)
    return jsonify({'message': f'User {username} created successfully'}), 201

@app.route('/api/users/<username>', methods=['PUT'])
@token_required
def api_update_user(username):
    if username not in users:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    users[username].update(data)
    save_users(users)
    return jsonify({'message': f'User {username} updated successfully'})

@app.route('/api/users/<username>', methods=['DELETE'])
@token_required
def api_delete_user(username):
    if username in users:
        del users[username]
        save_users(users)
        return jsonify({'message': f'User {username} deleted successfully'})
    return jsonify({'error': 'User not found'}), 404

# ---------------------------
# HTML UI Routes
# ---------------------------
@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        age = request.form['age']
        if username in users:
            return "User already exists!"
        users[username] = {'username': username, 'email': email, 'age': age}
        save_users(users)
        return redirect(url_for('index'))
    return render_template('create_user.html')

@app.route('/update/<username>', methods=['GET', 'POST'])
def update_user(username):
    if request.method == 'POST':
        email = request.form['email']
        age = request.form['age']
        if username in users:
            users[username].update({'email': email, 'age': age})
            save_users(users)
            return redirect(url_for('index'))
        return "User not found!"
    return render_template('update_user.html', username=username)

@app.route('/delete/<username>')
def delete_user(username):
    if username in users:
        del users[username]
        save_users(users)
    return redirect(url_for('index'))

# ---------------------------
# Run the App
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
