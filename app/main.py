import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import base64
from datetime import datetime
import time

# Configure the page
st.set_page_config(
    page_title="Aircraft Predictive Maintenance",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Bright neon color palette for charts
chart_colors = {
    'Critical': '#ff3333',  # Bright red
    'Warning': '#ffaa00',   # Bright orange
    'Moderate': '#ffff00',  # Bright yellow
    'Good': '#33ff33',      # Bright green
    'Excellent': '#33ffff', # Bright cyan
    'accent': '#9966ff',    # Bright purple
    'accent2': '#ff66ff',   # Bright magenta
    'highlight': '#ffffff'  # White
}

# Custom CSS for dark theme and animations
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        filter: brightness(0.4) contrast(1.2);
        mix-blend-mode: darken;
        z-index: -1;
    }
    
    .stApp {
        background-color: rgba(0, 0, 0, 0.85);  /* Much darker base layer */
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# CSS for styling and animations
st.markdown("""
<style>
    /* Improved main container - more opaque */
    .main {
        background-color: rgba(10, 10, 18, 0.95);
        border-radius: 10px;
        padding: 20px;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(100, 100, 140, 0.6);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
    }
    
    /* More solid containers for better readability */
    .container {
        background-color: rgba(15, 15, 25, 0.97);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 3px solid rgba(140, 131, 255, 0.8);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    }
    
    /* Higher contrast for headers */
    .header {
        color: #ffffff;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(140, 131, 255, 0.7);
        padding-bottom: 8px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        letter-spacing: 0.5px;
    }
    
    /* Dashboard metrics - dark background with light text */
    .metric-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 15px;
    }
    
    /* Solid metric cards for better visibility */
    .metric-card {
        background-color: rgba(15, 15, 25, 0.98);
        border-radius: 8px;
        padding: 15px;
        width: 23%;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(100, 100, 140, 0.6);
    }
    
    /* Brighter metric values */
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 5px;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }
    
    /* Brighter label text */
    .metric-label {
        font-size: 14px;
        color: #e0e0e0;
        font-weight: 500;
    }
    
    /* Plane animation */
    @keyframes fly {
        0% {
            transform: translateX(-100px) translateY(20px);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateX(calc(100vw + 100px)) translateY(-50px);
            opacity: 0;
        }
    }
    
    .plane {
        position: fixed;
        top: 100px;
        left: 0;
        font-size: 30px;
        color: white;
        animation: fly 15s linear infinite;
        z-index: 1000;
    }
    
    /* Status indicators - brighter colors for better visibility */
    .status-critical {
        color: #ff5555; /* Bright red for critical */
        font-weight: bold;
        font-size: 16px;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }
    
    .status-warning {
        color: #ffaa55; /* Bright orange for warning */
        font-weight: bold;
        font-size: 16px;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }
    
    .status-good {
        color: #55ff55; /* Bright green for good */
        font-weight: bold;
        font-size: 16px;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }
    
    /* Make all Streamlit elements completely solid */
    div.stPlotlyChart, div.stSelectbox, button, div.stSlider, div.stText, div.stMarkdown, div.stDataFrame {
        background-color: rgba(15, 15, 25, 0.98) !important;
        border-radius: 8px;
        border: 1px solid rgba(100, 100, 140, 0.6);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
    }
    
    /* Enhanced tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 15, 25, 0.95);
        border-radius: 8px;
        padding: 5px;
        border: 1px solid rgba(100, 100, 140, 0.4);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(25, 25, 40, 0.98);
        border-radius: 5px 5px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #e0e0e0;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(45, 45, 70, 0.98);
        border-bottom: 3px solid #9966ff;
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Ensure text in widgets is visible */
    input, select, textarea, .stSelectbox, .stMultiSelect {
        color: #ffffff !important;
    }
    
    /* Button styling */
    button, .stButton button {
        background-color: rgba(45, 45, 70, 0.95) !important;
        color: #ffffff !important;
        border: 1px solid rgba(140, 131, 255, 0.5) !important;
    }
    
    button:hover, .stButton button:hover {
        background-color: rgba(60, 60, 90, 0.95) !important;
        border-color: rgba(140, 131, 255, 0.8) !important;
    }
    
    /* Add a subtle text shadow to all text for better readability over the background */
    .stMarkdown, .stText, h1, h2, h3, p, span {
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    /* Ensure all text is highly visible */
    p, span, div, h1, h2, h3, h4, h5, h6, li {
        color: #ffffff !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.9) !important;
    }
    
    /* Better label visibility */
    label {
        color: #ffffff !important;
        font-weight: 500 !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.9) !important;
    }
</style>

<!-- Plane animation -->
<div class="plane">✈️</div>
""", unsafe_allow_html=True)

# Update chart styling function
def update_chart_style(fig):
    """Apply a high contrast style to Plotly charts"""
    fig.update_layout(
        plot_bgcolor='rgba(5, 5, 15, 0.95)',  # Almost solid dark background
        paper_bgcolor='rgba(5, 5, 15, 0)',
        font=dict(
            color='#ffffff',
            size=14
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(180, 180, 230, 0.3)',  # Brighter grid lines
            gridwidth=1,
            zeroline=False,
            color='#ffffff',
            title_font=dict(size=14, color='#ffffff')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(180, 180, 230, 0.3)',  # Brighter grid lines
            gridwidth=1,
            zeroline=False,
            color='#ffffff',
            title_font=dict(size=14, color='#ffffff')
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        title=dict(
            font=dict(
                size=18, 
                color='#ffffff'
            )
        )
    )
    
    # Make sure the chart has a border and shadow for better definition
    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color="rgba(140, 131, 255, 0.6)",
                    width=1,
                ),
                fillcolor="rgba(0, 0, 0, 0)"
            )
        ]
    )
    
    return fig

