import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
from datetime import datetime

def train_crop_recommendation():
    """Train crop recommendation model"""
    try:
        print("\n=== Training Crop Recommendation Model ===")
        df = pd.read_csv('dataset/Crop_recommendation.csv')
        print(f"Loaded {len(df)} records")
        
        X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
        y = df['label']
        
        # Split and train
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Save model
        model_path = 'models/crop/model.joblib'
        joblib.dump(model, model_path)
        print(f"Model saved to {model_path}")
        print(f"Test Accuracy: {model.score(X_test, y_test):.4f}")
        return True
        
    except Exception as e:
        print(f"Error in crop recommendation training: {str(e)}")
        return False

def train_market_price():
    """Train market price prediction model"""
    try:
        print("\n=== Training Market Price Model ===")
        df = pd.read_csv('dataset/crop_production.csv')
        print(f"Loaded {len(df)} records")
        
        # Preprocessing
        df = df.dropna()
        le_crop = LabelEncoder()
        le_district = LabelEncoder()
        
        X = pd.DataFrame({
            'crop': le_crop.fit_transform(df['Crop']),
            'district': le_district.fit_transform(df['District_Name']),
            'season': df['Season'].map({'Kharif': 0, 'Rabi': 1, 'Whole Year': 2, 'Summer': 3}).fillna(-1),
            'area': df['Area']
        })
        y = df['Production']
        
        # Split and train
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Save model and encoders
        model_path = 'models/market/'
        os.makedirs(model_path, exist_ok=True)
        joblib.dump(model, os.path.join(model_path, 'model.joblib'))
        joblib.dump(le_crop, os.path.join(model_path, 'crop_encoder.joblib'))
        joblib.dump(le_district, os.path.join(model_path, 'district_encoder.joblib'))
        
        print(f"Model saved to {model_path}")
        print(f"Test R² Score: {model.score(X_test, y_test):.4f}")
        return True
        
    except Exception as e:
        print(f"Error in market price training: {str(e)}")
        return False

def train_disaster_management():
    """Train disaster management model"""
    try:
        print("\n=== Training Disaster Management Model ===")
        # Load and combine disaster datasets
        rainfall = pd.read_csv('dataset/disastermanagement/rainfall in india 1901-2015.csv')
        district_rain = pd.read_csv('dataset/disastermanagement/district wise rainfall normal.csv')
        
        print("Original rainfall data shape:", rainfall.shape)
        print("Missing values before cleaning:")
        print(rainfall.isnull().sum())
        
        # Handle missing values by filling with column mean
        rainfall = rainfall.fillna(rainfall.mean(numeric_only=True))
        
        # Create target variable: 1 if annual rainfall is in top 10%, else 0
        rainfall['is_flood_risk'] = (rainfall['ANNUAL'] > rainfall['ANNUAL'].quantile(0.9)).astype(int)
        
        # Select features - using monthly rainfall data
        features = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 
                   'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        
        X = rainfall[features]
        y = rainfall['is_flood_risk']
        
        print("\nClass distribution:", y.value_counts())
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model with balanced class weights
        model = RandomForestClassifier(
            n_estimators=100, 
            random_state=42,
            class_weight='balanced',
            n_jobs=-1  # Use all CPU cores
        )
        
        print("\nTraining model...")
        model.fit(X_train, y_train)
        
        # Calculate metrics
        train_accuracy = model.score(X_train, y_train)
        test_accuracy = model.score(X_test, y_test)
        
        # Save model and metadata
        model_path = 'models/disaster/'
        os.makedirs(model_path, exist_ok=True)
        
        joblib.dump(model, os.path.join(model_path, 'model.joblib'))
        joblib.dump(features, os.path.join(model_path, 'features.joblib'))
        
        print(f"\nModel saved to {model_path}")
        print(f"Training Accuracy: {train_accuracy:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f}")
        
        # Feature importance
        importances = model.feature_importances_
        print("\nFeature Importances:")
        for feature, importance in zip(features, importances):
            print(f"{feature}: {importance:.4f}")
            
        return True
        
    except Exception as e:
        import traceback
        print(f"Error in disaster management training: {str(e)}")
        print("Traceback:", traceback.format_exc())
        return False

def train_govt_schemes():
    """Train government scheme analysis model"""
    try:
        print("\n=== Training Government Scheme Analysis Model ===")
        # Load the dataset
        df = pd.read_csv('dataset/govtschemes.csv')
        print(f"Loaded data with shape: {df.shape}")
        
        # Basic data cleaning
        df = df[df['State/UT'] != 'Grand Total']  # Remove summary row
        df = df[df['State/UT'] != 'Grand Total ']  # Some files might have trailing space
        
        # Get all unique states
        states = df['State/UT'].unique()
        print(f"Found {len(states)} states/UTs")
        
        # Save the processed data and state list
        model_path = 'models/schemes/'
        os.makedirs(model_path, exist_ok=True)
        
        # Save the preprocessed data
        df.to_csv(os.path.join(model_path, 'schemes_processed.csv'), index=False)
        joblib.dump(states, os.path.join(model_path, 'states.joblib'))
        
        # Create a summary of schemes by state
        scheme_columns = [col for col in df.columns if 'Instalment' in col and 'No. of Beneficiaries' in col]
        scheme_summary = df[['State/UT'] + scheme_columns].copy()
        
        # Convert beneficiary counts to numeric, handling any non-numeric values
        for col in scheme_columns:
            scheme_summary[col] = pd.to_numeric(scheme_summary[col], errors='coerce')
        
        # Calculate total beneficiaries per state
        scheme_summary['Total_Beneficiaries'] = scheme_summary[scheme_columns].sum(axis=1)
        
        # Save the summary
        scheme_summary.to_csv(os.path.join(model_path, 'scheme_summary.csv'), index=False)
        
        print(f"\nModel artifacts saved to {model_path}")
        print("Available data for analysis:")
        print(f"- {len(scheme_columns)} different scheme periods")
        print(f"- {len(states)} states/UTs")
        print("\nSample of the processed data:")
        print(scheme_summary[['State/UT', 'Total_Beneficiaries']].head())
        
        return True
        
    except Exception as e:
        import traceback
        print(f"Error in government scheme training: {str(e)}")
        print("Traceback:", traceback.format_exc())
        return False

def main():
    print(f"\n{'='*50}")
    print("Starting Model Training Pipeline")
    print(f"{'='*50}")
    
    start_time = datetime.now()
    results = {
        'crop': train_crop_recommendation(),
        'market': train_market_price(),
        'disaster': train_disaster_management(),
        'schemes': train_govt_schemes()
    }
    
    # Print summary
    print("\n" + "="*50)
    print("Training Summary:")
    for model, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"{model.upper()}: {status}")
    
    print(f"\nTotal time taken: {datetime.now() - start_time}")
    print("="*50)

if __name__ == "__main__":
    main()
