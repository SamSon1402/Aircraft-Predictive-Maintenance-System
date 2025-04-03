import unittest
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from app.utils.visualization import update_chart_style, create_themed_line_chart, add_threshold_line

class TestVisualization(unittest.TestCase):
    
    def setUp(self):
        # Create sample data for testing charts
        self.test_data = pd.DataFrame({
            'x': range(10),
            'y': [i**2 for i in range(10)]
        })
    
    def test_update_chart_style(self):
        # Create a simple figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.test_data['x'], y=self.test_data['y']))
        
        # Apply styling
        styled_fig = update_chart_style(fig)
        
        # Check that styling was applied
        self.assertEqual(styled_fig.layout.paper_bgcolor, 'rgba(5, 5, 15, 0)')
        self.assertEqual(styled_fig.layout.plot_bgcolor, 'rgba(5, 5, 15, 0.95)')
        self.assertEqual(styled_fig.layout.font.color, '#ffffff')
    
    def test_create_themed_line_chart(self):
        # Create a themed line chart
        fig = create_themed_line_chart(self.test_data, 'x', 'y', 'Test Chart')
        
        # Check that the chart was created with title
        self.assertEqual(fig.layout.title.text, 'Test Chart')
        
        # Check that the line was styled
        self.assertEqual(fig.data[0].line.width, 4)
    
    def test_add_threshold_line(self):
        # Create a simple figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.test_data['x'], y=self.test_data['y']))
        
        # Add threshold line
        threshold_value = 50
        threshold_text = "Test Threshold"
        fig_with_threshold = add_threshold_line(fig, threshold_value, threshold_text)
        
        # Check that a horizontal line was added
        self.assertGreater(len(fig_with_threshold.layout.shapes), 0)
        
        # Check that annotation was added
        self.assertGreater(len(fig_with_threshold.layout.annotations), 0)
        self.assertEqual(fig_with_threshold.layout.annotations[0].text, threshold_text)

if __name__ == '__main__':
    unittest.main()