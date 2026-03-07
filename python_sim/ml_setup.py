"""
ML Irrigation System - Complete Setup & Integration Guide

This script orchestrates the complete ML pipeline:
1. Generate synthetic training data
2. Train ML models (Random Forest, XGBoost)
3. Evaluate model performance
4. Test predictions
5. Provide integration examples

Run this to set up the complete ML system for your farming simulator.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ml_dataset_generation import IrrigationDatasetGenerator
from ml_train_model import IrrigationMLPipeline
from ml_irrigation_predictor import load_predictor


def print_header(title: str):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def step1_generate_dataset():
    """Step 1: Generate synthetic training dataset."""
    print_header("STEP 1: GENERATING SYNTHETIC DATASET")
    
    generator = IrrigationDatasetGenerator(n_samples=5000, random_seed=42)
    df = generator.generate_dataset()
    
    print(f"Dataset shape: {df.shape}")
    print(f"\nDataset statistics:")
    print(df.describe())
    
    print(f"\nCrop distribution:")
    print(df["crop"].value_counts())
    
    print(f"\nIrrigation decision distribution:")
    irrigation_counts = df["irrigation_decision"].value_counts()
    print(f"  Irrigate (1): {irrigation_counts.get(1, 0)} samples")
    print(f"  Skip (0): {irrigation_counts.get(0, 0)} samples")
    
    output_path = Path(__file__).parent / "irrigation_dataset.csv"
    generator.save_dataset(df, str(output_path))
    
    return True


def step2_train_models():
    """Step 2: Train ML models."""
    print_header("STEP 2: TRAINING ML MODELS")
    
    # Check if dataset exists
    dataset_path = Path(__file__).parent / "irrigation_dataset.csv"
    if not dataset_path.exists():
        print("✗ Dataset not found. Please run Step 1 first.")
        return False
    
    pipeline = IrrigationMLPipeline(str(dataset_path))
    pipeline.load_data()
    pipeline.preprocess_data()
    pipeline.train_classifier()
    pipeline.train_regressor()
    pipeline.save_models(str(Path(__file__).parent))
    pipeline.print_summary()
    
    return True


def step3_test_predictor():
    """Step 3: Test trained predictor."""
    print_header("STEP 3: TESTING PREDICTOR")
    
    # Check if models exist
    model_dir = Path(__file__).parent
    if not (model_dir / "irrigation_classifier.pkl").exists():
        print("✗ Models not found. Please run Step 2 first.")
        return False
    
    predictor = load_predictor(str(model_dir))
    
    # Get model info
    info = predictor.get_model_info()
    print(f"Classifier: {info['classifier']}")
    print(f"Regressor: {info['regressor']}")
    print(f"Features: {info['features']}\n")
    
    # Test predictions
    test_cases = [
        {
            "name": "🔴 CRITICAL: Dry field, hot, no rain",
            "crop": "rice",
            "farm_area": 5.0,
            "temperature": 35,
            "humidity": 30,
            "rainfall": 0,
            "soil_moisture": 20,
            "location": "Punjab, India",
        },
        {
            "name": "🟡 MODERATE: Adequate moisture, warm",
            "crop": "wheat",
            "farm_area": 3.0,
            "temperature": 22,
            "humidity": 60,
            "rainfall": 0,
            "soil_moisture": 55,
            "location": "Haryana, India",
        },
        {
            "name": "🟢 GOOD: Wet field, cool, rain possible",
            "crop": "maize",
            "farm_area": 7.5,
            "temperature": 15,
            "humidity": 75,
            "rainfall": 8,
            "soil_moisture": 75,
            "location": "Maharashtra, India",
        },
    ]
    
    print("Test Predictions:\n")
    for i, test in enumerate(test_cases, 1):
        print(f"{i}. {test['name']}")
        
        decision, amount, reason = predictor.predict(
            crop=test["crop"],
            farm_area=test["farm_area"],
            temperature=test["temperature"],
            humidity=test["humidity"],
            rainfall=test["rainfall"],
            soil_moisture=test["soil_moisture"],
            location=test["location"],
        )
        
        print(f"   Decision: {decision} (1=Irrigate, 0=Skip)")
        print(f"   Water Amount: {amount:.0f} liters")
        print(f"   Reasoning: {reason}")
        print()
    
    return True


def print_integration_guide():
    """Print guide for integrating into farm_sim.py."""
    print_header("INTEGRATION GUIDE: Adding ML to farm_sim.py")
    
    guide = """
QUICK INTEGRATION CHECKLIST:

1. Import the predictor at the top of farm_sim.py:
   ───────────────────────────────────────────────
   from ml_irrigation_predictor import load_predictor

