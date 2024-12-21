import nltk
nltk.download('punkt_tab')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from datetime import datetime

from keras.models import load_model
model = load_model('model.h5')
import json
import random
intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))
from flask import Flask, render_template, request, redirect, url_for, session, jsonify,Response,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from concurrent.futures import ThreadPoolExecutor
import warnings
import os



warnings.filterwarnings("ignore")
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'xyz'
app.config["MONGO_URI"] = "mongodb://localhost:27017/"
os.path.dirname("../templates")

executor = ThreadPoolExecutor(max_workers=4)  # Adjust the number of workers as needed

app.secret_key = 'abcd21234455'  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hosp'

mysql = MySQL(app)

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']        
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE status="active" AND email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['name'] = user['first_name']
            session['email'] = user['email']
            session['role'] = user['type']
            mesage = 'Logged in successfully !'            
            return redirect(url_for('dashboard'))
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
    
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    session.pop('name', None)
    session.pop('role', None)
    return redirect(url_for('login'))


@app.route('/roles', methods=['POST'])
def create_role():
    data = request.json
    role_name = data['role_name']
    status = data['status']

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO roles (role_name, status)
        VALUES (%s, %s)
    """, (role_name, status))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Role created successfully'}), 201

# Endpoint to get all roles
@app.route('/roles', methods=['GET'])
def get_all_roles():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    cursor.close()
    return jsonify(roles), 200

# Endpoint to get a specific role by ID
@app.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM roles WHERE role_id = %s", (role_id,))
    role = cursor.fetchone()
    cursor.close()

    if role:
        return jsonify(role), 200
    else:
        return jsonify({'message': 'Role not found'}), 404

# Endpoint to update a role
@app.route('/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    data = request.json
    role_name = data['role_name']
    status = data['status']

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE roles
        SET role_name = %s, status = %s
        WHERE role_id = %s
    """, (role_name, status, role_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Role updated successfully'}), 200

# Endpoint to delete a role by ID
@app.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM roles WHERE role_id = %s", (role_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Role deleted successfully'}), 200




# Fetch all permissions
@app.route('/permissions', methods=['GET'])
def get_permissions():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM permission")
    permissions = cursor.fetchall()
    cursor.close()
    return jsonify(permissions), 200

# Add a new permission
@app.route('/permissions', methods=['POST'])
def add_permission():
    data = request.json

    role_id = data['role_id']
    add_user = data.get('add_user', 0)
    edit_user = data.get('edit_user', 0)
    delete_user = data.get('delete_user', 0)
    add_prescription = data.get('add_prescription', 0)
    edit_prescription = data.get('edit_prescription', 0)
    delete_prescription = data.get('delete_prescription', 0)
    add_drug = data.get('add_drug', 0)
    edit_drug = data.get('edit_drug', 0)
    delete_drug = data.get('delete_drug', 0)
    add_test = data.get('add_test', 0)
    edit_test = data.get('edit_test', 0)
    delete_test = data.get('delete_test', 0)
    add_result = data.get('add_result', 0)
    edit_result = data.get('edit_result', 0)
    delete_result = data.get('delete_result', 0)
    add_vitals = data.get('add_vitals', 0)
    edit_vitals = data.get('edit_vitals', 0)
    delete_vitals = data.get('delete_vitals', 0)

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO permission (role_id, add_user, edit_user, delete_user, add_prescription, edit_prescription, delete_prescription,
        add_drug, edit_drug, delete_drug, add_test, edit_test, delete_test, add_result, edit_result, delete_result, add_vitals, edit_vitals, delete_vitals)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (role_id, add_user, edit_user, delete_user, add_prescription, edit_prescription, delete_prescription,
          add_drug, edit_drug, delete_drug, add_test, edit_test, delete_test, add_result, edit_result, delete_result,
          add_vitals, edit_vitals, delete_vitals))

    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Permission added successfully!"}), 201

# Update a permission
@app.route('/permissions/<int:permission_id>', methods=['PUT'])
def update_permission(permission_id):
    data = request.json

    add_user = data.get('add_user', 0)
    edit_user = data.get('edit_user', 0)
    delete_user = data.get('delete_user', 0)
    add_prescription = data.get('add_prescription', 0)
    edit_prescription = data.get('edit_prescription', 0)
    delete_prescription = data.get('delete_prescription', 0)
    add_drug = data.get('add_drug', 0)
    edit_drug = data.get('edit_drug', 0)
    delete_drug = data.get('delete_drug', 0)
    add_test = data.get('add_test', 0)
    edit_test = data.get('edit_test', 0)
    delete_test = data.get('delete_test', 0)
    add_result = data.get('add_result', 0)
    edit_result = data.get('edit_result', 0)
    delete_result = data.get('delete_result', 0)
    add_vitals = data.get('add_vitals', 0)
    edit_vitals = data.get('edit_vitals', 0)
    delete_vitals = data.get('delete_vitals', 0)

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE permission
        SET add_user = %s, edit_user = %s, delete_user = %s, add_prescription = %s, edit_prescription = %s, delete_prescription = %s,
            add_drug = %s, edit_drug = %s, delete_drug = %s, add_test = %s, edit_test = %s, delete_test = %s,
            add_result = %s, edit_result = %s, delete_result = %s, add_vitals = %s, edit_vitals = %s, delete_vitals = %s
        WHERE permission_id = %s
    """, (add_user, edit_user, delete_user, add_prescription, edit_prescription, delete_prescription,
          add_drug, edit_drug, delete_drug, add_test, edit_test, delete_test, add_result, edit_result, delete_result,
          add_vitals, edit_vitals, delete_vitals, permission_id))

    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Permission updated successfully!"}), 200

# Delete a permission
@app.route('/permissions/<int:permission_id>', methods=['DELETE'])
def delete_permission(permission_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM permission WHERE permission_id = %s", (permission_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Permission deleted successfully!"}), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    role_id = data['role_id']
    full_name = data['full_name']
    dob = data['dob']
    address = data['address']
    email = data['email']
    phone = data['phone']
    gender = data['gender']

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO users (role_id, full_name, dob, religion, address, email, phone, age, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (role_id, full_name, dob, address, email, phone, gender))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'User created successfully'}), 201

# Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users), 200

# Endpoint to get a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify(user), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# Endpoint to update user information
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    full_name = data['full_name']
    dob = data['dob']
    religion = data.get('religion', None)
    address = data['address']
    email = data['email']
    phone = data['phone']
    age = data['age']
    gender = data['gender']

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE users
        SET full_name = %s, dob = %s, religion = %s, address = %s, email = %s, phone = %s, age = %s, gender = %s
        WHERE user_id = %s
    """, (full_name, dob, religion, address, email, phone, age, gender, user_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'User updated successfully'}), 200

# Endpoint to delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'User deleted successfully'}), 200

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/chat")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)


if __name__ == "__main__":
    app.run()
