"""
ML Model Training for Irrigation Prediction

Trains Random Forest and XGBoost models on synthetic irrigation dataset.
Evaluates model performance and saves the best model as a pickle file.

Models learned:
- Binary classification: Should we irrigate? (Yes/No)
- Regression: How much water to apply? (Liters)

The trained model is saved and can be loaded for prediction in the simulator.
"""

import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, mean_absolute_error, r2_score)

try:
    from xgboost import XGBClassifier, XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠ XGBoost not installed. Install with: pip install xgboost")


class IrrigationMLPipeline:
    """
    Complete ML pipeline for irrigation prediction.
    
    Handles:
    - Data loading and preprocessing
    - Feature encoding
    - Model training (Random Forest + XGBoost)
    - Model evaluation
    - Model saving/loading
    """
    
    def __init__(self, dataset_path: str = "irrigation_dataset.csv"):
        """
        Initialize ML pipeline.
        
        Args:
            dataset_path: Path to irrigation dataset CSV
        """
        self.dataset_path = dataset_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train_classifier = None
        self.y_test_classifier = None
        self.y_train_regressor = None
        self.y_test_regressor = None
        
        self.label_encoders = {}
        self.scaler = StandardScaler()
        
        self.classifier_model = None
        self.regressor_model = None
        self.best_classifier_name = None
        self.best_regressor_name = None
        
        self.results = {}
    
    def load_data(self):
        """Load dataset from CSV."""
        print("[*] Loading dataset...")
        self.df = pd.read_csv(self.dataset_path)
        print(f"    Loaded {len(self.df)} samples with {len(self.df.columns)} features")
    
    def preprocess_data(self, test_size: float = 0.2, random_state: int = 42):
        """
        Preprocess data: encode categorical features, split train/test.
        
        Args:
            test_size: Fraction of data for testing
            random_state: For reproducibility
        """
        print("[*] Preprocessing data...")
        
        df_processed = self.df.copy()
        
        # Encode categorical features
        categorical_features = ["crop", "location"]
        for feature in categorical_features:
            le = LabelEncoder()
            df_processed[feature] = le.fit_transform(df_processed[feature])
            self.label_encoders[feature] = le
        
        # Separate features and targets
        X = df_processed.drop(columns=["irrigation_amount", "irrigation_decision"])
        y_regressor = df_processed["irrigation_amount"]
        y_classifier = df_processed["irrigation_decision"]
        
        # Split dataset
        X_train, X_test, y_train_c, y_test_c, y_train_r, y_test_r = train_test_split(
            X, y_classifier, y_regressor, test_size=test_size, random_state=random_state
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Convert back to DataFrame to preserve feature names
        feature_names = X.columns
        self.X_train = pd.DataFrame(X_train_scaled, columns=feature_names)
        self.X_test = pd.DataFrame(X_test_scaled, columns=feature_names)
        
        self.y_train_classifier = y_train_c.values
        self.y_test_classifier = y_test_c.values
        self.y_train_regressor = y_train_r.values
        self.y_test_regressor = y_test_r.values
        
        print(f"    Train: {len(self.X_train)}, Test: {len(self.X_test)}")
        print(f"    Features: {list(feature_names)}")
    
    def train_classifier(self):
        """Train classification models."""
        print("[*] Training classification models (Should we irrigate?)...")
        
        # Random Forest Classifier
        print("    - Training Random Forest Classifier...")
        rf_clf = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced"
        )
        rf_clf.fit(self.X_train, self.y_train_classifier)
        rf_pred = rf_clf.predict(self.X_test)
        
        rf_accuracy = accuracy_score(self.y_test_classifier, rf_pred)
        rf_precision = precision_score(self.y_test_classifier, rf_pred, zero_division=0)
        rf_recall = recall_score(self.y_test_classifier, rf_pred, zero_division=0)
        rf_f1 = f1_score(self.y_test_classifier, rf_pred, zero_division=0)
        
        rf_results = {
            "model": rf_clf,
            "accuracy": rf_accuracy,
            "precision": rf_precision,
            "recall": rf_recall,
            "f1": rf_f1,
        }
        
        print(f"      Accuracy: {rf_accuracy:.4f}, F1: {rf_f1:.4f}")
        
        # XGBoost Classifier (if available)
        xgb_results = None
        if XGBOOST_AVAILABLE:
            print("    - Training XGBoost Classifier...")
            xgb_clf = XGBClassifier(
                n_estimators=200,
                max_depth=7,
                learning_rate=0.1,
                subsample=0.8,
                random_state=42,
                verbosity=0,
            )
            xgb_clf.fit(self.X_train, self.y_train_classifier)
            xgb_pred = xgb_clf.predict(self.X_test)
            
            xgb_accuracy = accuracy_score(self.y_test_classifier, xgb_pred)
            xgb_precision = precision_score(self.y_test_classifier, xgb_pred, zero_division=0)
            xgb_recall = recall_score(self.y_test_classifier, xgb_pred, zero_division=0)
            xgb_f1 = f1_score(self.y_test_classifier, xgb_pred, zero_division=0)
            
            xgb_results = {
                "model": xgb_clf,
                "accuracy": xgb_accuracy,
                "precision": xgb_precision,
                "recall": xgb_recall,
                "f1": xgb_f1,
            }
            
            print(f"      Accuracy: {xgb_accuracy:.4f}, F1: {xgb_f1:.4f}")
        
        # Select best classifier
        if xgb_results and xgb_results["f1"] > rf_results["f1"]:
            self.classifier_model = xgb_results["model"]
            self.best_classifier_name = "XGBoost"
            self.results["classifier"] = xgb_results
        else:
            self.classifier_model = rf_results["model"]
            self.best_classifier_name = "Random Forest"
            self.results["classifier"] = rf_results
        
        print(f"    ✓ Selected {self.best_classifier_name} as best classifier")
    
    def train_regressor(self):
        """Train regression models."""
        print("[*] Training regression models (How much water to apply?)...")
        
        # Random Forest Regressor
        print("    - Training Random Forest Regressor...")
        rf_reg = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        )
        rf_reg.fit(self.X_train, self.y_train_regressor)
        rf_pred = rf_reg.predict(self.X_test)
        
        rf_mae = mean_absolute_error(self.y_test_regressor, rf_pred)
        rf_r2 = r2_score(self.y_test_regressor, rf_pred)
        
        rf_results = {
            "model": rf_reg,
            "mae": rf_mae,
            "r2": rf_r2,
        }
        
        print(f"      MAE: {rf_mae:.2f}L, R²: {rf_r2:.4f}")
        
        # XGBoost Regressor (if available)
        xgb_results = None
        if XGBOOST_AVAILABLE:
            print("    - Training XGBoost Regressor...")
            xgb_reg = XGBRegressor(
                n_estimators=200,
                max_depth=7,
                learning_rate=0.1,
                subsample=0.8,
                random_state=42,
                verbosity=0,
            )
            xgb_reg.fit(self.X_train, self.y_train_regressor)
            xgb_pred = xgb_reg.predict(self.X_test)
            
            xgb_mae = mean_absolute_error(self.y_test_regressor, xgb_pred)
            xgb_r2 = r2_score(self.y_test_regressor, xgb_pred)
            
            xgb_results = {
                "model": xgb_reg,
                "mae": xgb_mae,
                "r2": xgb_r2,
            }
            
            print(f"      MAE: {xgb_mae:.2f}L, R²: {xgb_r2:.4f}")
        
        # Select best regressor
        if xgb_results and xgb_results["r2"] > rf_results["r2"]:
            self.regressor_model = xgb_results["model"]
            self.best_regressor_name = "XGBoost"
            self.results["regressor"] = xgb_results
        else:
            self.regressor_model = rf_results["model"]
            self.best_regressor_name = "Random Forest"
            self.results["regressor"] = rf_results
        
        print(f"    ✓ Selected {self.best_regressor_name} as best regressor")
    
    def save_models(self, output_dir: str = None):
        """Save trained models to pickle files."""
        if output_dir is None:
            output_dir = Path(__file__).parent
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("[*] Saving models...")
        
        # Save classifier
        classifier_path = output_dir / "irrigation_classifier.pkl"
        with open(classifier_path, "wb") as f:
            pickle.dump(self.classifier_model, f)
        print(f"    ✓ Classifier saved: {classifier_path}")
        
        # Save regressor
        regressor_path = output_dir / "irrigation_regressor.pkl"
        with open(regressor_path, "wb") as f:
            pickle.dump(self.regressor_model, f)
        print(f"    ✓ Regressor saved: {regressor_path}")
        
        # Save preprocessing objects
        preprocessing_path = output_dir / "irrigation_preprocessing.pkl"
        preprocessing = {
            "scaler": self.scaler,
            "label_encoders": self.label_encoders,
        }
        with open(preprocessing_path, "wb") as f:
            pickle.dump(preprocessing, f)
        print(f"    ✓ Preprocessing saved: {preprocessing_path}")
        
        # Save metadata
        metadata_path = output_dir / "irrigation_metadata.pkl"
        metadata = {
            "classifier_name": self.best_classifier_name,
            "regressor_name": self.best_regressor_name,
            "feature_names": list(self.X_train.columns),
            "classifier_results": self.results.get("classifier", {}),
            "regressor_results": self.results.get("regressor", {}),
        }
        with open(metadata_path, "wb") as f:
            pickle.dump(metadata, f)
        print(f"    ✓ Metadata saved: {metadata_path}")
    
    def print_summary(self):
        """Print training summary."""
        print("\n" + "=" * 70)
        print("TRAINING SUMMARY")
        print("=" * 70)
        
        print(f"\nClassifier ({self.best_classifier_name}):")
        for key, value in self.results.get("classifier", {}).items():
            if key != "model":
                if isinstance(value, float):
                    print(f"  {key}: {value:.4f}")
                else:
                    print(f"  {key}: {value}")
        
        print(f"\nRegressor ({self.best_regressor_name}):")
        for key, value in self.results.get("regressor", {}).items():
            if key != "model":
                if isinstance(value, float):
                    print(f"  {key}: {value:.4f}")
                else:
                    print(f"  {key}: {value}")
        
        print("\n" + "=" * 70)


def main():
    """Main training pipeline."""
    print("=" * 70)
    print("IRRIGATION ML MODEL TRAINING")
    print("=" * 70)
    
    # Initialize pipeline
    pipeline = IrrigationMLPipeline(dataset_path="irrigation_dataset.csv")
    
    # Load and preprocess data
    pipeline.load_data()
    pipeline.preprocess_data()
    
    # Train models
    pipeline.train_classifier()
    pipeline.train_regressor()
    
    # Save models
    pipeline.save_models()
    
    # Print summary
    pipeline.print_summary()
    
    print("\n✓ Training complete! Models ready for inference.")


if __name__ == "__main__":
    main()
