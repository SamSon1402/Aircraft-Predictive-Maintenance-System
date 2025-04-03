import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from app.utils.data_processing import load_data
from app.utils.visualization import create_health_distribution_chart

def render():
    """Render the dashboard component"""
    # Dashboard container
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="header">Fleet Status Overview</div>', unsafe_allow_html=True)
    
    # Load data
    train_data = load_data()
    
    # Calculate metrics
    total_engines = train_data['unit_number'].nunique()
    avg_lifecycle = train_data.groupby('unit_number')['cycle'].max().mean().round(1)
    
    # Get min RUL for each engine
    engine_min_rul = train_data.groupby('unit_number')['RUL'].min().reset_index()
    critical_engines = len(engine_min_rul[engine_min_rul['RUL'] < 30])
    
    # Calculate maintenance cost savings
    unscheduled_cost = 250000  # $ per event
    scheduled_cost = 75000     # $ per event
    potential_savings = critical_engines * (unscheduled_cost - scheduled_cost)
    
    # Display metrics
    st.markdown(f'''
    <div class="metric-container">
        <div class="metric-card">
            <div class="metric-value">{total_engines}</div>
            <div class="metric-label">Fleet Size</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{avg_lifecycle}</div>
            <div class="metric-label">Avg Lifecycle (cycles)</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{critical_engines}</div>
            <div class="metric-label">Critical Engines</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${potential_savings:,}</div>
            <div class="metric-label">Potential Savings</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Health status distribution
    engine_min_rul['Status'] = pd.cut(
        engine_min_rul['RUL'],
        bins=[0, 20, 50, 100, 200, 1000],
        labels=['Critical', 'Warning', 'Moderate', 'Good', 'Excellent']
    )
    
    status_counts = engine_min_rul['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    status_order = ['Critical', 'Warning', 'Moderate', 'Good', 'Excellent']
    
    # Create and display the chart
    fig = create_health_distribution_chart(status_counts, status_order)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('</div>', unsafe_allow_html=True)