#!/usr/bin/env python3
"""
Comprehensive Database Setup for Medicino
This script populates the database with extensive medical data including:
- Symptoms and conditions with Ayurvedic remedies
- Medicine database with detailed information
- Comprehensive symptom mappings
"""

import sqlite3
import os
from datetime import datetime

DATABASE = 'medicino.db'

def create_database():
    """Create and populate the database with comprehensive medical data."""
    
    # Remove existing database if it exists
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print("Removed existing database.")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create tables
    print("Creating database tables...")
    
    # Users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Medicines table
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
    
    # Diagnosis history table
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
    
    # Symptoms database table
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
    
    print("Tables created successfully!")
    
    # Populate symptoms database with comprehensive data
    print("Populating symptoms database...")
    
    symptoms_data = [
        # Respiratory Conditions
        {
            'condition_name': 'Common Cold',
            'symptoms': 'runny nose, sneezing, sore throat, cough, congestion, mild fever, fatigue',
            'ayurvedic_remedy': 'Tulsi tea, ginger tea, honey with warm water, steam inhalation with eucalyptus oil',
            'medicine_suggestion': 'Paracetamol, Vitamin C supplements, Decongestants',
            'severity_level': 'mild',
            'description': 'A viral infection affecting the upper respiratory tract',
            'precautions': 'Rest, stay hydrated, avoid cold foods, maintain good hygiene'
        },
        {
            'condition_name': 'Bronchitis',
            'symptoms': 'persistent cough, chest discomfort, wheezing, shortness of breath, fatigue, mild fever',
            'ayurvedic_remedy': 'Vasaka leaf decoction, Sitopaladi churna, Kantakari tea',
            'medicine_suggestion': 'Bronchodilators, Expectorants, Antibiotics if bacterial',
            'severity_level': 'moderate',
            'description': 'Inflammation of the bronchial tubes causing cough and breathing difficulties',
            'precautions': 'Avoid smoking, stay hydrated, use humidifier, rest'
        },
        {
            'condition_name': 'Pneumonia',
            'symptoms': 'high fever, severe cough, chest pain, difficulty breathing, fatigue, loss of appetite',
            'ayurvedic_remedy': 'Kanakasava, Vasavaleha, Sitopaladi churna',
            'medicine_suggestion': 'Antibiotics, Oxygen therapy, Hospitalization if severe',
            'severity_level': 'severe',
            'description': 'Serious lung infection requiring immediate medical attention',
            'precautions': 'Seek immediate medical care, complete antibiotic course, rest'
        },
        
        # Digestive Conditions
        {
            'condition_name': 'Gastritis',
            'symptoms': 'stomach pain, nausea, vomiting, loss of appetite, bloating, heartburn',
            'ayurvedic_remedy': 'Amla powder, Licorice root, Ginger tea, Aloe vera juice',
            'medicine_suggestion': 'Antacids, Proton pump inhibitors, H2 blockers',
            'severity_level': 'moderate',
            'description': 'Inflammation of the stomach lining causing digestive discomfort',
            'precautions': 'Avoid spicy foods, eat smaller meals, avoid alcohol and smoking'
        },
        {
            'condition_name': 'Food Poisoning',
            'symptoms': 'nausea, vomiting, diarrhea, stomach cramps, fever, dehydration',
            'ayurvedic_remedy': 'Ginger tea, Cumin water, Coriander seeds, ORS solution',
            'medicine_suggestion': 'Oral rehydration solution, Anti-emetics, Anti-diarrheals',
            'severity_level': 'moderate',
            'description': 'Illness caused by consuming contaminated food or water',
            'precautions': 'Stay hydrated, rest, avoid solid foods initially, seek medical care if severe'
        },
        {
            'condition_name': 'Irritable Bowel Syndrome',
            'symptoms': 'abdominal pain, bloating, diarrhea, constipation, gas, mucus in stool',
            'ayurvedic_remedy': 'Triphala churna, Isabgol, Hing, Jeera water',
            'medicine_suggestion': 'Fiber supplements, Anti-spasmodics, Probiotics',
            'severity_level': 'moderate',
            'description': 'Chronic digestive disorder affecting the large intestine',
            'precautions': 'Identify trigger foods, manage stress, regular exercise, fiber-rich diet'
        },
        
        # Cardiovascular Conditions
        {
            'condition_name': 'Hypertension',
            'symptoms': 'headache, dizziness, chest pain, shortness of breath, vision problems, fatigue',
            'ayurvedic_remedy': 'Arjuna bark powder, Sarpagandha, Jatamansi, Garlic',
            'medicine_suggestion': 'ACE inhibitors, Beta blockers, Calcium channel blockers',
            'severity_level': 'severe',
            'description': 'High blood pressure requiring medical management',
            'precautions': 'Regular monitoring, low-salt diet, exercise, stress management'
        },
        {
            'condition_name': 'Angina',
            'symptoms': 'chest pain, pressure in chest, pain radiating to arms, shortness of breath, fatigue',
            'ayurvedic_remedy': 'Arjuna bark, Guggulu, Pushkarmool, Garlic',
            'medicine_suggestion': 'Nitroglycerin, Beta blockers, Calcium channel blockers',
            'severity_level': 'severe',
            'description': 'Chest pain due to reduced blood flow to heart',
            'precautions': 'Immediate medical attention, avoid strenuous activity, quit smoking'
        },
        
        # Neurological Conditions
        {
            'condition_name': 'Migraine',
            'symptoms': 'severe headache, nausea, vomiting, sensitivity to light, aura, dizziness',
            'ayurvedic_remedy': 'Brahmi, Shankhpushpi, Jatamansi, Ginger tea',
            'medicine_suggestion': 'Triptans, NSAIDs, Anti-emetics, Preventive medications',
            'severity_level': 'moderate',
            'description': 'Recurrent severe headaches often with visual disturbances',
            'precautions': 'Identify triggers, maintain regular sleep, avoid stress, stay hydrated'
        },
        {
            'condition_name': 'Tension Headache',
            'symptoms': 'mild to moderate headache, pressure around head, neck pain, stress',
            'ayurvedic_remedy': 'Brahmi, Shankhpushpi, Lavender oil, Peppermint oil',
            'medicine_suggestion': 'Paracetamol, Ibuprofen, Muscle relaxants',
            'severity_level': 'mild',
            'description': 'Common headache caused by stress and muscle tension',
            'precautions': 'Stress management, regular breaks, good posture, relaxation techniques'
        },
        
        # Musculoskeletal Conditions
        {
            'condition_name': 'Arthritis',
            'symptoms': 'joint pain, stiffness, swelling, reduced range of motion, fatigue',
            'ayurvedic_remedy': 'Guggulu, Shallaki, Ashwagandha, Turmeric with milk',
            'medicine_suggestion': 'NSAIDs, DMARDs, Physical therapy, Joint supplements',
            'severity_level': 'moderate',
            'description': 'Inflammation of joints causing pain and stiffness',
            'precautions': 'Regular exercise, weight management, joint protection, balanced diet'
        },
        {
            'condition_name': 'Back Pain',
            'symptoms': 'lower back pain, stiffness, muscle spasms, radiating pain, difficulty moving',
            'ayurvedic_remedy': 'Ashwagandha, Guggulu, Shallaki, Sesame oil massage',
            'medicine_suggestion': 'NSAIDs, Muscle relaxants, Physical therapy, Heat/cold therapy',
            'severity_level': 'moderate',
            'description': 'Common condition affecting the lower back muscles and spine',
            'precautions': 'Good posture, regular exercise, proper lifting techniques, ergonomic setup'
        },
        
        # Skin Conditions
        {
            'condition_name': 'Eczema',
            'symptoms': 'itchy skin, red patches, dry skin, inflammation, scaling, oozing',
            'ayurvedic_remedy': 'Neem paste, Turmeric paste, Coconut oil, Aloe vera gel',
            'medicine_suggestion': 'Topical corticosteroids, Moisturizers, Antihistamines',
            'severity_level': 'moderate',
            'description': 'Chronic skin condition causing inflammation and itching',
            'precautions': 'Avoid triggers, moisturize regularly, gentle skin care, stress management'
        },
        {
            'condition_name': 'Acne',
            'symptoms': 'pimples, blackheads, whiteheads, inflammation, scarring, oily skin',
            'ayurvedic_remedy': 'Neem paste, Turmeric paste, Aloe vera, Sandalwood paste',
            'medicine_suggestion': 'Benzoyl peroxide, Salicylic acid, Retinoids, Antibiotics',
            'severity_level': 'mild',
            'description': 'Common skin condition affecting hair follicles and oil glands',
            'precautions': 'Gentle cleansing, avoid touching face, healthy diet, stress management'
        },
        
        # Endocrine Conditions
        {
            'condition_name': 'Diabetes',
            'symptoms': 'increased thirst, frequent urination, fatigue, blurred vision, slow healing',
            'ayurvedic_remedy': 'Gudmar, Jamun seeds, Bitter gourd, Fenugreek seeds',
            'medicine_suggestion': 'Metformin, Insulin, Sulfonylureas, DPP-4 inhibitors',
            'severity_level': 'severe',
            'description': 'Chronic condition affecting blood sugar regulation',
            'precautions': 'Regular monitoring, balanced diet, exercise, medication compliance'
        },
        {
            'condition_name': 'Thyroid Disorder',
            'symptoms': 'fatigue, weight changes, mood swings, hair loss, temperature sensitivity',
            'ayurvedic_remedy': 'Ashwagandha, Kanchanara, Guggulu, Brahmi',
            'medicine_suggestion': 'Levothyroxine, Anti-thyroid medications, Regular monitoring',
            'severity_level': 'moderate',
            'description': 'Disorder affecting thyroid hormone production',
            'precautions': 'Regular check-ups, medication compliance, balanced diet, stress management'
        },
        
        # Mental Health Conditions
        {
            'condition_name': 'Anxiety',
            'symptoms': 'excessive worry, restlessness, difficulty concentrating, sleep problems, panic attacks',
            'ayurvedic_remedy': 'Brahmi, Jatamansi, Shankhpushpi, Ashwagandha',
            'medicine_suggestion': 'SSRIs, Benzodiazepines, Cognitive behavioral therapy',
            'severity_level': 'moderate',
            'description': 'Mental health condition characterized by excessive worry and fear',
            'precautions': 'Stress management, regular exercise, therapy, medication compliance'
        },
        {
            'condition_name': 'Depression',
            'symptoms': 'persistent sadness, loss of interest, fatigue, sleep changes, appetite changes',
            'ayurvedic_remedy': 'Ashwagandha, Brahmi, Jatamansi, Saffron',
            'medicine_suggestion': 'SSRIs, SNRIs, Psychotherapy, Lifestyle changes',
            'severity_level': 'severe',
            'description': 'Serious mental health condition requiring professional treatment',
            'precautions': 'Seek professional help, maintain routine, social support, medication compliance'
        },
        
        # Eye Conditions
        {
            'condition_name': 'Conjunctivitis',
            'symptoms': 'red eyes, itching, discharge, swelling, sensitivity to light, blurred vision',
            'ayurvedic_remedy': 'Rose water, Honey drops, Triphala eyewash, Coriander water',
            'medicine_suggestion': 'Antibiotic eye drops, Antihistamines, Artificial tears',
            'severity_level': 'mild',
            'description': 'Inflammation of the conjunctiva causing eye irritation',
            'precautions': 'Good hygiene, avoid touching eyes, separate towels, seek medical care'
        },
        
        # Ear Conditions
        {
            'condition_name': 'Ear Infection',
            'symptoms': 'ear pain, hearing loss, fever, drainage, dizziness, pressure in ear',
            'ayurvedic_remedy': 'Garlic oil, Onion juice, Warm compress, Tulsi drops',
            'medicine_suggestion': 'Antibiotics, Pain relievers, Ear drops, Decongestants',
            'severity_level': 'moderate',
            'description': 'Infection of the middle ear requiring medical treatment',
            'precautions': 'Seek medical care, avoid water in ears, complete antibiotic course'
        },
        
        # Urinary Conditions
        {
            'condition_name': 'Urinary Tract Infection',
            'symptoms': 'frequent urination, burning sensation, cloudy urine, pelvic pain, fever',
            'ayurvedic_remedy': 'Cranberry juice, Coriander seeds, Barley water, Coconut water',
            'medicine_suggestion': 'Antibiotics, Increased fluid intake, Pain relievers',
            'severity_level': 'moderate',
            'description': 'Infection of the urinary system requiring antibiotic treatment',
            'precautions': 'Stay hydrated, good hygiene, complete antibiotic course, seek medical care'
        }
    ]
    
    cursor.executemany('''
        INSERT INTO symptoms_database (condition_name, symptoms, ayurvedic_remedy, medicine_suggestion, severity_level, description, precautions)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [(item['condition_name'], item['symptoms'], item['ayurvedic_remedy'], 
           item['medicine_suggestion'], item['severity_level'], item['description'], item['precautions']) 
          for item in symptoms_data])
    
    print(f"Added {len(symptoms_data)} conditions to symptoms database")
    
    # Populate medicines database with comprehensive data
    print("Populating medicines database...")
    
    medicines_data = [
        # Pain Relief
        {
            'name': 'Paracetamol',
            'description': 'Over-the-counter pain reliever and fever reducer',
            'dosage': '500-1000mg every 4-6 hours, max 4000mg/day',
            'side_effects': 'Nausea, stomach upset, liver damage in high doses',
            'contraindications': 'Liver disease, alcohol dependence, pregnancy (consult doctor)',
            'price': 5.99,
            'category': 'Pain Relief'
        },
        {
            'name': 'Ibuprofen',
            'description': 'Non-steroidal anti-inflammatory drug for pain and inflammation',
            'dosage': '200-400mg every 4-6 hours, max 1200mg/day',
            'side_effects': 'Stomach upset, heartburn, increased bleeding risk',
            'contraindications': 'Stomach ulcers, heart disease, kidney problems',
            'price': 7.99,
            'category': 'Pain Relief'
        },
        {
            'name': 'Aspirin',
            'description': 'Pain reliever and blood thinner',
            'dosage': '325-650mg every 4-6 hours',
            'side_effects': 'Stomach irritation, bleeding risk, ringing in ears',
            'contraindications': 'Bleeding disorders, stomach ulcers, children under 12',
            'price': 4.99,
            'category': 'Pain Relief'
        },
        
        # Respiratory
        {
            'name': 'Salbutamol',
            'description': 'Bronchodilator for asthma and breathing difficulties',
            'dosage': '2 puffs every 4-6 hours as needed',
            'side_effects': 'Tremors, increased heart rate, nervousness',
            'contraindications': 'Severe heart disease, uncontrolled arrhythmias',
            'price': 15.99,
            'category': 'Respiratory'
        },
        {
            'name': 'Amoxicillin',
            'description': 'Antibiotic for bacterial infections',
            'dosage': '250-500mg three times daily for 7-10 days',
            'side_effects': 'Diarrhea, nausea, allergic reactions',
            'contraindications': 'Penicillin allergy, mononucleosis',
            'price': 12.99,
            'category': 'Antibiotics'
        },
        
        # Digestive
        {
            'name': 'Omeprazole',
            'description': 'Proton pump inhibitor for acid reflux and ulcers',
            'dosage': '20-40mg once daily before breakfast',
            'side_effects': 'Headache, diarrhea, vitamin B12 deficiency',
            'contraindications': 'Liver disease, pregnancy, long-term use',
            'price': 18.99,
            'category': 'Digestive'
        },
        {
            'name': 'Metformin',
            'description': 'Oral diabetes medication to control blood sugar',
            'dosage': '500-2000mg daily in divided doses',
            'side_effects': 'Nausea, diarrhea, lactic acidosis (rare)',
            'contraindications': 'Severe kidney disease, heart failure',
            'price': 25.99,
            'category': 'Diabetes'
        },
        
        # Cardiovascular
        {
            'name': 'Amlodipine',
            'description': 'Calcium channel blocker for high blood pressure',
            'dosage': '5-10mg once daily',
            'side_effects': 'Swelling in ankles, dizziness, flushing',
            'contraindications': 'Severe heart failure, aortic stenosis',
            'price': 22.99,
            'category': 'Cardiovascular'
        },
        {
            'name': 'Atorvastatin',
            'description': 'Statin medication to lower cholesterol',
            'dosage': '10-80mg once daily',
            'side_effects': 'Muscle pain, liver problems, diabetes risk',
            'contraindications': 'Liver disease, pregnancy, active liver disease',
            'price': 28.99,
            'category': 'Cardiovascular'
        },
        
        # Mental Health
        {
            'name': 'Sertraline',
            'description': 'SSRI antidepressant for depression and anxiety',
            'dosage': '50-200mg once daily',
            'side_effects': 'Nausea, insomnia, sexual dysfunction',
            'contraindications': 'MAOI use, bipolar disorder, pregnancy',
            'price': 35.99,
            'category': 'Mental Health'
        },
        {
            'name': 'Alprazolam',
            'description': 'Benzodiazepine for anxiety and panic disorders',
            'dosage': '0.25-1mg three times daily',
            'side_effects': 'Drowsiness, dependence, memory problems',
            'contraindications': 'Respiratory depression, pregnancy, alcohol use',
            'price': 32.99,
            'category': 'Mental Health'
        },
        
        # Skin
        {
            'name': 'Hydrocortisone',
            'description': 'Topical corticosteroid for skin inflammation',
            'dosage': 'Apply 1-2 times daily to affected area',
            'side_effects': 'Skin thinning, stretch marks, local irritation',
            'contraindications': 'Fungal infections, open wounds, face use',
            'price': 8.99,
            'category': 'Dermatology'
        },
        {
            'name': 'Benzoyl Peroxide',
            'description': 'Topical medication for acne treatment',
            'dosage': 'Apply 1-2 times daily to affected areas',
            'side_effects': 'Skin irritation, dryness, bleaching of clothes',
            'contraindications': 'Sensitive skin, pregnancy, breastfeeding',
            'price': 9.99,
            'category': 'Dermatology'
        },
        
        # Vitamins and Supplements
        {
            'name': 'Vitamin D3',
            'description': 'Essential vitamin for bone health and immune function',
            'dosage': '1000-4000 IU daily',
            'side_effects': 'Nausea, kidney stones (high doses)',
            'contraindications': 'Hypercalcemia, kidney disease',
            'price': 14.99,
            'category': 'Vitamins'
        },
        {
            'name': 'Omega-3 Fish Oil',
            'description': 'Essential fatty acids for heart and brain health',
            'dosage': '1000-2000mg daily',
            'side_effects': 'Fishy burps, diarrhea, bleeding risk',
            'contraindications': 'Bleeding disorders, fish allergies',
            'price': 19.99,
            'category': 'Supplements'
        },
        {
            'name': 'Probiotics',
            'description': 'Beneficial bacteria for gut health',
            'dosage': '1-2 capsules daily with meals',
            'side_effects': 'Mild bloating, gas, diarrhea initially',
            'contraindications': 'Severe immune deficiency, acute pancreatitis',
            'price': 16.99,
            'category': 'Supplements'
        },
        
        # Sleep and Relaxation
        {
            'name': 'Melatonin',
            'description': 'Natural sleep hormone for insomnia',
            'dosage': '1-5mg 30 minutes before bedtime',
            'side_effects': 'Drowsiness, vivid dreams, morning grogginess',
            'contraindications': 'Pregnancy, autoimmune disorders',
            'price': 11.99,
            'category': 'Sleep'
        },
        {
            'name': 'Valerian Root',
            'description': 'Natural herb for sleep and anxiety',
            'dosage': '300-600mg 30 minutes before bedtime',
            'side_effects': 'Drowsiness, vivid dreams, liver problems',
            'contraindications': 'Liver disease, pregnancy, driving',
            'price': 13.99,
            'category': 'Natural Remedies'
        },
        
        # Cough and Cold
        {
            'name': 'Dextromethorphan',
            'description': 'Cough suppressant for dry cough',
            'dosage': '15-30mg every 4-6 hours',
            'side_effects': 'Drowsiness, dizziness, nausea',
            'contraindications': 'MAOI use, chronic cough, asthma',
            'price': 6.99,
            'category': 'Cough & Cold'
        },
        {
            'name': 'Guaifenesin',
            'description': 'Expectorant to loosen chest congestion',
            'dosage': '200-400mg every 4 hours',
            'side_effects': 'Nausea, vomiting, dizziness',
            'contraindications': 'Severe kidney disease, pregnancy',
            'price': 7.99,
            'category': 'Cough & Cold'
        },
        
        # Allergy
        {
            'name': 'Cetirizine',
            'description': 'Antihistamine for allergy relief',
            'dosage': '10mg once daily',
            'side_effects': 'Drowsiness, dry mouth, headache',
            'contraindications': 'Kidney disease, pregnancy, driving',
            'price': 10.99,
            'category': 'Allergy'
        },
        {
            'name': 'Loratadine',
            'description': 'Non-drowsy antihistamine for allergies',
            'dosage': '10mg once daily',
            'side_effects': 'Headache, dry mouth, fatigue',
            'contraindications': 'Liver disease, pregnancy, children under 2',
            'price': 12.99,
            'category': 'Allergy'
        },
        
        # Women's Health
        {
            'name': 'Folic Acid',
            'description': 'Essential B vitamin for pregnancy and cell growth',
            'dosage': '400-800mcg daily',
            'side_effects': 'Nausea, bitter taste, allergic reactions',
            'contraindications': 'Vitamin B12 deficiency, cancer',
            'price': 8.99,
            'category': 'Women\'s Health'
        },
        {
            'name': 'Iron Supplement',
            'description': 'Mineral supplement for iron deficiency anemia',
            'dosage': '65-200mg daily with vitamin C',
            'side_effects': 'Constipation, black stools, stomach upset',
            'contraindications': 'Hemochromatosis, thalassemia',
            'price': 11.99,
            'category': 'Supplements'
        },
        
        # Men's Health
        {
            'name': 'Saw Palmetto',
            'description': 'Natural supplement for prostate health',
            'dosage': '160-320mg daily',
            'side_effects': 'Stomach upset, headache, decreased libido',
            'contraindications': 'Pregnancy, hormone-sensitive conditions',
            'price': 17.99,
            'category': 'Men\'s Health'
        },
        
        # Eye Health
        {
            'name': 'Lutein',
            'description': 'Carotenoid for eye health and macular degeneration',
            'dosage': '10-20mg daily',
            'side_effects': 'Yellow skin discoloration, stomach upset',
            'contraindications': 'Pregnancy, breastfeeding',
            'price': 15.99,
            'category': 'Eye Health'
        },
        
        # Bone Health
        {
            'name': 'Calcium Carbonate',
            'description': 'Mineral supplement for bone health',
            'dosage': '500-1000mg daily with vitamin D',
            'side_effects': 'Constipation, gas, kidney stones',
            'contraindications': 'Hypercalcemia, kidney stones',
            'price': 9.99,
            'category': 'Bone Health'
        },
        {
            'name': 'Glucosamine',
            'description': 'Natural compound for joint health and arthritis',
            'dosage': '1500mg daily',
            'side_effects': 'Stomach upset, headache, allergic reactions',
            'contraindications': 'Shellfish allergy, diabetes, pregnancy',
            'price': 21.99,
            'category': 'Joint Health'
        }
    ]
    
    cursor.executemany('''
        INSERT INTO medicines (name, description, dosage, side_effects, contraindications, price, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [(item['name'], item['description'], item['dosage'], item['side_effects'],
           item['contraindications'], item['price'], item['category']) 
          for item in medicines_data])
    
    print(f"Added {len(medicines_data)} medicines to database")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("\n🎉 Database setup completed successfully!")
    print(f"📊 Database contains:")
    print(f"   • {len(symptoms_data)} medical conditions with symptoms")
    print(f"   • {len(medicines_data)} medicines with detailed information")
    print(f"   • Comprehensive Ayurvedic remedies")
    print(f"   • Severity levels and precautions")
    print(f"   • Price information and categories")
    
    print("\n🔧 Next Steps:")
    print("1. Run 'python app.py' to start the application")
    print("2. Register a new account")
    print("3. Test the symptom diagnosis with various conditions")
    print("4. Explore the medicine database")
    print("5. Check diagnosis history functionality")

if __name__ == '__main__':
    create_database()
