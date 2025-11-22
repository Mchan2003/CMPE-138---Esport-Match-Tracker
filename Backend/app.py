from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

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
