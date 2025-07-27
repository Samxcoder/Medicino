import sqlite3
import os

DATABASE = 'medicino.db'

def setup_database():
    """Setup the complete database with comprehensive data"""

    # Remove existing database if it exists
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print("Existing database removed.")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create medicines table
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

    # Create diagnosis_history table
    cursor.execute('''
        CREATE TABLE diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptoms TEXT NOT NULL,
            diagnosed_condition TEXT,
            ayurvedic_remedy TEXT,
            medicine_suggestion TEXT,
            confidence_score REAL,
            user_feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create symptoms_database table
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

    # Insert comprehensive medicine data
    medicines_data = [
        ('Paracetamol', 'Acetaminophen-based pain reliever and fever reducer', '500-1000mg every 4-6 hours (max 4g/day)', 'Nausea, rash, liver damage with overdose', 'Severe liver disease, alcohol dependency', 15.50, 'Analgesic'),
        ('Ibuprofen', 'NSAID anti-inflammatory pain reliever', '200-400mg every 4-6 hours', 'Stomach upset, headache, dizziness', 'Stomach ulcers, kidney disease, heart conditions', 22.00, 'NSAID'),
        ('Cetirizine', 'Second-generation antihistamine for allergies', '10mg once daily', 'Drowsiness, dry mouth, fatigue', 'Severe kidney disease, pregnancy', 18.75, 'Antihistamine'),
        ('Dolo 650', 'Paracetamol 650mg tablet for pain and fever', '1 tablet every 8 hours', 'Nausea, skin rash, stomach upset', 'Liver problems, alcohol abuse', 12.25, 'Analgesic'),
        ('Aspirin', 'Salicylate pain reliever and blood thinner', '75-300mg daily', 'Stomach irritation, bleeding, tinnitus', 'Bleeding disorders, asthma, children under 16', 8.50, 'Analgesic'),
        ('Amoxicillin', 'Penicillin-type antibiotic', '250-500mg every 8 hours', 'Diarrhea, nausea, skin rash', 'Penicillin allergy, severe kidney disease', 45.00, 'Antibiotic'),
        ('Omeprazole', 'Proton pump inhibitor for acid reflux', '20mg once daily before meals', 'Headache, nausea, diarrhea', 'Severe liver disease, osteoporosis risk', 32.75, 'PPI'),
        ('Diclofenac', 'NSAID for inflammation and pain', '50mg 2-3 times daily', 'Stomach upset, dizziness, headache', 'Heart disease, stomach ulcers, kidney problems', 28.50, 'NSAID'),
        ('Loratadine', 'Non-drowsy antihistamine', '10mg once daily', 'Headache, nervousness, fatigue', 'Severe liver disease', 25.00, 'Antihistamine'),
        ('Crocin', 'Paracetamol-based fever and pain reliever', '500mg every 6 hours', 'Rare: allergic reactions, liver toxicity', 'Liver disease, alcoholism', 10.75, 'Analgesic')
    ]

    cursor.executemany('''
        INSERT INTO medicines (name, description, dosage, side_effects, contraindications, price, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', medicines_data)

    # Insert comprehensive symptoms and conditions data
    conditions_data = [
        ('Common Cold', 'sneezing,runny nose,congestion,mild headache,watery eyes,sore throat',
         'Steam inhalation with eucalyptus oil. Drink herbal tea with tulsi and ginger. Consume honey with warm water.',
         'Cetirizine, Paracetamol', 'mild',
         'Upper respiratory tract viral infection causing nasal congestion and throat irritation.',
         'Rest, stay hydrated, avoid close contact with others'),

        ('Viral Fever', 'fever,body ache,headache,fatigue,chills,loss of appetite',
         'Drink hot water with ginger and turmeric. Take adequate rest and consume immunity-boosting kadha.',
         'Paracetamol, Dolo 650', 'moderate',
         'Fever caused by viral infection, usually self-limiting.',
         'Complete bed rest, increase fluid intake, monitor temperature'),

        ('Flu (Influenza)', 'high fever,severe headache,muscle pain,chills,fatigue,dry cough,sore throat',
         'Rest completely, increase fluid intake, consume kadha with immunity boosters like giloy and ashwagandha.',
         'Paracetamol, Ibuprofen', 'severe',
         'Highly contagious viral respiratory infection.',
         'Isolation, complete rest, medical attention if symptoms worsen'),

        ('Allergic Rhinitis', 'sneezing,itching,runny nose,watery eyes,nasal congestion',
         'Avoid allergens, use neem-based remedies, consume turmeric milk, practice pranayama.',
         'Cetirizine, Loratadine', 'mild',
         'Allergic reaction affecting nasal passages and eyes.',
         'Identify and avoid triggers, keep environment clean'),

        ('Tension Headache', 'head pain,pressure sensation,neck stiffness,mild nausea',
         'Apply peppermint oil to temples, practice meditation and yoga, ensure adequate sleep.',
         'Aspirin, Ibuprofen, Paracetamol', 'mild',
         'Most common type of headache caused by stress and tension.',
         'Stress management, regular sleep schedule, relaxation techniques'),

        ('Migraine', 'severe headache,nausea,vomiting,sensitivity to light and sound,visual disturbances',
         'Rest in dark quiet room, apply cold compress, practice deep breathing exercises, avoid trigger foods.',
         'Aspirin, specialized migraine medication', 'severe',
         'Neurological condition causing severe recurring headaches.',
         'Identify triggers, maintain regular meals and sleep, seek medical help'),

        ('Gastritis', 'stomach pain,nausea,vomiting,bloating,loss of appetite,heartburn',
         'Consume buttermilk, avoid spicy and oily food, drink fresh ginger tea, eat small frequent meals.',
         'Omeprazole, Antacids', 'moderate',
         'Inflammation of stomach lining causing digestive discomfort.',
         'Avoid NSAIDs, alcohol, spicy foods, eat regular meals'),

        ('Food Poisoning', 'nausea,vomiting,diarrhea,stomach cramps,fever,weakness',
         'Stay hydrated with ORS, consume yogurt and buttermilk, avoid solid food initially.',
         'ORS, Probiotics, Paracetamol for fever', 'moderate',
         'Illness caused by consuming contaminated food or water.',
         'Stay hydrated, rest, seek medical help if severe'),

        ('Hypertension', 'headache,dizziness,chest pain,shortness of breath,nosebleeds',
         'Practice yoga and meditation, consume garlic and amla, reduce salt intake, maintain healthy weight.',
         'Consult doctor for prescription medication', 'severe',
         'High blood pressure that can lead to serious complications.',
         'Regular monitoring, lifestyle changes, medication compliance'),

        ('Anxiety', 'restlessness,rapid heartbeat,sweating,nervousness,difficulty concentrating',
         'Practice deep breathing, meditation, consume ashwagandha tea, maintain regular exercise routine.',
         'Consult mental health professional', 'moderate',
         'Mental health condition causing excessive worry and fear.',
         'Stress management, regular exercise, adequate sleep, professional help'),

        ('Insomnia', 'difficulty falling asleep,frequent awakening,daytime fatigue,irritability',
         'Practice yoga nidra, consume warm milk with turmeric, maintain sleep hygiene, avoid screens before bed.',
         'Melatonin supplements (consult doctor)', 'moderate',
         'Sleep disorder affecting ability to fall or stay asleep.',
         'Sleep hygiene, regular schedule, relaxation techniques'),

        ('Acid Reflux', 'heartburn,chest pain,regurgitation,difficulty swallowing,chronic cough',
         'Avoid spicy and acidic foods, consume coconut water, practice pranayama, eat smaller meals.',
         'Omeprazole, Antacids', 'moderate',
         'Stomach acid backing up into the esophagus.',
         'Dietary changes, weight management, avoid lying down after meals'),

        ('Sinusitis', 'facial pain,nasal congestion,headache,thick nasal discharge,reduced smell',
         'Steam inhalation with eucalyptus, neti pot with saline, consume turmeric and ginger tea.',
         'Decongestants, Ibuprofen', 'moderate',
         'Inflammation of sinus cavities causing facial pain and congestion.',
         'Keep nasal passages moist, avoid allergens, stay hydrated'),

        ('Bronchitis', 'persistent cough,mucus production,chest discomfort,fatigue,mild fever',
         'Steam inhalation, consume honey and ginger, practice breathing exercises, rest adequately.',
         'Cough suppressants, Paracetamol', 'moderate',
         'Inflammation of bronchial tubes causing persistent cough.',
         'Rest, stay hydrated, avoid smoking and pollutants'),

        ('Urinary Tract Infection', 'burning sensation during urination,frequent urination,cloudy urine,pelvic pain',
         'Increase water intake, consume cranberry juice, practice good hygiene, avoid holding urine.',
         'Antibiotics (Amoxicillin - consult doctor)', 'moderate',
         'Bacterial infection affecting urinary system.',
         'Stay hydrated, proper hygiene, complete antibiotic course')
    ]

    cursor.executemany('''
        INSERT INTO symptoms_database (condition_name, symptoms, ayurvedic_remedy, medicine_suggestion, severity_level, description, precautions)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', conditions_data)

    print("Database setup completed successfully!")
    print(f"Inserted {len(medicines_data)} medicines")
    print(f"Inserted {len(conditions_data)} medical conditions")

    # Display some statistics
    cursor.execute("SELECT COUNT(*) FROM medicines")
    medicine_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM symptoms_database")
    condition_count = cursor.fetchone()[0]

    print(f"\nDatabase Statistics:")
    print(f"Total Medicines: {medicine_count}")
    print(f"Total Medical Conditions: {condition_count}")

    # Display sample data
    print(f"\nSample Medicines:")
    cursor.execute("SELECT name, category, price FROM medicines LIMIT 5")
    for row in cursor.fetchall():
        print(f"- {row[0]} ({row[1]}) - ₹{row[2]}")

    print(f"\nSample Conditions:")
    cursor.execute("SELECT condition_name, severity_level FROM symptoms_database LIMIT 5")
    for row in cursor.fetchall():
        print(f"- {row[0]} (Severity: {row[1]})")

    conn.commit()
    conn.close()
    print(f"\nDatabase '{DATABASE}' created successfully!")

if __name__ == "__main__":
    setup_database()
