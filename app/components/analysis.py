import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from app.utils.data_processing import load_data
from app.utils.visualization import update_chart_style, create_themed_line_chart

def render():
    """Render the analysis component"""
    # Analysis container
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="header">Engine Degradation Analysis</div>', unsafe_allow_html=True)
    
    # Load data
    train_data = load_data()
    
    # Feature correlation analysis
    sensor_cols = [col for col in train_data.columns if 'sensor' in col]
    
    if len(sensor_cols) > 0:
        # Calculate correlations with RUL
        correlations = train_data[sensor_cols + ['RUL']].corr()['RUL'].drop('RUL').abs().sort_values(ascending=False)
        
        # Plot correlations in a bar chart
        fig = px.bar(
            x=correlations.index,
            y=correlations.values,
            title="Sensor Correlations with RUL",
            labels={'x': 'Sensor', 'y': 'Absolute Correlation'},
            color=correlations.values,
            color_continuous_scale='Viridis'
        )
        
        # Apply the styling
        fig = update_chart_style(fig)
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Top correlated sensors
        top_sensors = correlations.index[:3].tolist()
        
        # Display top correlations
        st.markdown("### Top sensors for degradation monitoring:")
        for i, sensor in enumerate(top_sensors):
            st.write(f"{sensor}: {correlations.iloc[i]:.3f} correlation")
    
    st.markdown('</div>', unsafe_allow_html=True)