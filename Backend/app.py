from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv('DB_PASSWORD'), #make a .env file and store your mysql connection password
    'database': 'matchtracker'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/getPlayer', methods=['GET'])
def get_table():
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try: 
        cursor = connection.cursor(dictionary=True)
        cursor.execute("Select * From player;")
        players = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(players)
    except: 
        return jsonify({'error: str(e)'}), 500

if __name__ == '__main__':
    app.run(debug=True)