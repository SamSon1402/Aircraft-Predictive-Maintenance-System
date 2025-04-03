import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler
import app.config as config

@st.cache_data
def load_data():
    """Load and preprocess the dataset"""
    try:
        train_data = pd.read_csv(config.DATA_PATH)
        return train_data
    except:
        # Create sample data if file doesn't exist
        st.warning("Could not load data file. Using synthetic data instead.")
        return create_synthetic_data()

def create_synthetic_data():
    """Create synthetic data for demonstration purposes"""
    engines = 100
    cycles_per_engine = 200
    
    data = []
    for engine in range(1, engines + 1):
        max_cycle = np.random.randint(100, 300)
        for cycle in range(1, max_cycle + 1):
            # Create synthetic sensor readings
            row = {
                'unit_number': engine,
                'cycle': cycle,
                'max_cycle': max_cycle,
                'RUL': max_cycle - cycle
            }
            
            # Add synthetic sensor readings
            for i in range(1, 20):
                base_value = np.random.uniform(100, 1000)
                noise = np.random.normal(0, base_value * 0.01)
                degradation = cycle / max_cycle * np.random.uniform(0, base_value * 0.2)
                row[f'sensor_{i}'] = base_value + noise + degradation
            
            data.append(row)
    
    return pd.DataFrame(data)

def preprocess_data(data):
    """Preprocess data for model training"""
    # Get sensor columns
    sensor_cols = [col for col in data.columns if 'sensor' in col]
    
    # Create feature matrix and target
    X = data[sensor_cols]
    y = data['RUL']
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y, scaler, sensor_cols