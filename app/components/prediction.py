import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from app.utils.data_processing import load_data
from app.utils.model import train_model
from app.utils.visualization import update_chart_style

def render():
    """Render the prediction component"""
    # Prediction container
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="header">RUL Prediction Engine</div>', unsafe_allow_html=True)
    
    # Load data
    train_data = load_data()
    
    # Train model
    with st.spinner("Training machine learning model..."):
        model, scaler, importance = train_model(train_data)
    
    # Display feature importance
    st.markdown("### Feature Importance")
    
    fig = px.bar(
        importance.head(10),
        x='Importance',
        y='Feature',
        orientation='h',
        title="Top 10 Most Important Sensors",
        color='Importance',
        color_continuous_scale='Viridis'
    )
    
    # Apply styling
    fig = update_chart_style(fig)
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Prediction interface
    st.markdown("### Predict Remaining Useful Life")
    
    # Engine selection
    engine_options = sorted(train_data['unit_number'].unique())
    selected_engine = st.selectbox("Select Engine", engine_options, key="pred_engine")
    
    if selected_engine:
        # Get engine data
        engine_data = train_data[train_data['unit_number'] == selected_engine]
        
        # Select cycle
        max_cycle = engine_data['cycle'].max()
        cycle = st.slider("Select Operating Cycle", 1, int(max_cycle), int(max_cycle//2))
        
        # Get data for that cycle
        cycle_data = engine_data[engine_data['cycle'] == cycle]
        
        if not cycle_data.empty:
            # Make prediction
            st.write(f"Predictions for Engine #{selected_engine} at cycle {cycle} will appear here")
    
    st.markdown('</div>', unsafe_allow_html=True)