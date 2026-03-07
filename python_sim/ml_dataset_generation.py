"""
ML Dataset Generation for Irrigation Prediction

Generates synthetic training data for ML-based irrigation prediction system.
This module creates realistic agricultural conditions based on:
- Crop type and its water requirements
- Weather patterns (temperature, humidity, rainfall)
- Farm properties (location, area)
- Soil moisture dynamics

The dataset mimics real-world irrigation scenarios without requiring physical sensors.
"""

import numpy as np
import pandas as pd
from pathlib import Path
import json


class IrrigationDatasetGenerator:
    """
    Generates synthetic but realistic irrigation training data.
    
    Attributes:
        crops: Dict of crop profiles with water requirements and optimal conditions
        locations: List of agricultural locations with climate profiles
        n_samples: Number of synthetic data points to generate
    """
    
    # Crop water requirements and optimal conditions (based on agricultural research)
    CROP_PROFILES = {
        "rice": {
            "daily_requirement": 600,        # liters/acre/day
            "optimal_moisture_min": 55,      # % soil moisture
            "optimal_moisture_max": 85,
            "temp_min": 20,                  # Celsius
            "temp_max": 30,
            "humidity_pref": 70,             # %
        },
        "wheat": {
            "daily_requirement": 350,
            "optimal_moisture_min": 40,
            "optimal_moisture_max": 70,
            "temp_min": 10,
            "temp_max": 25,
            "humidity_pref": 60,
        },
        "maize": {
            "daily_requirement": 550,
            "optimal_moisture_min": 45,
            "optimal_moisture_max": 75,
            "temp_min": 15,
            "temp_max": 30,
            "humidity_pref": 65,
        },
        "tomato": {
            "daily_requirement": 450,
            "optimal_moisture_min": 50,
            "optimal_moisture_max": 75,
            "temp_min": 18,
            "temp_max": 28,
            "humidity_pref": 65,
        },
        "cotton": {
            "daily_requirement": 500,
            "optimal_moisture_min": 40,
            "optimal_moisture_max": 70,
            "temp_min": 20,
            "temp_max": 32,
            "humidity_pref": 50,
        },
    }
    
    # Location climate profiles
    LOCATION_PROFILES = {
        "Punjab, India": {"avg_temp": 25, "avg_humidity": 60, "rainfall_prob": 0.3},
        "Haryana, India": {"avg_temp": 26, "avg_humidity": 55, "rainfall_prob": 0.25},
        "Maharashtra, India": {"avg_temp": 28, "avg_humidity": 65, "rainfall_prob": 0.4},
        "Kolkata, India": {"avg_temp": 27, "avg_humidity": 75, "rainfall_prob": 0.5},
        "Malda, West Bengal": {"avg_temp": 26, "avg_humidity": 70, "rainfall_prob": 0.45},
    }
    
    def __init__(self, n_samples: int = 5000, random_seed: int = 42):
        """
        Initialize dataset generator.
        
        Args:
            n_samples: Number of synthetic samples to generate
            random_seed: For reproducibility
        """
        self.n_samples = n_samples
        np.random.seed(random_seed)
        self.data = []
    
    def _calculate_irrigation_amount(self, crop_profile: dict, soil_moisture: float, 
                                    temperature: float, rainfall: float) -> float:
        """
        Calculate optimal irrigation water amount based on crop needs and conditions.
        
        Args:
            crop_profile: Crop water requirement profile
            soil_moisture: Current soil moisture (0-100%)
            temperature: Temperature in Celsius
            rainfall: Rainfall in mm
            
        Returns:
            Water amount in liters per acre
        """
        base_requirement = crop_profile["daily_requirement"]
        
        # Adjust for soil moisture deficit
        optimal_min = crop_profile["optimal_moisture_min"]
        optimal_max = crop_profile["optimal_moisture_max"]
        optimal_mid = (optimal_min + optimal_max) / 2
        
        # Moisture-based adjustment (0-100%)
        moisture_deficit = max(0, optimal_mid - soil_moisture)
        moisture_factor = 1 + (moisture_deficit / 100)
        
        # Temperature-based adjustment (higher temp = more water needed)
        temp_adjustment = 1 + (temperature - 25) * 0.02  # 2% per degree above 25C
        
        # Rainfall reduction (each mm reduces daily need)
        rainfall_reduction = min(base_requirement, rainfall * 50)  # 50L per mm
        
        # Final irrigation amount
        irrigation_amount = (base_requirement * moisture_factor * temp_adjustment) - rainfall_reduction
        
        return max(0, irrigation_amount)
    
    def _determine_irrigation_decision(self, soil_moisture: float, 
                                      irrigation_amount: float) -> int:
        """
        Determine whether to irrigate (binary classification).
        
        Args:
            soil_moisture: Current soil moisture percentage
            irrigation_amount: Calculated irrigation amount
            
        Returns:
            1 if irrigation needed, 0 otherwise
        """
        # Irrigate if:
        # 1. Soil moisture is below 35% (critical threshold)
        # 2. Irrigation amount is significant (> 100L)
        if soil_moisture < 35 or irrigation_amount > 100:
            return 1
        return 0
    
    def generate_dataset(self) -> pd.DataFrame:
        """
        Generate synthetic dataset with realistic patterns.
        
        Returns:
            DataFrame with features and target variables
        """
        records = []
        
        crops = list(self.CROP_PROFILES.keys())
        locations = list(self.LOCATION_PROFILES.keys())
        
        for _ in range(self.n_samples):
            # Random selection
            crop = np.random.choice(crops)
            location = np.random.choice(locations)
            
            crop_profile = self.CROP_PROFILES[crop]
            loc_profile = self.LOCATION_PROFILES[location]
            
            # Farm area (0.5 to 50 acres)
            farm_area = np.random.uniform(0.5, 50)
            
            # Temperature variation around location average
            temp = loc_profile["avg_temp"] + np.random.normal(0, 5)
            temp = np.clip(temp, 5, 40)
            
            # Humidity variation
            humidity = loc_profile["avg_humidity"] + np.random.normal(0, 10)
            humidity = np.clip(humidity, 20, 100)
            
            # Rainfall (mm) - stochastic based on location probability
            if np.random.random() < loc_profile["rainfall_prob"]:
                rainfall = np.random.exponential(scale=10) + 2  # 2-30mm typically
            else:
                rainfall = 0
            
            # Soil moisture (0-100%)
            soil_moisture = np.random.uniform(20, 80)
            
            # Calculate target: irrigation amount
            irrigation_amount = self._calculate_irrigation_amount(
                crop_profile, soil_moisture, temp, rainfall
            )
            
            # Calculate target: irrigation decision
            irrigation_decision = self._determine_irrigation_decision(soil_moisture, irrigation_amount)
            
            records.append({
                "crop": crop,
                "farm_area": farm_area,
                "temperature": temp,
                "humidity": humidity,
                "rainfall": rainfall,
                "soil_moisture": soil_moisture,
                "location": location,
                "irrigation_amount": irrigation_amount,
                "irrigation_decision": irrigation_decision,
            })
        
        df = pd.DataFrame(records)
        return df
    
    @staticmethod
    def save_dataset(df: pd.DataFrame, filepath: str = "irrigation_dataset.csv"):
        """Save dataset to CSV."""
        df.to_csv(filepath, index=False)
        print(f"✓ Dataset saved to {filepath}")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
    
    @staticmethod
    def load_dataset(filepath: str = "irrigation_dataset.csv") -> pd.DataFrame:
        """Load dataset from CSV."""
        return pd.read_csv(filepath)


def main():
    """Generate and save synthetic irrigation dataset."""
    print("=" * 70)
    print("IRRIGATION ML DATASET GENERATION")
    print("=" * 70)
    
    generator = IrrigationDatasetGenerator(n_samples=5000, random_seed=42)
    
    print("\n[1/3] Generating synthetic dataset...")
    df = generator.generate_dataset()
    
    print("\n[2/3] Dataset Statistics:")
    print(df.describe())
    
    print("\n[3/3] Class Distribution:")
    print(f"  Irrigate (1): {(df['irrigation_decision'] == 1).sum()} samples")
    print(f"  Skip (0): {(df['irrigation_decision'] == 0).sum()} samples")
    print(f"  Balance: {(df['irrigation_decision'] == 1).sum() / len(df) * 100:.1f}% irrigation")
    
    output_dir = Path(__file__).parent
    output_path = output_dir / "irrigation_dataset.csv"
    
    generator.save_dataset(df, str(output_path))
    
    print("\n" + "=" * 70)
    print("✓ Dataset generation complete!")
    print(f"  Saved to: {output_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