# Update line chart function for better visibility
def create_themed_line_chart(data, x, y, title):
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        markers=True
    )
    # Thicker lines and larger markers
    fig.update_traces(line=dict(color=chart_colors['accent'], width=4))
    fig.update_traces(marker=dict(color=chart_colors['accent2'], size=10, line=dict(width=2, color='#ffffff')))
    return update_chart_style(fig)

# Add threshold line with higher visibility
def add_threshold_line(fig, y_value, text="Critical Threshold"):
    fig.add_hline(
        y=y_value,
        line_dash="dash",
        line_color=chart_colors['Critical'],
        line_width=3,
        annotation_text=text,
        annotation_font=dict(color=chart_colors['highlight'], size=16),
        annotation_bgcolor="rgba(5, 5, 15, 0.9)"
    )
    return fig

# Create a status card with appropriate styling
def create_status_card(status, rul_value):
    """Create a high-contrast status card with appropriate styling based on RUL value"""
    if rul_value < 20:
        status_class = "status-critical"
        status_text = "CRITICAL"
        border_color = "#ff3333"
        bg_color = "rgba(40, 0, 0, 0.95)"
    elif rul_value < 50:
        status_class = "status-warning"
        status_text = "WARNING"
        border_color = "#ffaa00"
        bg_color = "rgba(40, 20, 0, 0.95)"
    else:
        status_class = "status-good"
        status_text = "GOOD"
        border_color = "#33ff33"
        bg_color = "rgba(0, 40, 0, 0.95)"
    
    return f'''
    <div style="background-color: {bg_color}; padding:15px; border-radius:8px; border-left: 4px solid {border_color}; margin-bottom: 15px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6); border: 1px solid {border_color};">
        <span style="font-size:18px; color: #ffffff;">Status: <span class="{status_class}">{status_text}</span></span>
        <br>
        <span style="color:#ffffff; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">Remaining Useful Life: {rul_value} cycles</span>
    </div>
    '''

