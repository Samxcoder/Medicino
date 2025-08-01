#!/usr/bin/env python3
"""
Test the improved diagnosis algorithm
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import diagnose_symptoms

def test_diagnosis():
    test_cases = [
        "persistent fever",
        "fever and cough",
        "headache, fever, cough",
        "stomach pain, nausea, vomiting",
        "chest pain, shortness of breath",
        "joint pain, stiffness, swelling",
        "fatigue, weight loss, increased thirst",
        "itchy skin, red patches",
        "ear pain, hearing loss",
        "blurred vision, headache"
    ]
    
    print("Testing Improved Diagnosis Algorithm")
    print("=" * 50)
    
    for symptoms in test_cases:
        print(f"\n🔍 Input: '{symptoms}'")
        result = diagnose_symptoms(symptoms)
        print(f"📋 Condition: {result['disease']}")
        print(f"🎯 Confidence: {result['confidence']}%")
        print(f"⚠️  Severity: {result['severity']}")
        print(f"🌿 Ayurvedic: {result['ayurvedic'][:80]}...")
        print(f"💊 Medicine: {result['medicine'][:80]}...")
        print("-" * 50)

if __name__ == '__main__':
    test_diagnosis() 