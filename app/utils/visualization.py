import plotly.express as px
import plotly.graph_objects as go
import app.config as config

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
    
    # Make sure the chart has a border for better definition
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

def create_themed_line_chart(data, x, y, title):
    """Create a themed line chart with good visibility"""
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        markers=True
    )
    # Thicker lines and larger markers
    fig.update_traces(line=dict(color=config.CHART_COLORS['accent'], width=4))
    fig.update_traces(marker=dict(color=config.CHART_COLORS['accent2'], size=10, line=dict(width=2, color='#ffffff')))
    return update_chart_style(fig)

def add_threshold_line(fig, y_value, text="Critical Threshold"):
    """Add a threshold line to a chart"""
    fig.add_hline(
        y=y_value,
        line_dash="dash",
        line_color=config.CHART_COLORS['Critical'],
        line_width=3,
        annotation_text=text,
        annotation_font=dict(color=config.CHART_COLORS['highlight'], size=16),
        annotation_bgcolor="rgba(5, 5, 15, 0.9)"
    )
    return fig

def create_health_distribution_chart(status_counts, status_order):
    """Create a bar chart showing engine health distribution"""
    fig = px.bar(
        status_counts,
        y='Status',
        x='Count',
        color='Status',
        color_discrete_map={
            'Critical': config.CHART_COLORS['Critical'],
            'Warning': config.CHART_COLORS['Warning'],
            'Moderate': config.CHART_COLORS['Moderate'],
            'Good': config.CHART_COLORS['Good'],
            'Excellent': config.CHART_COLORS['Excellent']
        },
        category_orders={'Status': status_order},
        orientation='h',
        title="Engine Health Distribution"
    )
    
    # Apply the enhanced styling
    fig = update_chart_style(fig)
    
    return fig