# Enhanced parameter display with more solid background and colorful parameters
def create_parameter_display(parameters):
    """Create a styled parameter display with high contrast for key-value pairs"""
    html = '''
    <div style="background-color: rgba(5, 5, 15, 0.95); padding:15px; border-radius:8px; margin-top:15px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6); border: 1px solid rgba(140, 131, 255, 0.6);">
    <table style="width:100%;">
    '''
    
    for key, value in parameters.items():
        html += f'''
        <tr>
            <td style="padding:10px; color:#9966ff; font-weight:bold; width:40%; border-bottom: 1px solid rgba(140, 131, 255, 0.4); text-shadow: 0 1px 2px rgba(0,0,0,0.9);">{key}</td>
            <td style="padding:10px; color:#ffffff; width:60%; border-bottom: 1px solid rgba(140, 131, 255, 0.4); text-shadow: 0 1px 2px rgba(0,0,0,0.9);">{value}</td>
        </tr>
        '''
    
    html += '''
    </table>
    </div>
    '''
    return html

# Enhanced prediction display with solid background and bold values
def create_prediction_display(value, label, color="#9966ff"):
    return f'''
    <div style="background-color: rgba(5, 5, 15, 0.95); padding:20px; border-radius:8px; text-align:center; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6); border: 1px solid rgba(140, 131, 255, 0.6);">
        <div style="font-size:16px; color:#ffffff; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">{label}</div>
        <div style="font-size:32px; font-weight:bold; color:{color}; text-shadow: 0 2px 4px rgba(0,0,0,0.9);">{value}</div>
    </div>
    '''

# Enhanced maintenance recommendation boxes
def create_maintenance_recommendation(prediction):
    if prediction <= 30:
        return f'''
        <div style="background-color:rgba(40, 0, 0, 0.95); border-left:4px solid #ff3333; padding:15px; border-radius:4px; margin-top:20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6); border: 1px solid #ff3333;">
            <div style="font-size:18px; color:#ff3333; font-weight:bold; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">🚨 CRITICAL: IMMEDIATE MAINTENANCE REQUIRED</div>
            <div style="color:#ffffff; margin-top:10px; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">
                Engine is approaching end of useful life. Schedule maintenance within the next 30 cycles to prevent failure.
            </div>
        </div>
        '''
    elif prediction <= 70:
        return f'''
        <div style="background-color:rgba(40, 20, 0, 0.95); border-left:4px solid #ffaa00; padding:15px; border-radius:4px; margin-top:20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6); border: 1px solid #ffaa00;">
            <div style="font-size:18px; color:#ffaa00; font-weight:bold; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">⚠️ WARNING: MAINTENANCE REQUIRED SOON</div>
            <div style="color:#ffffff; margin-top:10px; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">
                Engine is showing early signs of degradation. Plan for maintenance within the next 50-60 cycles.
            </div>
        </div>
        '''
    else:
        return f'''
        <div style="background-color:rgba(0, 40, 0, 0.95); border-left:4px solid #33ff33; padding:15px; border-radius:4px; margin-top:20px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6); border: 1px solid #33ff33;">
            <div style="font-size:18px; color:#33ff33; font-weight:bold; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">✅ HEALTHY: NO IMMEDIATE ACTION REQUIRED</div>
            <div style="color:#ffffff; margin-top:10px; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">
                Engine is in good condition. Continue with standard operation procedures.
            </div>
        </div>
        '''

# Enhanced mission connection box
def create_mission_box():
    return '''
    <div style="background-color:rgba(25, 25, 50, 0.95); border-left:4px solid #9966ff; padding:15px; border-radius:4px; margin-top:30px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6); border: 1px solid #9966ff;">
        <div style="font-size:18px; color:#ffffff; font-weight:bold; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">SITA's Sustainability Mission</div>
        <div style="color:#ffffff; margin-top:10px; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">
            This predictive maintenance system directly supports SITA's Data Intelligence team's goal to develop 
            "data-driven and AI-powered solutions to optimize operations in the aviation industry, with a specific 
            focus on reducing the sector's CO₂ emissions."
        </div>
    </div>
    '''

