from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re
import os



app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Configuration
DATABASE = 'medicino.db'

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'], user['email'])
    return None

def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes the database with the correct, complete schema.
    This is a fallback in case database_setup.py is not run.
    """
    if os.path.exists(DATABASE):
        return  # Assume database is already set up

    print("Database not found. Creating and populating with minimal data...")
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table for authentication
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Corrected medicines table with 'category'
    cursor.execute('''
        CREATE TABLE medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            dosage TEXT,
            side_effects TEXT,
            contraindications TEXT,
            price REAL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Corrected diagnosis_history table with user_id
    cursor.execute('''
        CREATE TABLE diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symptoms TEXT NOT NULL,
            diagnosed_condition TEXT,
            ayurvedic_remedy TEXT,
            medicine_suggestion TEXT,
            confidence_score REAL,
            user_feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Corrected symptoms_database table with 'description' and 'precautions'
    cursor.execute('''
        CREATE TABLE symptoms_database (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition_name TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            ayurvedic_remedy TEXT,
            medicine_suggestion TEXT,
            severity_level TEXT,
            description TEXT,
            precautions TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database created. Run 'python database_setup.py' for comprehensive data.")


def diagnose_symptoms(symptoms_text):
    """AI-like symptom diagnosis logic with complete data fields."""
    conn = get_db_connection()
    conditions = conn.execute("SELECT * FROM symptoms_database").fetchall()
    conn.close()

    input_symptoms = [s.strip().lower() for s in re.split(r'[,\s]+', symptoms_text.lower()) if s.strip()]
    best_match = None
    best_score = 0

    for condition in conditions:
        condition_symptoms = [s.strip().lower() for s in condition['symptoms'].split(',')]
        matches = sum(1 for symptom in input_symptoms if any(symptom in cs or cs in symptom for cs in condition_symptoms))
        score = matches / len(condition_symptoms) if condition_symptoms else 0

        if score > best_score and score > 0.3:
            best_score = score
            best_match = condition

    if best_match:
        return {
            'disease': best_match['condition_name'],
            'ayurvedic': best_match['ayurvedic_remedy'],
            'medicine': best_match['medicine_suggestion'],
            'confidence': round(best_score * 100, 2),
            'severity': best_match['severity_level'],
            'description': best_match['description'],
            'precautions': best_match['precautions']
        }
    else:
        return {
            'disease': 'Unable to determine condition',
            'ayurvedic': 'Please consult an Ayurvedic practitioner for personalized treatment.',
            'medicine': 'Please consult a healthcare professional for proper diagnosis.',
            'confidence': 0,
            'severity': 'unknown',
            'description': 'Your symptoms do not strongly match any known conditions in our database.',
            'precautions': 'Always seek professional medical advice for an accurate diagnosis.'
        }

@app.route('/')
def index():
    """Serve the main web application from index.html."""
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return render_template('landing.html')

@app.route('/app')
@login_required
def main_app():
    """Serve the main application (requires authentication)."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        
        # Check if username or email already exists
        existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', 
                                   (username, email)).fetchone()
        if existing_user:
            flash('Username or email already exists!', 'error')
            conn.close()
            return render_template('register.html')
        
        # Create new user
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                    (username, email, password_hash))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            user_obj = User(user['id'], user['username'], user['email'])
            login_user(user_obj)
            flash('Login successful!', 'success')
            return redirect(url_for('main_app'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/api/diagnose', methods=['POST'])
@login_required
def diagnose_api():
    """Diagnose symptoms API endpoint."""
    data = request.get_json()
    if not data or 'symptoms' not in data or not data['symptoms'].strip():
        return jsonify({'success': False, 'message': 'Symptoms are required'}), 400
    
    symptoms = data['symptoms']
    diagnosis_result = diagnose_symptoms(symptoms)

    # Save to history with user_id
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO diagnosis_history (user_id, symptoms, diagnosed_condition, ayurvedic_remedy, medicine_suggestion, confidence_score)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (current_user.id, symptoms, diagnosis_result['disease'], diagnosis_result['ayurvedic'], diagnosis_result['medicine'], diagnosis_result['confidence']))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'data': diagnosis_result})

@app.route('/api/medicine/<medicine_name>')
@login_required
def get_medicine_info_api(medicine_name):
    """Get medicine information API endpoint."""
    conn = get_db_connection()
    medicine = conn.execute('SELECT * FROM medicines WHERE name LIKE ?', (f'%{medicine_name}%',)).fetchone()
    conn.close()
    
    if medicine:
        return jsonify({'success': True, 'data': dict(medicine)})
    else:
        return jsonify({'success': False, 'message': 'Medicine not found'})

@app.route('/api/medicines')
@login_required
def list_medicines_api():
    """List all medicines API endpoint."""
    conn = get_db_connection()
    medicines = conn.execute('SELECT * FROM medicines ORDER BY name').fetchall()
    conn.close()
    return jsonify({'success': True, 'data': [dict(row) for row in medicines]})

@app.route('/api/history')
@login_required
def get_diagnosis_history_api():
    """Get diagnosis history API endpoint."""
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM diagnosis_history WHERE user_id = ? ORDER BY created_at DESC LIMIT 50', 
                          (current_user.id,)).fetchall()
    conn.close()
    return jsonify({'success': True, 'data': [dict(row) for row in history]})

if __name__ == '__main__':
    # On first run, create a DB if it doesn't exist.
    # For full data, user must run database_setup.py as per README.
    init_db() 
    print("Starting Medicino Web Portal...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)