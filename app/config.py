# Application configuration
PAGE_TITLE = "Aircraft Predictive Maintenance"
PAGE_ICON = "✈️"
LAYOUT = "wide"
SIDEBAR_STATE = "collapsed"
APP_TITLE = "Aircraft Predictive Maintenance System"

# Data paths
DATA_PATH = "data/raw/fixed_train_FD001.csv"
BACKGROUND_IMAGE = "assets/images/moon_landscape.png"

# Chart colors
CHART_COLORS = {
    'Critical': '#ff3333',  # Bright red
    'Warning': '#ffaa00',   # Bright orange
    'Moderate': '#ffff00',  # Bright yellow
    'Good': '#33ff33',      # Bright green
    'Excellent': '#33ffff', # Bright cyan
    'accent': '#9966ff',    # Bright purple
    'accent2': '#ff66ff',   # Bright magenta
    'highlight': '#ffffff'  # White
}

# Footer
FOOTER_HTML = '''
<div style="text-align:center; margin-top:40px; padding:10px; color:#ffffff; font-size:14px; text-shadow: 0 1px 2px rgba(0,0,0,0.9);">
    Aircraft Predictive Maintenance System | Created for SITA Data Intelligence Team
</div>
'''