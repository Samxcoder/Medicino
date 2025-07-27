from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3
import json
import re
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup
DATABASE = 'medicino.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create medicines table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            dosage TEXT,
            side_effects TEXT,
            contraindications TEXT,
            price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create diagnosis_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptoms TEXT NOT NULL,
            diagnosed_condition TEXT,
            ayurvedic_remedy TEXT,
            medicine_suggestion TEXT,
            confidence_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create symptoms_database table for better diagnosis
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS symptoms_database (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition_name TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            ayurvedic_remedy TEXT,
            medicine_suggestion TEXT,
            severity_level TEXT
        )
    ''')

    # Insert sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM medicines")
    if cursor.fetchone()[0] == 0:
        sample_medicines = [
            ('Paracetamol', 'Pain reliever and fever reducer', '500mg every 6 hours', 'Nausea, rash, liver damage (overdose)', 'Liver disease, alcohol dependency', 15.50),
            ('Ibuprofen', 'Anti-inflammatory pain reliever', '200-400mg every 4-6 hours', 'Stomach upset, headache', 'Stomach ulcers, kidney disease', 22.00),
            ('Cetirizine', 'Antihistamine for allergies', '10mg once daily', 'Drowsiness, dry mouth', 'Severe kidney disease', 18.75),
            ('Dolo', 'Paracetamol-based pain reliever', '650mg every 8 hours', 'Nausea, skin rash', 'Liver problems', 12.25),
            ('Aspirin', 'Pain reliever and blood thinner', '75-300mg daily', 'Stomach irritation, bleeding', 'Bleeding disorders, asthma', 8.50)
        ]

        cursor.executemany('''
            INSERT INTO medicines (name, description, dosage, side_effects, contraindications, price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_medicines)

    # Insert sample symptoms data
    cursor.execute("SELECT COUNT(*) FROM symptoms_database")
    if cursor.fetchone()[0] == 0:
        sample_conditions = [
            ('Viral Infection', 'fever,sore throat,body ache,headache,fatigue', 'Drink hot water with ginger and turmeric. Take rest and consume honey with warm water.', 'Paracetamol, Dolo', 'moderate'),
            ('Common Cold', 'sneezing,runny nose,congestion,mild headache,watery eyes', 'Steam inhalation with eucalyptus oil. Drink herbal tea with tulsi and ginger.', 'Cetirizine, Ibuprofen', 'mild'),
            ('Flu', 'high fever,severe headache,muscle pain,chills,fatigue,dry cough', 'Rest, increase fluid intake, consume kadha (herbal decoction) with immunity boosters.', 'Paracetamol, Ibuprofen', 'severe'),
            ('Allergic Reaction', 'sneezing,itching,rash,swelling,runny nose,watery eyes', 'Avoid allergens, use neem-based remedies, consume turmeric milk.', 'Cetirizine, Antihistamines', 'mild'),
            ('Headache', 'head pain,sensitivity to light,nausea,dizziness', 'Apply peppermint oil to temples, practice meditation, stay hydrated.', 'Aspirin, Ibuprofen', 'mild'),
            ('Stomach Upset', 'nausea,vomiting,stomach pain,diarrhea,loss of appetite', 'Consume buttermilk, avoid spicy food, drink ginger tea.', 'ORS, Probiotics', 'moderate'),
            ('Migraine', 'severe headache,nausea,vomiting,sensitivity to light and sound', 'Rest in dark room, apply cold compress, practice breathing exercises.', 'Aspirin, Specialized migraine medication', 'severe')
        ]

        cursor.executemany('''
            INSERT INTO symptoms_database (condition_name, symptoms, ayurvedic_remedy, medicine_suggestion, severity_level)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_conditions)

    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def diagnose_symptoms(symptoms_text):
    """AI-like symptom diagnosis logic"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all conditions from database
    cursor.execute("SELECT * FROM symptoms_database")
    conditions = cursor.fetchall()

    # Convert symptoms to lowercase for matching
    input_symptoms = [s.strip().lower() for s in re.split(r'[,\s]+', symptoms_text.lower()) if s.strip()]

    best_match = None
    best_score = 0

    for condition in conditions:
        condition_symptoms = [s.strip().lower() for s in condition['symptoms'].split(',')]

        # Calculate match score
        matches = sum(1 for symptom in input_symptoms if any(symptom in cs or cs in symptom for cs in condition_symptoms))
        score = matches / len(condition_symptoms) if condition_symptoms else 0

        if score > best_score and score > 0.3:  # Minimum 30% match
            best_score = score
            best_match = condition

    conn.close()

    if best_match:
        return {
            'disease': best_match['condition_name'],
            'ayurvedic': best_match['ayurvedic_remedy'],
            'medicine': best_match['medicine_suggestion'],
            'confidence': round(best_score * 100, 2),
            'severity': best_match['severity_level']
        }
    else:
        return {
            'disease': 'Unable to determine condition',
            'ayurvedic': 'Please consult an Ayurvedic practitioner for personalized treatment.',
            'medicine': 'Please consult a healthcare professional for proper diagnosis.',
            'confidence': 0,
            'severity': 'unknown'
        }

@app.route('/')
def index():
    """Serve the main HTML page"""
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medicino Web Portal</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f0f2f5;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: auto;
            background: #fff;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1, h2 {
            color: #1a73e8;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
        }
        textarea, input[type="text"] {
            width: 100%;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 6px;
            border: 1px solid #ddd;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            background-color: #1a73e8;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
        }
        button:hover {
            background-color: #155ab6;
        }
        .results {
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 5px solid #1a73e8;
        }
        .loader {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .confidence-score {
            background-color: #e8f5e8;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
        .severity {
            padding: 5px 10px;
            border-radius: 15px;
            color: white;
            font-weight: bold;
            display: inline-block;
            margin-top: 5px;
        }
        .severity.mild { background-color: #4caf50; }
        .severity.moderate { background-color: #ff9800; }
        .severity.severe { background-color: #f44336; }
        .medicine-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            background-color: #fafafa;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>💊 MEDICINO: A Smart Medical Assistant</h1>

        <section id="symptom-checker">
            <h2>AI-Powered Symptom Diagnosis</h2>
            <p>Enter your symptoms below for intelligent diagnosis and recommendations.</p>
            <textarea id="symptomsInput" rows="4" placeholder="e.g., fever, sore throat, headache, body ache"></textarea>
            <button id="diagnoseBtn">Diagnose Symptoms</button>
            <button id="voiceBtn">🎤 Use Voice Input</button>

            <div id="diagnosisLoader" class="loader">Analyzing symptoms...</div>

            <div id="diagnosisResult" class="results" style="display: none;">
                <h3>Diagnosis & Recommendations</h3>
                <p><strong>Possible Condition:</strong> <span id="diseaseOutput"></span></p>
                <div id="severityBadge"></div>
                <p><strong>Ayurvedic Remedy:</strong> <span id="ayurvedicOutput"></span></p>
                <p><strong>Medicine Suggestion:</strong> <span id="medicineOutput"></span></p>
                <div id="confidenceScore" class="confidence-score"></div>
            </div>
        </section>

        <hr style="margin: 30px 0;">

        <section id="medicine-info">
            <h2>Medicine Information Database</h2>
            <p>Enter the name of a medicine to get detailed information.</p>
            <input type="text" id="medicineInput" placeholder="e.g., Paracetamol, Ibuprofen">
            <button id="searchMedicineBtn">Search Medicine</button>

            <div id="medicineLoader" class="loader">Searching database...</div>

            <div id="medicineInfoResult" class="results" style="display: none;"></div>
        </section>
    </div>

    <script>
        const API_BASE = '';  // Since we're serving from the same domain

        document.addEventListener('DOMContentLoaded', () => {
            const diagnoseBtn = document.getElementById('diagnoseBtn');
            const symptomsInput = document.getElementById('symptomsInput');
            const diagnosisResult = document.getElementById('diagnosisResult');
            const diagnosisLoader = document.getElementById('diagnosisLoader');
            const searchMedicineBtn = document.getElementById('searchMedicineBtn');
            const medicineInput = document.getElementById('medicineInput');
            const medicineInfoResult = document.getElementById('medicineInfoResult');
            const medicineLoader = document.getElementById('medicineLoader');

            // Diagnosis functionality
            diagnoseBtn.addEventListener('click', async () => {
                const symptoms = symptomsInput.value.trim();
                if (!symptoms) {
                    alert("Please enter your symptoms.");
                    return;
                }

                diagnosisLoader.style.display = 'block';
                diagnosisResult.style.display = 'none';

                try {
                    const response = await fetch('/api/diagnose', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({symptoms: symptoms})
                    });

                    const result = await response.json();

                    diagnosisLoader.style.display = 'none';

                    if (result.success) {
                        document.getElementById('diseaseOutput').textContent = result.data.disease;
                        document.getElementById('ayurvedicOutput').textContent = result.data.ayurvedic;
                        document.getElementById('medicineOutput').textContent = result.data.medicine;

                        // Display confidence score
                        document.getElementById('confidenceScore').innerHTML =
                            `<strong>Confidence Score:</strong> ${result.data.confidence}% - This diagnosis is based on symptom matching analysis.`;

                        // Display severity badge
                        const severityBadge = document.getElementById('severityBadge');
                        if (result.data.severity !== 'unknown') {
                            severityBadge.innerHTML = `<span class="severity ${result.data.severity}">Severity: ${result.data.severity.toUpperCase()}</span>`;
                        }

                        diagnosisResult.style.display = 'block';
                    } else {
                        alert('Error: ' + result.message);
                    }
                } catch (error) {
                    diagnosisLoader.style.display = 'none';
                    alert('Network error occurred. Please try again.');
                }
            });

            // Medicine search functionality
            searchMedicineBtn.addEventListener('click', async () => {
                const medicineName = medicineInput.value.trim();
                if (!medicineName) {
                    alert("Please enter a medicine name.");
                    return;
                }

                medicineLoader.style.display = 'block';
                medicineInfoResult.style.display = 'none';

                try {
                    const response = await fetch(`/api/medicine/${encodeURIComponent(medicineName)}`);
                    const result = await response.json();

                    medicineLoader.style.display = 'none';

                    if (result.success && result.data) {
                        const medicine = result.data;
                        medicineInfoResult.innerHTML = `
                            <div class="medicine-card">
                                <h3>${medicine.name}</h3>
                                <p><strong>Description:</strong> ${medicine.description}</p>
                                <p><strong>Dosage:</strong> ${medicine.dosage}</p>
                                <p><strong>Side Effects:</strong> ${medicine.side_effects}</p>
                                <p><strong>Contraindications:</strong> ${medicine.contraindications}</p>
                                <p><strong>Price:</strong> ₹${medicine.price}</p>
                            </div>
                        `;
                        medicineInfoResult.style.display = 'block';
                    } else {
                        medicineInfoResult.innerHTML = `
                            <div class="medicine-card">
                                <h3>Medicine Not Found</h3>
                                <p>The medicine "${medicineName}" was not found in our database. Please check the spelling or try a different name.</p>
                            </div>
                        `;
                        medicineInfoResult.style.display = 'block';
                    }
                } catch (error) {
                    medicineLoader.style.display = 'none';
                    alert('Network error occurred. Please try again.');
                }
            });

            // Voice input placeholder
            document.getElementById('voiceBtn').addEventListener('click', () => {
                if ('webkitSpeechRecognition' in window) {
                    const recognition = new webkitSpeechRecognition();
                    recognition.continuous = false;
                    recognition.interimResults = false;
                    recognition.lang = 'en-US';

                    recognition.onstart = () => {
                        document.getElementById('voiceBtn').textContent = '🎤 Listening...';
                        document.getElementById('voiceBtn').disabled = true;
                    };

                    recognition.onresult = (event) => {
                        const transcript = event.results[0][0].transcript;
                        symptomsInput.value = transcript;
                    };

                    recognition.onend = () => {
                        document.getElementById('voiceBtn').textContent = '🎤 Use Voice Input';
                        document.getElementById('voiceBtn').disabled = false;
                    };

                    recognition.onerror = (event) => {
                        alert('Speech recognition error: ' + event.error);
                        document.getElementById('voiceBtn').textContent = '🎤 Use Voice Input';
                        document.getElementById('voiceBtn').disabled = false;
                    };

                    recognition.start();
                } else {
                    alert('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
                }
            });
        });
    </script>
</body>
</html>
    '''
    return render_template_string(html_content)

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """Diagnose symptoms API endpoint"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', '').strip()

        if not symptoms:
            return jsonify({'success': False, 'message': 'Symptoms are required'})

        # Perform diagnosis
        diagnosis_result = diagnose_symptoms(symptoms)

        # Save to history
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO diagnosis_history (symptoms, diagnosed_condition, ayurvedic_remedy, medicine_suggestion, confidence_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (symptoms, diagnosis_result['disease'], diagnosis_result['ayurvedic'],
              diagnosis_result['medicine'], diagnosis_result['confidence']))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'data': diagnosis_result})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/medicine/<medicine_name>')
def get_medicine_info(medicine_name):
    """Get medicine information API endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Search for medicine (case-insensitive)
        cursor.execute('''
            SELECT * FROM medicines
            WHERE LOWER(name) LIKE LOWER(?)
        ''', (f'%{medicine_name}%',))

        medicine = cursor.fetchone()
        conn.close()

        if medicine:
            medicine_data = dict(medicine)
            return jsonify({'success': True, 'data': medicine_data})
        else:
            return jsonify({'success': False, 'message': 'Medicine not found'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/medicines')
def list_medicines():
    """List all medicines API endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM medicines ORDER BY name')
        medicines = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({'success': True, 'data': medicines})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/history')
def get_diagnosis_history():
    """Get diagnosis history API endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM diagnosis_history
            ORDER BY created_at DESC
            LIMIT 50
        ''')
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify({'success': True, 'data': history})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    # Initialize database
    init_db()
    print("Database initialized successfully!")
    print("Starting Medicino Web Portal...")
    print("Available endpoints:")
    print("- GET  /                     - Main web interface")
    print("- POST /api/diagnose         - Symptom diagnosis")
    print("- GET  /api/medicine/<name>  - Medicine information")
    print("- GET  /api/medicines        - List all medicines")
    print("- GET  /api/history          - Diagnosis history")

    app.run(debug=True, host='0.0.0.0', port=5000)
