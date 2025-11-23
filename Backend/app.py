from flask import Flask, jsonify, request, session
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from flask_cors import CORS
import bcrypt

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = "super_secret_key" 

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv('DB_PASSWORD'), #make a .env file and store your mysql connection password
    'database': 'matchtracker'
}

VALID_TABLE = ['game', 'tornament', 'matchInfo', 'team', 'player',
               'place', 'venue', 'prizepool', 'sponser', 'commentator',
               'organizer', 'manager', 'coach']

VALID_PRIMARY_KEY = ['game_id', 'tornament_id', 'matchInfo_id', 'team_id', 'player_id',
                     'place_id', 'venue_id', 'prizepool_id', 'sponser_id', 'commentator_id',
                     'organizer_id', 'manager_id', 'coach_id']

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def get_user_by_username():
    """
    Looks up a user by username in the UserAccount Table
    Returns user's information or None if not found.
    Simply reads from Database
    """
    connection = get_db_connection()
    if connection is None:
        return None
    
    cursor = None
    try: 
        cursor = connection.cursor(dicitonary=True)
        query = "SELECT user_id, username, password_hash, role FROM UserAccount WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        return user
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/regisiter', methods['POST'])
def register():
    """
    Register a new user.
    Expects JSON: { "username": "...", "password": "..." }
    """
    data = requeset.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    # 1. Validation
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    
    # 2. Check if username already exists
    if get_user_by_username(username):
        return jsonify({'error': 'username already exists'}), 400

    # 3. Hash password with bcyrpt
    # - encode(): str -> bytes
    # - decode(): bytes -> str (for storing in VARCHAR)
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # 4. Insert into UserAccount Table
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = None
    try:
        cursor = connection.cursor()
        query = curosr.execute(query, (username, password_hash, 'user')) # default to 'user' role
        connection.commit()

        return jsonify({
            'success': True,
            'message': 'user registered',
            'user_id': cursor.lastrowid,
            'username': username,
            'role': 'user'
        }), 201
    
    except Error as e:
        if connection:
            connection.rollback()
        return jsonify({'error':str(e)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}      
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400

    # 1. Search user in Database
    user = get_user_by_username(username)
    if not user:
        return jsonify({'error': 'invalid credentials'}), 401

    stored_hash = user['password_hash'] # string stored in database

    # 2. Compare provided password to stored bcyrpt hash
    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return jsonify({'error': 'invalid credentials'}), 401
    
    # 3. Store login info in session so user is remembered
    session['user_id'] = user['user_id']
    session['username'] = user['username']
    session['role'] = user['role']

    return jsonify({
        'success': True,
        'message': 'login successful',
        'user': {
            'user_id': user['user_id'],
            'username': user['username'],
            'role': user['role']
        }
    }), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'logged out'}), 200


@app.route('/getTable', methods=['POST']) 
def get_table():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    data = request.get_json()
    table_name = data.get('table_name').lower()
    
    if table_name not in VALID_TABLE:
        return jsonify({'error': 'Invalid table name'}), 400

    try: 
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"Select * From {table_name};")
        table = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(table)
    except: 
        return jsonify({'error: str(e)'}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/getEntry', methods=['POST']) 
def get_entry():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    data = request.get_json()
    table_name = data.get('table_name').lower()
    primary_key = data.get('primary_key').lower()
    id = data.get('id')
    
    if table_name not in VALID_TABLE:
        return jsonify({'error': 'Invalid table name'}), 400
    if primary_key not in VALID_PRIMARY_KEY:
        return jsonify({'error': 'Invalid Primary Key'}), 400

    try: 
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name} WHERE {primary_key} = %s", (id,))
        entry = cursor.fetchall()
        cursor.close()
        connection.close()
        if entry:
            return jsonify(entry)
    except Exception as e:  
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/deleteEntry', methods=['DELETE']) 
def delete_entry():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    data = request.get_json()
    table_name = data.get('table_name').lower()
    primary_key = data.get('primary_key').lower()
    id = data.get('id')
    
    if table_name not in VALID_TABLE:
        return jsonify({'error': 'Invalid table name'}), 400
    if primary_key not in VALID_PRIMARY_KEY:
        return jsonify({'error': 'Invalid Primary Key'}), 400

    try: 
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM {table_name} WHERE {primary_key} = %s", (id,))
        entry = cursor.fetchall()
        cursor.close()
        connection.close()
        if entry:
            return jsonify(entry)
    except Exception as e:  
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.post("/byGame")
def by_game():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        data = request.get_json(force=True) or {}
        game_id = data.get("game_id")
        if not game_id:
            return jsonify({'error': 'Missing game_id'}), 400

        cur = connection.cursor(dictionary=True)

        # Tournaments for the game
        cur.execute("""
            SELECT t.*
            FROM Tournament t
            WHERE t.game_id = %s
        """, (game_id,))
        tournaments = cur.fetchall()

        # Teams for the game (via tournaments)
        cur.execute("""
            SELECT DISTINCT tm.*
            FROM Team tm
            JOIN TournamentTeam tt ON tt.team_id = tm.team_id
            JOIN Tournament t      ON t.tournament_id = tt.tournament_id
            WHERE t.game_id = %s
        """, (game_id,))
        teams = cur.fetchall()

        # Players for the game (direct junction)
        cur.execute("""
            SELECT p.*
            FROM Player p
            JOIN PlayerGame pg ON pg.player_id = p.player_id
            WHERE pg.game_id = %s
        """, (game_id,))
        players = cur.fetchall()

        # Organizers for the game (via tournaments)
        cur.execute("""
            SELECT DISTINCT o.*
            FROM Organizer o
            JOIN Tournament t ON t.organizer_id = o.organizer_id
            WHERE t.game_id = %s
        """, (game_id,))
        organizers = cur.fetchall()

        cur.close()
        connection.close()
        return jsonify({
            "tournaments": tournaments,
            "teams": teams,
            "players": players,
            "organizers": organizers
        })

    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            cur.close()
        except: pass
        try:
            connection.close()
        except: pass
#todo: add insert element, and user login

if __name__ == '__main__':
    app.run(debug=True)
