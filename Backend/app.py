from flask import Flask, jsonify, request
from datetime import datetime
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

VALID_TABLE = {
    'game': 'game_id', 
    'tournament': 'tournament_id', 
    'matchinfo': 'matchinfo_id', 
    'team': 'team_id', 
    'player': 'player_id',
    'place': 'place_id', 
    'venue': 'venue_id', 
    'prizepool': 'prizepool_id', 
    'sponsor': 'sponsor_id',  
    'commentator': 'commentator_id',
    'organizer': 'organizer_id', 
    'manager': 'manager_id', 
    'coach': 'coach_id'
}

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
    cursor = None 

    try: 
        data = request.get_json(force=True)
        table_name = data.get('table_name')

        if table_name is None:
            return jsonify({'error': 'Invalid input. Check json key format'}), 400

        table_name = table_name.lower();
        if table_name not in VALID_TABLE.keys():
            return jsonify({'error': 'Invalid table name'}), 400   

        cursor = connection.cursor(dictionary=True)
        query = f"Select * From {table_name};"
        cursor.execute(query)
        table = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(table)
    except Exception as e:  
        if connection:
            connection.rollback()  
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
    cursor = None 

    try: 
        data = request.get_json(force=True)
        table_name = data.get('table_name')
        id = data.get('id')

        if table_name is None or id is None:
            return jsonify({'error': 'Invalid input. Check json format'}), 400
        table_name = table_name.lower()
        if table_name not in VALID_TABLE.keys():
            return jsonify({'error': 'Invalid table name'}), 400
        primary_key= VALID_TABLE[table_name];

        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name} WHERE {primary_key} = %s"
        cursor.execute(query, (id,))
        entry = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(entry)
    except Exception as e:  
        if connection:
            connection.rollback() 
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

    try: 
        data = request.get_json(force=True)
        table_name = data.get('table_name')
        id = data.get('id')

        if table_name is None or id is None:
            return jsonify({'error': 'Invalid input. Check json format'}), 400
        table_name = table_name.lower()
        if table_name not in VALID_TABLE.keys():
            return jsonify({'error': 'Invalid table name'}), 400
        primary_key= VALID_TABLE[table_name];

        cursor = connection.cursor(dictionary=True)
        query = f"DELETE FROM {table_name} WHERE {primary_key} = %s"
        cursor.execute(query, (id,))
        connection.commit()
        return jsonify({
            'success': True, 
            'message': 'Entry Deleted',
            'rows_affected': cursor.rowcount
        }), 201
    except Exception as e:
        if connection:
            connection.rollback()   
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/insertEntry', methods=['POST']) 
def insert_entry():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = None

    try: 
        data = request.get_json()
        table_name = data.get('table_name').lower()
        entry = data.get('entry')

        if table_name is None or entry is None:
            return jsonify({'error': 'Invalid input. Check json format'}), 400
        table_name = table_name.lower()
        if table_name not in VALID_TABLE.keys():
            return jsonify({'error': 'Invalid table name'}), 400

        cursor = connection.cursor(dictionary=True)
        column_names = ', '.join(entry.keys())
        placeholders = ', '.join(['%s'] * len(entry))
        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        cursor.execute(query, tuple(entry.values()))
        connection.commit()
        return jsonify({
            'success': True, 
            'message': 'Entry inserted',
            'id': cursor.lastrowid
        }), 201
    except Exception as e:
        if connection:
            connection.rollback()   
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/updateEntry', methods=['PUT']) 
def update_entry():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = None

    try: 
        data = request.get_json()
        table_name = data.get('table_name').lower()
        id = data.get('id')
        update_colms = data.get('update_colms')

        if table_name is None or update_colms is None or id is None:
            return jsonify({'error': 'Invalid input. Check json format'}), 400
        table_name = table_name.lower()
        if table_name not in VALID_TABLE.keys():
            return jsonify({'error': 'Invalid table name'}), 400

        primary_key = VALID_TABLE[table_name]

        set_clause = ", ".join([f"{key} = %s" for key in update_colms.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = %s"

        cursor = connection.cursor(dictionary=True)
        values = list(update_colms.values()) + [id]
        cursor.execute(query, values)
        connection.commit()

        return jsonify({
            'success': True, 
            'message': 'Entry updated',
            'rows_affected': cursor.rowcount
        }), 200 
    except Exception as e:
        if connection:
            connection.rollback()   
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/upcomingTornaments', methods=['POST']) 
def upcoming_tornaments():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = None 

    try: 
        data = request.get_json(force=True)
        current_time = data.get('current_time')
        current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")

        if current_time is None:
            return jsonify({'error': 'Invalid input. Check json key format'}), 400

        cursor = connection.cursor(dictionary=True)
        query = """SELECT T.tournament_id, T.tournament_name, T.tournament_schedule, 
                           T.tournament_format, G.game_name 
                    FROM Tournament T
                    INNER JOIN Game G ON T.game_id = G.game_id
                    WHERE tournament_schedule >= %s 
                    ORDER BY tournament_schedule;""" 
        cursor.execute(query, (current_time,))
        entries = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(entries)
    except Exception as e:  
        if connection:
            connection.rollback()  
        return jsonify({'error: str(e)'}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/getFormat', methods=['POST']) 
def get_format():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = None 

    try: 
        data = request.get_json(force=True)
        format = data.get('format')

        if format is None:
            return jsonify({'error': 'Invalid input. Check json key format: format)'}), 400

        cursor = connection.cursor(dictionary=True)
        query = """SELECT tournament_id, tournament_name, tournament_format
                   FROM Tournament
                   WHERE tournament_format = %s
                   ORDER BY tournament_schedule;""" 
        cursor.execute(query, (format,))
        entries = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(entries)
    except Exception as e:  
        if connection:
            connection.rollback()  
        return jsonify({'error: str(e)'}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/getPlacementPoints', methods=['POST']) 
def get_placement_points():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = None 

    try: 
        data = request.get_json(force=True)
        tournament_name = data.get('tournament_name')

        if tournament_name is None:
            return jsonify({'error': 'Invalid input. Check json key format: format)'}), 400

        cursor = connection.cursor(dictionary=True)
        query = """SELECT P.placement_id, P.placement_rank, P.placement_points, P.placement_prize_amount,
                          TM.team_name   
                   FROM Placement P
                   INNER JOIN Team TM On P.team_id = TM.team_id
                   INNER JOIN Tournament T On P.tournament_id = T.tournament_id
                   WHERE T.tournament_name = %s;
                   ORDER BY P.placement_points DESC;""" 
        cursor.execute(query, (tournament_name,))
        entries = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(entries)
    except Exception as e:  
        if connection:
            connection.rollback()  
        return jsonify({'error: str(e)'}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/getMatchesInTournament', methods=['POST']) 
def get_matches_in_tournament():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = None 

    try: 
        data = request.get_json(force=True)
        tournament_name = data.get('tournament_name')

        if tournament_name is None:
            return jsonify({'error': 'Invalid input. Check json key format: format)'}), 400

        cursor = connection.cursor(dictionary=True)
        query = """SELECT M.match_id, M.match_rounds, M.match_date_time, M.match_results,
                          T1.team_name AS team1_name, T2.team_name AS team2_name
                   FROM MatchInfo M
                   INNER JOIN Tournament T ON M.tournament_id = T.tournament_id
                   INNER JOIN Team T1 On M.team1_id = T1.team_id
                   INNER JOIN Team T2 On M.team2_id = T2.team_id
                   WHERE T.tournament_name = %s
                   ORDER BY M.match_date_time;""" 
        cursor.execute(query, (tournament_name,))
        entries = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(entries)
    except Exception as e:  
        if connection:
            connection.rollback()  
        return jsonify({'error: str(e)'}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/getTeamsInMatch', methods=['POST']) 
def get_teams_in_match():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = None 

    try: 
        data = request.get_json(force=True)
        tournament_name = data.get('tournament_name')

        if tournament_name is None:
            return jsonify({'error': 'Invalid input. Check json key format: format)'}), 400

        cursor = connection.cursor(dictionary=True)
        query = """SELECT TM.team_name
                   FROM Team TM
                   INNER JOIN TournamentTeam TT ON TM.team_id = TT.team_id
                   INNER JOIN Tournament T ON TT.tournament_id = T.tournament_id
                   WHERE T.tournament_name = %s
                   ORDER BY TM.team_name;""" 
        cursor.execute(query, (tournament_name,))
        entries = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(entries)
    except Exception as e:  
        if connection:
            connection.rollback()  
        return jsonify({'error: str(e)'}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/getTeamWins', methods=['POST']) 
def get_team_wins():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = None 

    try: 
        data = request.get_json(force=True)
        team_name = data.get('team_name')

        if team_name is None:
            return jsonify({'error': 'Invalid input. Check json key format: format)'}), 400

        cursor = connection.cursor(dictionary=True)
        query = """SELECT T.team_name, COUNT(*) AS wins
                   FROM Team T
                   INNER JOIN MatchInfo M ON T.team_id = M.match_winner_id
                   WHERE T.team_name = %s""" 
        cursor.execute(query, (team_name,))
        entries = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(entries)
    except Exception as e:  
        if connection:
            connection.rollback()  
        return jsonify({'error: str(e)'}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
