import pandas as pd
import numpy as np
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from app.utils.data_processing import preprocess_data

@st.cache_resource
def train_model(data):
    """Train a machine learning model for RUL prediction"""
    # Preprocess data
    X_scaled, y, scaler, sensor_cols = preprocess_data(data)
    
    # Train model
    model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
    model.fit(X_scaled, y)
    
    # Get feature importance
    importance = pd.DataFrame({
        'Feature': sensor_cols,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    return model, scaler, importance

def predict_rul(model, scaler, engine_data, cycle, sensor_cols):
    """Predict RUL for a specific engine at a specific cycle"""
    # Get data for that cycle
    cycle_data = engine_data[engine_data['cycle'] == cycle]
    
    if not cycle_data.empty and set(sensor_cols).issubset(cycle_data.columns):
        features = cycle_data[sensor_cols].values
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        
        return prediction
    
    return None