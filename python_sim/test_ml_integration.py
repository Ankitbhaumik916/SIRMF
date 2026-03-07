"""
Quick test to verify ML integration works with farm_sim.py
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ml_irrigation_predictor import load_predictor

def test_ml_integration():
    """Test that ML predictor loads and works with farm_sim parameters."""
    
    print("=" * 70)
    print("ML INTEGRATION TEST")
    print("=" * 70)
    
    # Load predictor
    try:
        predictor = load_predictor()
        print("✓ ML predictor loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load ML predictor: {e}")
        return False
    
    # Simulate a few farm conditions (like farm_sim.py would call)
    test_cases = [
        {
            "name": "Sunny conditions (high evaporation)",
            "crop": "rice",
            "farm_area": 5.0,
            "temperature": 32,
            "humidity": 35,
            "rainfall": 0.0,
            "soil_moisture": 35.0,
            "location": "Punjab, India",
        },
        {
            "name": "Rainy conditions (low evaporation)",
            "crop": "wheat",
            "farm_area": 3.5,
            "temperature": 18,
            "humidity": 85,
            "rainfall": 5.0,
            "soil_moisture": 70.0,
            "location": "Haryana, India",
        },
        {
            "name": "Cloudy moderate conditions",
            "crop": "maize",
            "farm_area": 7.5,
            "temperature": 22,
            "humidity": 55,
            "rainfall": 0.0,
            "soil_moisture": 50.0,
            "location": "Maharashtra, India",
        },
    ]
    
    print("\n[*] Testing predictions with farm_sim weather conditions:\n")
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        print(f"  Weather: {test['temperature']}°C, {test['humidity']}% humidity, {test['rainfall']}mm rain")
        print(f"  Soil: {test['soil_moisture']:.1f}% moisture")
        
        try:
            decision, amount, reasoning = predictor.predict(
                crop=test["crop"],
                farm_area=test["farm_area"],
                temperature=test["temperature"],
                humidity=test["humidity"],
                rainfall=test["rainfall"],
                soil_moisture=test["soil_moisture"],
                location=test["location"],
            )
            
            print(f"  Decision: {'✓ IRRIGATE' if decision == 1 else '✗ SKIP'}")
            print(f"  Amount: {amount:.0f}L")
            print(f"  Reasoning: {reasoning[:60]}...")
            print()
        except Exception as e:
            print(f"  ✗ Prediction failed: {e}\n")
            return False
    
    print("=" * 70)
    print("✓ ALL TESTS PASSED - ML integration ready for farm_sim.py")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_ml_integration()
    sys.exit(0 if success else 1)
