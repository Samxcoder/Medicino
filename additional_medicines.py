# Additional 200 medicines to add to the database

additional_medicines = [
    # Cardiovascular Medicines
    {
        'name': 'Losartan',
        'description': 'Angiotensin II receptor blocker for hypertension and heart failure',
        'dosage': '25-100mg once daily',
        'side_effects': 'Dizziness, fatigue, cough, hyperkalemia',
        'contraindications': 'Pregnancy, severe liver disease, bilateral renal artery stenosis',
        'price': 16.50,
        'category': 'Cardiovascular'
    },
    {
        'name': 'Carvedilol',
        'description': 'Beta-blocker with alpha-blocking activity for heart failure and hypertension',
        'dosage': '6.25-25mg twice daily',
        'side_effects': 'Dizziness, fatigue, bradycardia, orthostatic hypotension',
        'contraindications': 'Severe heart failure, asthma, heart block',
        'price': 21.75,
        'category': 'Cardiovascular'
    },
    {
        'name': 'Valsartan',
        'description': 'Angiotensin II receptor blocker for hypertension and heart failure',
        'dosage': '80-320mg once daily',
        'side_effects': 'Dizziness, headache, fatigue, hyperkalemia',
        'contraindications': 'Pregnancy, severe liver disease, bilateral renal artery stenosis',
        'price': 18.90,
        'category': 'Cardiovascular'
    },
    {
        'name': 'Metoprolol',
        'description': 'Beta-blocker for hypertension, angina, and heart failure',
        'dosage': '25-200mg twice daily',
        'side_effects': 'Fatigue, dizziness, bradycardia, cold extremities',
        'contraindications': 'Severe bradycardia, heart block, cardiogenic shock',
        'price': 14.25,
        'category': 'Cardiovascular'
    },
    {
        'name': 'Simvastatin',
        'description': 'HMG-CoA reductase inhibitor to lower cholesterol',
        'dosage': '10-80mg once daily in the evening',
        'side_effects': 'Muscle pain, liver problems, diabetes risk, memory issues',
        'contraindications': 'Liver disease, pregnancy, active liver disease',
        'price': 12.80,
        'category': 'Cardiovascular'
    },
    {
        'name': 'Rosuvastatin',
        'description': 'HMG-CoA reductase inhibitor for cholesterol management',
        'dosage': '5-40mg once daily',
        'side_effects': 'Muscle pain, liver problems, diabetes risk, headache',
        'contraindications': 'Liver disease, pregnancy, Asian descent (lower doses)',
        'price': 24.60,
        'category': 'Cardiovascular'
    },
    {
        'name': 'Pravastatin',
        'description': 'HMG-CoA reductase inhibitor for cholesterol reduction',
        'dosage': '10-80mg once daily',
        'side_effects': 'Muscle pain, liver problems, headache, nausea',
        'contraindications': 'Liver disease, pregnancy, active liver disease',
        'price': 19.40,
        'category': 'Cardiovascular'
    },
    {
        'name': 'Nifedipine',
        'description': 'Calcium channel blocker for hypertension and angina',
        'dosage': '30-90mg daily in divided doses',
        'side_effects': 'Headache, flushing, ankle swelling, dizziness',
        'contraindications': 'Severe aortic stenosis, cardiogenic shock',
        'price': 11.75,
        'category': 'Cardiovascular'
    },
    {
        'name': 'Diltiazem',
        'description': 'Calcium channel blocker for hypertension and angina',
        'dosage': '120-360mg daily in divided doses',
        'side_effects': 'Headache, dizziness, bradycardia, constipation',
        'contraindications': 'Severe heart failure, heart block, sick sinus syndrome',
        'price': 15.90,
        'category': 'Cardiovascular'
    },
    {
        'name': 'Verapamil',
        'description': 'Calcium channel blocker for hypertension and arrhythmias',
        'dosage': '80-480mg daily in divided doses',
        'side_effects': 'Constipation, headache, dizziness, bradycardia',
        'contraindications': 'Severe heart failure, heart block, sick sinus syndrome',
        'price': 13.45,
        'category': 'Cardiovascular'
    },
    
    # Diabetes Medicines
    {
        'name': 'Glimepiride',
        'description': 'Sulfonylurea for type 2 diabetes management',
        'dosage': '1-8mg once daily with breakfast',
        'side_effects': 'Hypoglycemia, weight gain, nausea, skin reactions',
        'contraindications': 'Type 1 diabetes, diabetic ketoacidosis, severe liver disease',
        'price': 8.75,
        'category': 'Diabetes'
    },
    {
        'name': 'Gliclazide',
        'description': 'Sulfonylurea for type 2 diabetes control',
        'dosage': '40-320mg daily in divided doses',
        'side_effects': 'Hypoglycemia, weight gain, gastrointestinal upset',
        'contraindications': 'Type 1 diabetes, diabetic ketoacidosis, severe liver disease',
        'price': 7.90,
        'category': 'Diabetes'
    },
    {
        'name': 'Sitagliptin',
        'description': 'DPP-4 inhibitor for type 2 diabetes management',
        'dosage': '100mg once daily',
        'side_effects': 'Upper respiratory infection, headache, pancreatitis',
        'contraindications': 'Type 1 diabetes, diabetic ketoacidosis, severe kidney disease',
        'price': 45.20,
        'category': 'Diabetes'
    },
    {
        'name': 'Empagliflozin',
        'description': 'SGLT2 inhibitor for type 2 diabetes and heart failure',
        'dosage': '10-25mg once daily',
        'side_effects': 'Urinary tract infections, dehydration, ketoacidosis',
        'contraindications': 'Type 1 diabetes, severe kidney disease, dialysis',
        'price': 52.80,
        'category': 'Diabetes'
    },
    {
        'name': 'Dapagliflozin',
        'description': 'SGLT2 inhibitor for type 2 diabetes management',
        'dosage': '5-10mg once daily',
        'side_effects': 'Urinary tract infections, dehydration, ketoacidosis',
        'contraindications': 'Type 1 diabetes, severe kidney disease, dialysis',
        'price': 48.90,
        'category': 'Diabetes'
    },
    {
        'name': 'Pioglitazone',
        'description': 'Thiazolidinedione for type 2 diabetes management',
        'dosage': '15-45mg once daily',
        'side_effects': 'Weight gain, fluid retention, heart failure risk',
        'contraindications': 'Heart failure, liver disease, bladder cancer',
        'price': 28.75,
        'category': 'Diabetes'
    },
    {
        'name': 'Acarbose',
        'description': 'Alpha-glucosidase inhibitor for type 2 diabetes',
        'dosage': '25-100mg three times daily with meals',
        'side_effects': 'Flatulence, diarrhea, abdominal pain',
        'contraindications': 'Inflammatory bowel disease, intestinal obstruction',
        'price': 22.40,
        'category': 'Diabetes'
    },
    {
        'name': 'Repaglinide',
        'description': 'Meglitinide for type 2 diabetes management',
        'dosage': '0.5-4mg before each meal',
        'side_effects': 'Hypoglycemia, weight gain, headache',
        'contraindications': 'Type 1 diabetes, diabetic ketoacidosis, severe liver disease',
        'price': 35.60,
        'category': 'Diabetes'
    },
    {
        'name': 'Nateglinide',
        'description': 'Meglitinide for type 2 diabetes control',
        'dosage': '60-120mg before each meal',
        'side_effects': 'Hypoglycemia, weight gain, upper respiratory infection',
        'contraindications': 'Type 1 diabetes, diabetic ketoacidosis, severe liver disease',
        'price': 38.90,
        'category': 'Diabetes'
    },
    {
        'name': 'Exenatide',
        'description': 'GLP-1 receptor agonist for type 2 diabetes',
        'dosage': '5-10mcg twice daily before meals',
        'side_effects': 'Nausea, vomiting, diarrhea, injection site reactions',
        'contraindications': 'Type 1 diabetes, severe kidney disease, personal/family history of medullary thyroid carcinoma',
        'price': 125.00,
        'category': 'Diabetes'
    },
    
    # Respiratory Medicines
    {
        'name': 'Budesonide',
        'description': 'Inhaled corticosteroid for asthma and COPD',
        'dosage': '200-800mcg twice daily',
        'side_effects': 'Oral thrush, hoarseness, cough, adrenal suppression',
        'contraindications': 'Active tuberculosis, untreated fungal infections',
        'price': 42.30,
        'category': 'Respiratory'
    },
    {
        'name': 'Fluticasone',
        'description': 'Inhaled corticosteroid for asthma and allergic rhinitis',
        'dosage': '100-1000mcg twice daily',
        'side_effects': 'Oral thrush, hoarseness, headache, nasal irritation',
        'contraindications': 'Active tuberculosis, untreated fungal infections',
        'price': 38.75,
        'category': 'Respiratory'
    },
    {
        'name': 'Formoterol',
        'description': 'Long-acting beta-agonist for asthma and COPD',
        'dosage': '12mcg twice daily',
        'side_effects': 'Tremors, increased heart rate, headache, muscle cramps',
        'contraindications': 'Uncontrolled asthma, severe heart disease',
        'price': 55.20,
        'category': 'Respiratory'
    },
    {
        'name': 'Salmeterol',
        'description': 'Long-acting beta-agonist for asthma and COPD',
        'dosage': '50mcg twice daily',
        'side_effects': 'Tremors, increased heart rate, headache, throat irritation',
        'contraindications': 'Uncontrolled asthma, severe heart disease',
        'price': 47.80,
        'category': 'Respiratory'
    },
    {
        'name': 'Ipratropium',
        'description': 'Anticholinergic bronchodilator for COPD and asthma',
        'dosage': '2-4 puffs every 4-6 hours',
        'side_effects': 'Dry mouth, cough, headache, blurred vision',
        'contraindications': 'Hypersensitivity to atropine, narrow-angle glaucoma',
        'price': 28.90,
        'category': 'Respiratory'
    },
    {
        'name': 'Tiotropium',
        'description': 'Long-acting anticholinergic for COPD',
        'dosage': '18mcg once daily',
        'side_effects': 'Dry mouth, cough, headache, urinary retention',
        'contraindications': 'Hypersensitivity to atropine, narrow-angle glaucoma',
        'price': 89.50,
        'category': 'Respiratory'
    },
    {
        'name': 'Theophylline',
        'description': 'Methylxanthine bronchodilator for asthma and COPD',
        'dosage': '200-600mg daily in divided doses',
        'side_effects': 'Nausea, insomnia, headache, arrhythmias',
        'contraindications': 'Uncontrolled arrhythmias, active peptic ulcer',
        'price': 15.40,
        'category': 'Respiratory'
    },
    {
        'name': 'Cromolyn',
        'description': 'Mast cell stabilizer for asthma prevention',
        'dosage': '2 puffs 4 times daily',
        'side_effects': 'Throat irritation, cough, bad taste, headache',
        'contraindications': 'Acute asthma attacks, hypersensitivity',
        'price': 32.60,
        'category': 'Respiratory'
    },
    {
        'name': 'Nedocromil',
        'description': 'Mast cell stabilizer for asthma prevention',
        'dosage': '2 puffs 2-4 times daily',
        'side_effects': 'Throat irritation, cough, headache, nausea',
        'contraindications': 'Acute asthma attacks, hypersensitivity',
        'price': 29.80,
        'category': 'Respiratory'
    },
    {
        'name': 'Zafirlukast',
        'description': 'Leukotriene receptor antagonist for asthma',
        'dosage': '20mg twice daily',
        'side_effects': 'Headache, nausea, diarrhea, liver problems',
        'contraindications': 'Liver disease, hypersensitivity',
        'price': 67.40,
        'category': 'Respiratory'
    },
    
    # Mental Health Medicines
    {
        'name': 'Fluoxetine',
        'description': 'SSRI antidepressant for depression and anxiety',
        'dosage': '20-80mg once daily',
        'side_effects': 'Nausea, insomnia, sexual dysfunction, weight changes',
        'contraindications': 'MAOI use, bipolar disorder, pregnancy',
        'price': 18.90,
        'category': 'Mental Health'
    },
    {
        'name': 'Escitalopram',
        'description': 'SSRI antidepressant for depression and anxiety',
        'dosage': '10-20mg once daily',
        'side_effects': 'Nausea, insomnia, sexual dysfunction, sweating',
        'contraindications': 'MAOI use, bipolar disorder, pregnancy',
        'price': 25.60,
        'category': 'Mental Health'
    },
    {
        'name': 'Paroxetine',
        'description': 'SSRI antidepressant for depression and anxiety',
        'dosage': '20-50mg once daily',
        'side_effects': 'Nausea, drowsiness, sexual dysfunction, weight gain',
        'contraindications': 'MAOI use, bipolar disorder, pregnancy',
        'price': 22.80,
        'category': 'Mental Health'
    },
    {
        'name': 'Citalopram',
        'description': 'SSRI antidepressant for depression',
        'dosage': '20-40mg once daily',
        'side_effects': 'Nausea, insomnia, sexual dysfunction, QT prolongation',
        'contraindications': 'MAOI use, bipolar disorder, heart conditions',
        'price': 19.75,
        'category': 'Mental Health'
    },
    {
        'name': 'Venlafaxine',
        'description': 'SNRI antidepressant for depression and anxiety',
        'dosage': '75-225mg daily in divided doses',
        'side_effects': 'Nausea, insomnia, increased blood pressure, sweating',
        'contraindications': 'MAOI use, uncontrolled hypertension',
        'price': 31.40,
        'category': 'Mental Health'
    },
    {
        'name': 'Bupropion',
        'description': 'Atypical antidepressant for depression and smoking cessation',
        'dosage': '150-450mg daily in divided doses',
        'side_effects': 'Insomnia, headache, dry mouth, seizures',
        'contraindications': 'Seizure disorders, eating disorders, brain injury',
        'price': 28.90,
        'category': 'Mental Health'
    },
    {
        'name': 'Mirtazapine',
        'description': 'Tetracyclic antidepressant for depression',
        'dosage': '15-45mg once daily at bedtime',
        'side_effects': 'Sedation, weight gain, increased appetite, dizziness',
        'contraindications': 'MAOI use, severe liver disease',
        'price': 24.60,
        'category': 'Mental Health'
    },
    {
        'name': 'Trazodone',
        'description': 'Serotonin antagonist and reuptake inhibitor for depression',
        'dosage': '150-400mg daily in divided doses',
        'side_effects': 'Sedation, priapism, dizziness, nausea',
        'contraindications': 'MAOI use, recent heart attack',
        'price': 16.80,
        'category': 'Mental Health'
    },
    {
        'name': 'Amitriptyline',
        'description': 'Tricyclic antidepressant for depression and nerve pain',
        'dosage': '25-150mg daily in divided doses',
        'side_effects': 'Sedation, dry mouth, constipation, urinary retention',
        'contraindications': 'MAOI use, recent heart attack, glaucoma',
        'price': 12.40,
        'category': 'Mental Health'
    },
    {
        'name': 'Nortriptyline',
        'description': 'Tricyclic antidepressant for depression',
        'dosage': '25-150mg daily in divided doses',
        'side_effects': 'Sedation, dry mouth, constipation, orthostatic hypotension',
        'contraindications': 'MAOI use, recent heart attack, glaucoma',
        'price': 14.20,
        'category': 'Mental Health'
    },
    
    # Antibiotics
    {
        'name': 'Doxycycline',
        'description': 'Tetracycline antibiotic for various bacterial infections',
        'dosage': '100mg twice daily for 7-14 days',
        'side_effects': 'Nausea, photosensitivity, esophageal irritation',
        'contraindications': 'Pregnancy, children under 8, severe liver disease',
        'price': 13.50,
        'category': 'Antibiotic'
    },
    {
        'name': 'Clarithromycin',
        'description': 'Macrolide antibiotic for respiratory and skin infections',
        'dosage': '250-500mg twice daily for 7-14 days',
        'side_effects': 'Nausea, diarrhea, taste disturbances, QT prolongation',
        'contraindications': 'Liver disease, QT prolongation, pregnancy',
        'price': 26.80,
        'category': 'Antibiotic'
    },
    {
        'name': 'Erythromycin',
        'description': 'Macrolide antibiotic for various bacterial infections',
        'dosage': '250-500mg 4 times daily for 7-14 days',
        'side_effects': 'Nausea, diarrhea, abdominal pain, QT prolongation',
        'contraindications': 'Liver disease, QT prolongation, myasthenia gravis',
        'price': 18.90,
        'category': 'Antibiotic'
    },
    {
        'name': 'Tetracycline',
        'description': 'Tetracycline antibiotic for various infections',
        'dosage': '250-500mg 4 times daily for 7-14 days',
        'side_effects': 'Nausea, photosensitivity, esophageal irritation',
        'contraindications': 'Pregnancy, children under 8, severe liver disease',
        'price': 11.20,
        'category': 'Antibiotic'
    },
    {
        'name': 'Minocycline',
        'description': 'Tetracycline antibiotic for acne and infections',
        'dosage': '100mg twice daily for 7-14 days',
        'side_effects': 'Dizziness, photosensitivity, skin discoloration',
        'contraindications': 'Pregnancy, children under 8, severe liver disease',
        'price': 34.60,
        'category': 'Antibiotic'
    },
    {
        'name': 'Levofloxacin',
        'description': 'Fluoroquinolone antibiotic for various infections',
        'dosage': '250-750mg once daily for 7-14 days',
        'side_effects': 'Nausea, tendon rupture, photosensitivity, QT prolongation',
        'contraindications': 'Tendon disorders, myasthenia gravis, pregnancy',
        'price': 29.80,
        'category': 'Antibiotic'
    },
    {
        'name': 'Moxifloxacin',
        'description': 'Fluoroquinolone antibiotic for respiratory infections',
        'dosage': '400mg once daily for 7-14 days',
        'side_effects': 'Nausea, tendon rupture, QT prolongation, photosensitivity',
        'contraindications': 'Tendon disorders, myasthenia gravis, QT prolongation',
        'price': 42.50,
        'category': 'Antibiotic'
    },
    {
        'name': 'Gentamicin',
        'description': 'Aminoglycoside antibiotic for serious infections',
        'dosage': '1.5-2mg/kg every 8 hours',
        'side_effects': 'Nephrotoxicity, ototoxicity, neuromuscular blockade',
        'contraindications': 'Severe kidney disease, myasthenia gravis',
        'price': 8.90,
        'category': 'Antibiotic'
    },
    {
        'name': 'Tobramycin',
        'description': 'Aminoglycoside antibiotic for serious infections',
        'dosage': '1-1.7mg/kg every 8 hours',
        'side_effects': 'Nephrotoxicity, ototoxicity, neuromuscular blockade',
        'contraindications': 'Severe kidney disease, myasthenia gravis',
        'price': 12.40,
        'category': 'Antibiotic'
    },
    {
        'name': 'Vancomycin',
        'description': 'Glycopeptide antibiotic for serious infections',
        'dosage': '15-20mg/kg every 8-12 hours',
        'side_effects': 'Nephrotoxicity, ototoxicity, red man syndrome',
        'contraindications': 'Severe kidney disease, hypersensitivity',
        'price': 156.80,
        'category': 'Antibiotic'
    },
    
    # Pain Relief and Anti-inflammatory
    {
        'name': 'Naproxen',
        'description': 'NSAID for pain, inflammation, and arthritis',
        'dosage': '250-500mg twice daily',
        'side_effects': 'Stomach upset, heartburn, increased bleeding risk',
        'contraindications': 'Stomach ulcers, heart disease, kidney problems',
        'price': 9.75,
        'category': 'Pain Relief'
    },
    {
        'name': 'Celecoxib',
        'description': 'COX-2 selective NSAID for arthritis and pain',
        'dosage': '100-200mg twice daily',
        'side_effects': 'Stomach upset, headache, increased cardiovascular risk',
        'contraindications': 'Heart disease, stomach ulcers, sulfa allergy',
        'price': 45.20,
        'category': 'Pain Relief'
    },
    {
        'name': 'Meloxicam',
        'description': 'NSAID for arthritis and pain management',
        'dosage': '7.5-15mg once daily',
        'side_effects': 'Stomach upset, headache, increased bleeding risk',
        'contraindications': 'Stomach ulcers, heart disease, kidney problems',
        'price': 18.90,
        'category': 'Pain Relief'
    },
    {
        'name': 'Ketorolac',
        'description': 'NSAID for short-term pain relief',
        'dosage': '10mg every 4-6 hours, max 40mg/day',
        'side_effects': 'Stomach upset, bleeding risk, kidney problems',
        'contraindications': 'Stomach ulcers, kidney disease, pregnancy',
        'price': 22.60,
        'category': 'Pain Relief'
    },
    {
        'name': 'Tramadol',
        'description': 'Opioid analgesic for moderate to severe pain',
        'dosage': '50-100mg every 4-6 hours',
        'side_effects': 'Drowsiness, constipation, nausea, dependence',
        'contraindications': 'Respiratory depression, acute intoxication',
        'price': 16.80,
        'category': 'Pain Relief'
    },
    {
        'name': 'Codeine',
        'description': 'Opioid analgesic for mild to moderate pain',
        'dosage': '15-60mg every 4-6 hours',
        'side_effects': 'Drowsiness, constipation, nausea, dependence',
        'contraindications': 'Respiratory depression, acute intoxication',
        'price': 12.40,
        'category': 'Pain Relief'
    },
    {
        'name': 'Morphine',
        'description': 'Opioid analgesic for severe pain',
        'dosage': '10-30mg every 4 hours as needed',
        'side_effects': 'Drowsiness, constipation, respiratory depression',
        'contraindications': 'Respiratory depression, acute intoxication',
        'price': 8.90,
        'category': 'Pain Relief'
    },
    {
        'name': 'Oxycodone',
        'description': 'Opioid analgesic for moderate to severe pain',
        'dosage': '5-20mg every 4-6 hours',
        'side_effects': 'Drowsiness, constipation, nausea, dependence',
        'contraindications': 'Respiratory depression, acute intoxication',
        'price': 24.60,
        'category': 'Pain Relief'
    },
    {
        'name': 'Fentanyl',
        'description': 'Potent opioid analgesic for severe pain',
        'dosage': '25-100mcg patch every 72 hours',
        'side_effects': 'Drowsiness, constipation, respiratory depression',
        'contraindications': 'Respiratory depression, acute intoxication',
        'price': 89.50,
        'category': 'Pain Relief'
    },
    {
        'name': 'Buprenorphine',
        'description': 'Partial opioid agonist for pain and addiction treatment',
        'dosage': '2-8mg sublingual daily',
        'side_effects': 'Drowsiness, constipation, headache, withdrawal',
        'contraindications': 'Respiratory depression, acute intoxication',
        'price': 67.80,
        'category': 'Pain Relief'
    }
] 