# Enhanced sustainability metrics
def create_sustainability_metric(label, value, color="#33ffff"):
    return f'''
    <div style="background-color:rgba(5, 5, 15, 0.95); padding:20px; border-radius:8px; text-align:center; border: 1px solid {color}; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6);">
        <div style="font-size:16px; color:#ffffff; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">{label}</div>
        <div style="font-size:26px; font-weight:bold; color:{color}; text-shadow: 0 2px 4px rgba(0,0,0,0.9);">{value}</div>
    </div>
    '''

# Update the health distribution chart
def create_health_distribution_chart(status_counts, status_order):
    fig = px.bar(
        status_counts,
        y='Status',
        x='Count',
        color='Status',
        color_discrete_map={
            'Critical': chart_colors['Critical'],
            'Warning': chart_colors['Warning'],
            'Moderate': chart_colors['Moderate'],
            'Good': chart_colors['Good'],
            'Excellent': chart_colors['Excellent']
        },
        category_orders={'Status': status_order},
        orientation='h',
        title="Engine Health Distribution"
    )
    
    # Apply the enhanced styling
    fig = update_chart_style(fig)
    
    return fig

# Enhanced sensor comparison chart
def create_sensor_comparison_chart(data_frames, sensor_name):
    fig = go.Figure()
    
    # Use a color cycle for different engines
    colors = [chart_colors['accent'], chart_colors['accent2'], 
              chart_colors['Critical'], chart_colors['Good'], 
              chart_colors['Warning'], chart_colors['Moderate']]
    
    for i, (engine, df) in enumerate(data_frames.items()):
        color_idx = i % len(colors)
        fig.add_trace(
            go.Scatter(
                x=df['cycle'],
                y=df[sensor_name],
                mode='lines',
                name=f'Engine {engine}',
                line=dict(color=colors[color_idx], width=3),
            )
        )
    
    # Apply the styling
    fig = update_chart_style(fig)
    fig.update_layout(
        title=f"{sensor_name} Values Across Selected Engines",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#ffffff")
        )
    )
    
    return fig

# Enhanced correlation chart
def create_correlation_chart(correlations):
    fig = px.bar(
        x=correlations.index,
        y=correlations.values,
        title="Sensor Correlations with RUL",
        labels={'x': 'Sensor', 'y': 'Absolute Correlation'},
        color=correlations.values,
        color_continuous_scale=[
            [0, chart_colors['Good']],
            [0.5, chart_colors['Warning']],
            [1, chart_colors['accent']]
        ]
    )
    
    # Apply the styling
    fig = update_chart_style(fig)
    
    return fig

# Enhanced feature importance chart
def create_feature_importance_chart(importance_df):
    fig = px.bar(
        importance_df.head(10),
        x='Importance',
        y='Feature',
        orientation='h',
        title="Top 10 Most Important Sensors",
        color='Importance',
        color_continuous_scale=[
            [0, chart_colors['Good']],
            [0.5, chart_colors['Warning']],
            [1, chart_colors['accent']]
        ]
    )
    
    # Apply the styling
    fig = update_chart_style(fig)
    
    return fig

