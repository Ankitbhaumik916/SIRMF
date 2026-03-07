"""
ML Irrigation Prediction - Inference Module

Loads trained models and provides irrigation predictions for the simulator.
This module encapsulates all prediction logic and is designed to integrate
seamlessly with the pygame farming simulation.

Usage in simulator:
    predictor = IrrigationPredictor()
    decision, amount, reasoning = predictor.predict(crop, farm_area, temp, 
                                                    humidity, rainfall, 
                                                    soil_moisture, location)
"""

import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, Any


class IrrigationPredictor:
    """
    ML-based irrigation prediction system.
    
    Loads trained models and provides real-time irrigation recommendations
    for the farming simulator.
    
    Attributes:
        classifier: Model for irrigation decision (yes/no)
        regressor: Model for water amount prediction
        scaler: Feature scaler for preprocessing
        label_encoders: Categorical feature encoders
        metadata: Model metadata and feature information
    """
    
    def __init__(self, model_dir: str = None):
        """
        Initialize predictor by loading trained models.
        
        Args:
            model_dir: Directory containing model files. 
                      If None, uses current script directory.
        """
        if model_dir is None:
            model_dir = Path(__file__).parent
        else:
            model_dir = Path(model_dir)
        
        print("[*] Loading irrigation prediction models...")
        
        # Load models
        with open(model_dir / "irrigation_classifier.pkl", "rb") as f:
            self.classifier = pickle.load(f)
        
        with open(model_dir / "irrigation_regressor.pkl", "rb") as f:
            self.regressor = pickle.load(f)
        
        # Load preprocessing objects
        with open(model_dir / "irrigation_preprocessing.pkl", "rb") as f:
            preprocessing = pickle.load(f)
            self.scaler = preprocessing["scaler"]
            self.label_encoders = preprocessing["label_encoders"]
        
        # Load metadata
        with open(model_dir / "irrigation_metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)
        
        print(f"    ✓ Loaded {self.metadata['classifier_name']} classifier")
        print(f"    ✓ Loaded {self.metadata['regressor_name']} regressor")
    
    def _prepare_features(self, crop: str, farm_area: float, temperature: float,
                         humidity: float, rainfall: float, soil_moisture: float,
                         location: str) -> np.ndarray:
        """
        Prepare and encode features for prediction.
        
        Args:
            crop: Crop type (e.g., 'rice', 'wheat', 'maize')
            farm_area: Farm area in acres
            temperature: Temperature in Celsius
            humidity: Humidity percentage (0-100)
            rainfall: Rainfall in mm
            soil_moisture: Soil moisture percentage (0-100)
            location: Location string
            
        Returns:
            Scaled feature array ready for prediction
        """
        # Create feature dictionary
        features_dict = {
            "crop": crop.lower(),
            "farm_area": farm_area,
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
            "soil_moisture": soil_moisture,
            "location": location,
        }
        
        # Encode categorical features
        features_dict["crop"] = self.label_encoders["crop"].transform(
            [features_dict["crop"]]
        )[0]
        
        # Handle unknown locations gracefully
        try:
            features_dict["location"] = self.label_encoders["location"].transform(
                [features_dict["location"]]
            )[0]
        except ValueError:
            # Use most common location code if location is unknown
            features_dict["location"] = 0
        
        # Create feature array in correct order
        feature_order = self.metadata["feature_names"]
        X = np.array([[
            features_dict[name] for name in feature_order
        ]])
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def predict(self, crop: str, farm_area: float, temperature: float,
               humidity: float, rainfall: float, soil_moisture: float,
               location: str = "Unknown") -> Tuple[int, float, str]:
        """
        Predict irrigation decision and water amount.
        
        Args:
            crop: Crop type
            farm_area: Farm area in acres
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            rainfall: Rainfall in mm
            soil_moisture: Soil moisture percentage
            location: Location (optional)
            
        Returns:
            Tuple of:
                - irrigation_decision (1 = irrigate, 0 = skip)
                - water_amount (liters)
                - reasoning (explanation message)
        """
        # Prepare features
        X = self._prepare_features(crop, farm_area, temperature, humidity,
                                  rainfall, soil_moisture, location)
        
        # Predict
        decision = int(self.classifier.predict(X)[0])
        water_amount = max(0, float(self.regressor.predict(X)[0]))
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            decision, water_amount, soil_moisture, temperature,
            humidity, rainfall, crop
        )
        
        return decision, water_amount, reasoning
    
    def _generate_reasoning(self, decision: int, water_amount: float,
                           soil_moisture: float, temperature: float,
                           humidity: float, rainfall: float,
                           crop: str) -> str:
        """
        Generate human-readable explanation for AI decision.
        
        Args:
            decision: 1 = irrigate, 0 = skip
            water_amount: Predicted water amount
            soil_moisture: Current soil moisture
            temperature: Current temperature
            humidity: Current humidity
            rainfall: Current rainfall
            crop: Crop type
            
        Returns:
            Explanation message
        """
        reasons = []
        
        if decision == 1:
            # Collect reasons for irrigation
            if soil_moisture < 35:
                reasons.append(f"Low soil moisture ({soil_moisture:.0f}%)")
            
            if temperature > 28:
                reasons.append(f"High temperature ({temperature:.0f}°C)")
            
            if humidity < 40:
                reasons.append(f"Low humidity ({humidity:.0f}%)")
            
            if rainfall == 0:
                reasons.append("No rainfall today")
            
            reason_text = " and ".join(reasons) if reasons else "Optimal irrigation time"
            decision_text = f"Apply {water_amount:.0f}L"
            
            return f"✓ AI IRRIGATE: {decision_text} due to {reason_text}"
        else:
            # Collect reasons for skipping
            if soil_moisture > 65:
                reasons.append(f"Adequate moisture ({soil_moisture:.0f}%)")
            
            if rainfall > 0:
                reasons.append(f"Rainfall detected ({rainfall:.1f}mm)")
            
            if humidity > 70:
                reasons.append(f"High humidity ({humidity:.0f}%)")
            
            if temperature < 15:
                reasons.append(f"Cool temperature ({temperature:.0f}°C)")
            
            reason_text = " and ".join(reasons) if reasons else "Not needed yet"
            
            return f"✗ AI SKIP: {reason_text}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models."""
        return {
            "classifier": self.metadata["classifier_name"],
            "regressor": self.metadata["regressor_name"],
            "features": self.metadata["feature_names"],
            "classifier_results": self.metadata.get("classifier_results", {}),
            "regressor_results": self.metadata.get("regressor_results", {}),
        }
    
    def predict_batch(self, features_list: list) -> list:
        """
        Make predictions on multiple samples.
        
        Args:
            features_list: List of dicts with keys:
                          [crop, farm_area, temperature, humidity, 
                           rainfall, soil_moisture, location]
                           
        Returns:
            List of tuples (decision, water_amount, reasoning)
        """
        results = []
        for features in features_list:
            result = self.predict(
                crop=features["crop"],
                farm_area=features["farm_area"],
                temperature=features["temperature"],
                humidity=features["humidity"],
                rainfall=features["rainfall"],
                soil_moisture=features["soil_moisture"],
                location=features.get("location", "Unknown"),
            )
            results.append(result)
        
        return results


