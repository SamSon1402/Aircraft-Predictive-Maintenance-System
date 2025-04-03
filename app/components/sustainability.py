import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from app.utils.visualization import update_chart_style
import app.config as config

def render():
    """Render the sustainability component"""
    # Sustainability container
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="header">Environmental Impact</div>', unsafe_allow_html=True)
    
    st.markdown('''
    <div style="color:#d0d0d0; margin-bottom:20px;">
        Predictive maintenance directly supports SITA's mission to reduce the aviation sector's CO₂ emissions
        through data-driven solutions.
    </div>
    ''', unsafe_allow_html=True)
    
    # Calculator inputs
    st.markdown("### Impact Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fleet_size = st.slider("Fleet Size", 10, 500, 100)
    
    with col2:
        engines_per_aircraft = st.slider("Engines per Aircraft", 2, 4, 2)
    
    with col3:
        flight_hours = st.slider("Flight Hours/Year", 2000, 6000, 3500)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        maintenance_improvement = st.slider("Efficiency Improvement (%)", 0.5, 5.0, 2.0, 0.1)
    
    with col2:
        fuel_per_hour = st.slider("Fuel per Engine (kg/h)", 800, 3000, 2000)
    
    with col3:
        co2_per_kg_fuel = st.slider("CO₂ per kg of Fuel", 3.0, 3.2, 3.16, 0.01)
    
    # Calculate impact
    total_engines = fleet_size * engines_per_aircraft
    annual_fuel_per_engine = flight_hours * fuel_per_hour
    total_annual_fuel = total_engines * annual_fuel_per_engine
    fuel_saved = total_annual_fuel * (maintenance_improvement / 100)
    co2_saved = fuel_saved * co2_per_kg_fuel
    
    # Display results
    st.markdown("### Annual Impact")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Fuel Saved", f"{fuel_saved/1000:,.1f} tonnes")
    
    with col2:
        st.metric("CO₂ Reduced", f"{co2_saved/1000:,.1f} tonnes")
    
    with col3:
        trees_equivalent = int(co2_saved / 25)  # Approx 25kg CO2 per tree per year
        st.metric("Tree Equivalent", f"{trees_equivalent:,} trees")
    
    st.markdown('</div>', unsafe_allow_html=True)