2. Initialize predictor in FarmSimulation.__init__():
   ───────────────────────────────────────────────
   def __init__(self, ...):
       ...
       # Load ML irrigation predictor
       self.ml_predictor = load_predictor()
       self.ai_decision_message = ""
       self.ai_decision_timer = 0.0

3. Update _update_tiles() to use ML predictions:
   ───────────────────────────────────────────────
   def _update_tiles(self, dt: float):
       cfg = WEATHER_CONFIG[self.weather]
       
       for x, y in self.farmland_positions:
           tile = self.tiles[y][x]
           
           # Get ML prediction
           decision, amount, reasoning = self.ml_predictor.predict(
               crop=self.crop_name.lower(),
               farm_area=self.land_area,
               temperature=self.current_temp,
               humidity=self.current_humidity,
               rainfall=self.current_rainfall,
               soil_moisture=tile.moisture,
               location=self.location,
           )
           
           # Apply weather effects
           tile.moisture -= cfg["evap"] * dt
           tile.moisture += cfg["rain_gain"] * dt
           
           # Apply ML-based irrigation if decision is 1
           if decision == 1 and amount > 0:
               liters_per_tile = amount / len(self.farmland_positions)
               tile.moisture += (liters_per_tile / 100) * dt
               self.ai_decision_message = reasoning
               self.ai_decision_timer = 5.0
           
           # Store for HUD display
           self.current_ai_decision = decision

4. Display AI decision in _draw_hud():
   ────────────────────────────────────
   In the HUD section, add:
   
   if self.ai_decision_message and self.ai_decision_timer > 0:
       msg_surf = self.small_font.render(self.ai_decision_message, True, (100, 200, 100))
       self.screen.blit(msg_surf, (HUD_WIDTH + 10, 150))
       self.ai_decision_timer -= dt

TESTING THE INTEGRATION:

   python python_sim/farm_sim.py --username Ankit22

   You should see:
   - AI irrigation messages in the HUD
   - Soil moisture responding to AI decisions
   - Different behaviors based on weather/crop/soil conditions

PRODUCTION EXTENSIONS:

   1. Real IoT Integration:
      - Replace synthetic weather with actual sensor data
      - Use real soil moisture sensors (e.g., capacitive sensors)
      - Integrate with weather APIs (OpenWeatherMap)
   
   2. Model Improvement:
      - Collect real farm data over seasons
      - Retrain models with actual irrigation outcomes
      - Add farmer feedback loop
   
   3. Advanced Features:
      - Schedule-based irrigation (e.g., early morning)
      - Crop stage-based adjustments
      - Price-based optimization (water cost)
      - Multi-field irrigation coordination
   
   4. Monitoring & Alerting:
      - Log predictions and actual outcomes
      - Alert on anomalies
      - Dashboard with model confidence scores

REFERENCES:

   - Dataset: irrigation_dataset.csv
   - Trained Models: irrigation_classifier.pkl, irrigation_regressor.pkl
   - Preprocessing: irrigation_preprocessing.pkl
   - Metadata: irrigation_metadata.pkl
"""
    
    print(guide)


def main():
    """Main orchestration function."""
    print("\n" + "=" * 80)
    print("  ML-BASED IRRIGATION PREDICTION SYSTEM - COMPLETE SETUP")
    print("=" * 80)
    
    print("""
This setup will:
1. Generate 5,000 synthetic training samples
2. Train Random Forest & XGBoost models
3. Test predictions on sample scenarios
4. Save models for use in simulator

Estimated time: 2-3 minutes
""")
    
    input("Press Enter to start...\n")
    
    # Step 1: Generate dataset
    try:
        if not step1_generate_dataset():
            sys.exit(1)
    except Exception as e:
        print(f"✗ Error in dataset generation: {e}")
        sys.exit(1)
    
    input("\nPress Enter to continue to model training...\n")
    
    # Step 2: Train models
    try:
        if not step2_train_models():
            sys.exit(1)
    except Exception as e:
        print(f"✗ Error in model training: {e}")
        sys.exit(1)
    
    input("\nPress Enter to test predictor...\n")
    
    # Step 3: Test predictor
    try:
        if not step3_test_predictor():
            sys.exit(1)
    except Exception as e:
        print(f"✗ Error in testing: {e}")
        sys.exit(1)
    
    # Print integration guide
    print_integration_guide()
    
    print_header("SETUP COMPLETE!")
    print("""
✓ Dataset generated: irrigation_dataset.csv
✓ Models trained and saved
✓ Predictor tested successfully

NEXT STEPS:

1. Integrate into farm_sim.py using the guide above
2. Run simulator with: python python_sim/farm_sim.py --username Ankit22
3. Watch AI-driven irrigation decisions in real-time!

For more information, see:
- python_sim/ml_dataset_generation.py
- python_sim/ml_train_model.py
- python_sim/ml_irrigation_predictor.py
""")


if __name__ == "__main__":
    main()