# Enhanced gauge styling
def create_rul_gauge(prediction, actual_rul):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=prediction,
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={
            'reference': actual_rul, 
            'increasing': {'color': chart_colors['Good']}, 
            'decreasing': {'color': chart_colors['Critical']},
            'font': {'size': 16}
        },
        number={'font': {'size': 24, 'color': '#ffffff'}},
        gauge={
            'axis': {
                'range': [0, 200], 
                'tickwidth': 1, 
                'tickcolor': "#ffffff",
                'tickfont': {'color': '#ffffff'}
            },
            'bar': {'color': chart_colors['accent']},
            'bgcolor': "rgba(5, 5, 15, 0.5)",
            'borderwidth': 2,
            'bordercolor': "rgba(140, 140, 190, 0.6)",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(255, 51, 51, 0.6)'},   # Bright red with opacity
                {'range': [30, 70], 'color': 'rgba(255, 170, 0, 0.6)'},  # Bright orange with opacity
                {'range': [70, 120], 'color': 'rgba(255, 255, 0, 0.6)'}, # Bright yellow with opacity
                {'range': [120, 200], 'color': 'rgba(51, 255, 51, 0.6)'} # Bright green with opacity
            ],
            'threshold': {
                'line': {'color': chart_colors['Critical'], 'width': 4},
                'thickness': 0.75,
                'value': 30
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(5, 5, 15, 0)',
        font=dict(color='#ffffff'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    
    return fig

# Enhanced emissions comparison chart
def create_emissions_chart(emissions_data, co2_saved):
    fig = px.bar(
        emissions_data,
        x='Scenario',
        y='CO₂ Emissions (tonnes)',
        color='Scenario',
        color_discrete_map={
            'Without Predictive Maintenance': chart_colors['Critical'],
            'With Predictive Maintenance': chart_colors['Good']
        },
        title="CO₂ Emissions Comparison"
    )
    
    fig.add_annotation(
        x=1,
        y=(emissions_data['CO₂ Emissions (tonnes)'][1] + 
           (emissions_data['CO₂ Emissions (tonnes)'][0] - emissions_data['CO₂ Emissions (tonnes)'][1])/2),
        text=f"Reduction: {co2_saved/1000:,.1f} tonnes",
        showarrow=True,
        arrowhead=1,
        font=dict(size=16, color="#ffffff"),
        bgcolor="rgba(5, 5, 15, 0.8)",
        bordercolor="#ffffff",
        borderwidth=1
    )
    
    # Apply the styling
    fig = update_chart_style(fig)
    
    return fig

# Load the data 
@st.cache_data
def load_data():
    try:
        train_data = pd.read_csv('data/fixed_train_FD001.csv')
        return train_data
    except:
        # Create sample data if file doesn't exist
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

# Load data
train_data = load_data()

# Train a model
@st.cache_resource
def train_model(data):
    # Get feature columns
    sensor_cols = [col for col in data.columns if 'sensor' in col]
    
    # Create training data
    X = data[sensor_cols]
    y = data['RUL']
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train a model
    model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
    model.fit(X_scaled, y)
    
    # Get feature importance
    importance = pd.DataFrame({
        'Feature': sensor_cols,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    return model, scaler, importance

# Minimalist navigation
tabs = ["Dashboard", "Analysis", "Prediction", "Sustainability"]
selected_tab = st.sidebar.radio("Navigation", tabs, label_visibility="collapsed")

# Main content container
st.markdown('<div class="main">', unsafe_allow_html=True)

# Title with minimal styling
st.markdown("<h1 style='color:#ffffff; font-size:32px; margin-bottom:30px; text-align:center; text-shadow: 0 2px 4px rgba(0,0,0,0.9);'>Aircraft Predictive Maintenance System</h1>", unsafe_allow_html=True)

# Dashboard Tab
if selected_tab == "Dashboard":
    # Dashboard container
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="header">Fleet Status Overview</div>', unsafe_allow_html=True)
    
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
    
    # Display metrics in a stylish way
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
    
    # Create horizontal bar chart with enhanced colors
    fig = create_health_distribution_chart(status_counts, status_order)
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Engine details section
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="header">Individual Engine Monitor</div>', unsafe_allow_html=True)
    
    # Engine selector
    engine_options = sorted(train_data['unit_number'].unique())
    selected_engine = st.selectbox("Select Engine", engine_options)
    
    if selected_engine:
        # Get engine data
        engine_data = train_data[train_data['unit_number'] == selected_engine]
        min_rul = engine_data['RUL'].min()
        max_cycle = engine_data['cycle'].max()
        
        # Display enhanced status card
        st.markdown(create_status_card("Status", min_rul), unsafe_allow_html=True)
        
        # Create tabs for different visualizations
        engine_tabs = st.tabs(["RUL Trend", "Sensor Readings"])
        
        with engine_tabs[0]:
            # Plot RUL trend with enhanced styling
            fig = create_themed_line_chart(
                engine_data,
                'cycle',
                'RUL',
                f"Remaining Useful Life (RUL) for Engine #{selected_engine}"
            )
            
            # Add critical threshold
            fig = add_threshold_line(fig, 30)
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with engine_tabs[1]:
            # Find most variable sensors
            sensor_cols = [col for col in train_data.columns if 'sensor' in col]
            sensor_std = engine_data[sensor_cols].std().sort_values(ascending=False)
            top_sensors = sensor_std.head(5).index.tolist()
            
            # Let user select sensors
            selected_sensors = st.multiselect(
                "Select Sensors",
                options=sensor_cols,
                default=top_sensors[:3]
            )
            
            if selected_sensors:
                # Create data frames dictionary for the chart function
                data_frames = {selected_engine: engine_data}
                
                # Create sensor comparison chart with a single engine
                fig = create_sensor_comparison_chart(data_frames, selected_sensors[0])
                
                # Add additional sensor traces
                for sensor in selected_sensors[1:]:
                    fig.add_trace(
                        go.Scatter(
                            x=engine_data['cycle'],
                            y=engine_data[sensor],
                            mode='lines',
                            name=sensor,
                            line=dict(width=3)
                        )
                    )
                
                # Update the title
                fig.update_layout(title=f"Sensor Readings for Engine #{selected_engine}")
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('</div>', unsafe_allow_html=True)

# Analysis Tab
elif selected_tab == "Analysis":
    # Analysis container
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="header">Engine Degradation Analysis</div>', unsafe_allow_html=True)
    
    # Feature correlation analysis
    sensor_cols = [col for col in train_data.columns if 'sensor' in col]
    
    if len(sensor_cols) > 0:
        # Calculate correlations with RUL
        correlations = train_data[sensor_cols + ['RUL']].corr()['RUL'].drop('RUL').abs().sort_values(ascending=False)
        
        # Create enhanced correlation chart
        fig = create_correlation_chart(correlations)
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Top correlated sensors
        top_sensors = correlations.index[:3].tolist()
        
        # Display parameter table with top correlations
        correlation_params = {}
        for i, sensor in enumerate(top_sensors):
            correlation_params[sensor] = f"{correlations.iloc[i]:.3f} correlation"
        
        st.markdown(create_parameter_display(correlation_params), unsafe_allow_html=True)
        
        # Comparison across engines
        st.markdown("<h3 style='color:#ffffff; margin-top:30px;'>Compare Engines</h3>", unsafe_allow_html=True)
        
        # Select engines to compare
        engine_options = sorted(train_data['unit_number'].unique())
        selected_engines = st.multiselect(
            "Select Engines to Compare",
            options=engine_options,
            default=engine_options[:3] if len(engine_options) >= 3 else engine_options
        )
        
        # Select sensor to compare
        selected_sensor = st.selectbox(
            "Select Sensor for Comparison",
            options=sensor_cols,
            index=sensor_cols.index(top_sensors[0]) if top_sensors[0] in sensor_cols else 0
        )
        
        if selected_engines and selected_sensor:
            # Create data frames dictionary for the chart function
            data_frames = {engine: train_data[train_data['unit_number'] == engine] for engine in selected_engines}
            
            # Create enhanced sensor comparison chart
            fig = create_sensor_comparison_chart(data_frames, selected_sensor)
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('</div>', unsafe_allow_html=True)

# Prediction Tab
elif selected_tab == "Prediction":
    # Prediction container
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="header">RUL Prediction Engine</div>', unsafe_allow_html=True)
    
    # Train model with loading animation
    with st.spinner("Training machine learning model..."):
        model, scaler, importance = train_model(train_data)
    
    # Display feature importance
    st.markdown("<h3 style='color:#ffffff; margin-top:20px;'>Feature Importance</h3>", unsafe_allow_html=True)
    
    # Create enhanced feature importance chart
    fig = create_feature_importance_chart(importance)
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Prediction interface
    st.markdown("<h3 style='color:#ffffff; margin-top:30px;'>Predict Remaining Useful Life</h3>", unsafe_allow_html=True)
    
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
            sensor_cols = [col for col in train_data.columns if 'sensor' in col]
            
            if set(sensor_cols).issubset(cycle_data.columns):
                features = cycle_data[sensor_cols].values
                
                # Scale and predict
                features_scaled = scaler.transform(features)
                prediction = model.predict(features_scaled)[0]
                actual_rul = cycle_data['RUL'].values[0]
                
                # Display prediction and actual with enhanced styling
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(create_prediction_display(f"{prediction:.1f} cycles", "Predicted RUL", color=chart_colors['accent']), unsafe_allow_html=True)
                
                with col2:
                    st.markdown(create_prediction_display(f"{actual_rul} cycles", "Actual RUL", color=chart_colors['highlight']), unsafe_allow_html=True)
                
                # Enhanced RUL gauge
                fig = create_rul_gauge(prediction, actual_rul)
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                
                # Enhanced maintenance recommendation
                st.markdown(create_maintenance_recommendation(prediction), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sustainability Tab
elif selected_tab == "Sustainability":
    # Sustainability container
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<div class="header">Environmental Impact</div>', unsafe_allow_html=True)
    
    st.markdown('''
    <div style="color:#ffffff; margin-bottom:20px; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">
        Predictive maintenance directly supports SITA's mission to reduce the aviation sector's CO₂ emissions
        through data-driven solutions.
    </div>
    ''', unsafe_allow_html=True)
    
    # Calculator inputs in a clean layout
    st.markdown("<h3 style='color:#ffffff; margin-top:20px;'>Impact Calculator</h3>", unsafe_allow_html=True)
    
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
    
    # Display results in a clean, minimalist style
    st.markdown('''
    <div style="margin-top:30px; margin-bottom:20px;">
        <div style="font-size:20px; color:#ffffff; margin-bottom:15px; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">Annual Impact</div>
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_sustainability_metric("Fuel Saved", f"{fuel_saved/1000:,.1f} tonnes", color=chart_colors['accent2']), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_sustainability_metric("CO₂ Reduced", f"{co2_saved/1000:,.1f} tonnes", color=chart_colors['Good']), unsafe_allow_html=True)
    
    with col3:
        trees_equivalent = int(co2_saved / 25)  # Approx 25kg CO2 per tree per year
        st.markdown(create_sustainability_metric("Tree Equivalent", f"{trees_equivalent:,} trees", color=chart_colors['Good']), unsafe_allow_html=True)
    
    # Emissions comparison chart
    emissions_data = pd.DataFrame({
        'Scenario': ['Without Predictive Maintenance', 'With Predictive Maintenance'],
        'CO₂ Emissions (tonnes)': [
            total_annual_fuel * co2_per_kg_fuel / 1000,
            (total_annual_fuel - fuel_saved) * co2_per_kg_fuel / 1000
        ]
    })
    
    # Create enhanced emissions chart
    fig = create_emissions_chart(emissions_data, co2_saved)
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Enhanced SITA mission connection
    st.markdown(create_mission_box(), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('''
<div style="text-align:center; margin-top:40px; padding:10px; color:#ffffff; font-size:14px; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">
    Aircraft Predictive Maintenance System | Created for SITA Data Intelligence Team
</div>
''', unsafe_allow_html=True)

# Close main container
st.markdown('</div>', unsafe_allow_html=True)

# Try to load the background image
try:
    set_background('assets/moon_landscape.png')
except:
    # If image can't be loaded, create a custom background
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #0a0a14, #1f1f36);
    }
    </style>
    """, unsafe_allow_html=True)