def load_predictor(model_dir: str = None) -> IrrigationPredictor:
    """
    Convenience function to load predictor.
    
    Args:
        model_dir: Directory containing models (optional)
        
    Returns:
        IrrigationPredictor instance
    """
    return IrrigationPredictor(model_dir)


if __name__ == "__main__":
    # Test the predictor
    print("=" * 70)
    print("IRRIGATION ML PREDICTOR - TEST")
    print("=" * 70)
    
    try:
        predictor = IrrigationPredictor()
        
        print("\n[*] Testing predictions...")
        
        # Test case 1: Dry soil, hot, no rain
        print("\nTest 1: Dry conditions")
        decision, amount, reason = predictor.predict(
            crop="rice",
            farm_area=5.0,
            temperature=32,
            humidity=35,
            rainfall=0,
            soil_moisture=25,
            location="Punjab, India"
        )
        print(f"  Decision: {decision} | Amount: {amount:.0f}L | {reason}")
        
        # Test case 2: Adequate soil, cool, rain expected
        print("\nTest 2: Adequate conditions")
        decision, amount, reason = predictor.predict(
            crop="wheat",
            farm_area=3.0,
            temperature=18,
            humidity=70,
            rainfall=5,
            soil_moisture=65,
            location="Haryana, India"
        )
        print(f"  Decision: {decision} | Amount: {amount:.0f}L | {reason}")
        
        # Test case 3: Moderate conditions
        print("\nTest 3: Moderate conditions")
        decision, amount, reason = predictor.predict(
            crop="maize",
            farm_area=7.5,
            temperature=25,
            humidity=55,
            rainfall=0,
            soil_moisture=50,
            location="Maharashtra, India"
        )
        print(f"  Decision: {decision} | Amount: {amount:.0f}L | {reason}")
        
        print("\n" + "=" * 70)
        print("✓ Predictor test complete!")
        print("=" * 70)
        
    except FileNotFoundError:
        print("✗ Models not found. Please run ml_train_model.py first.")
