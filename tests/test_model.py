import unittest
import pandas as pd
import numpy as np
from app.utils.data_processing import create_synthetic_data
from app.utils.model import train_model, predict_rul

class TestModel(unittest.TestCase):
    
    def setUp(self):
        # Create a small synthetic dataset for testing
        self.test_data = create_synthetic_data()
        
        # Train the model on test data
        self.model, self.scaler, self.importance = train_model(self.test_data)
        
        # Get sensor columns for predictions
        self.sensor_cols = [col for col in self.test_data.columns if 'sensor' in col]
    
    def test_train_model(self):
        # Test that model training works
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.scaler)
        
        # Check that importance was calculated for all features
        self.assertEqual(len(self.importance), len(self.sensor_cols))
        
        # Check that importance values sum to approximately 1
        self.assertAlmostEqual(sum(self.importance['Importance']), 1.0, delta=0.01)
    
    def test_predict_rul(self):
        # Get a sample engine
        engine_num = self.test_data['unit_number'].iloc[0]
        engine_data = self.test_data[self.test_data['unit_number'] == engine_num]
        
        # Get a cycle to test
        cycle = engine_data['cycle'].iloc[0]
        
        # Test prediction
        prediction = predict_rul(self.model, self.scaler, engine_data, cycle, self.sensor_cols)
        
        # Check that prediction is a reasonable number
        self.assertIsNotNone(prediction)
        self.assertGreaterEqual(prediction, 0)  # RUL should be non-negative
        
        # Check prediction is within reasonable range of actual
        actual_rul = engine_data[engine_data['cycle'] == cycle]['RUL'].iloc[0]
        self.assertLess(abs(prediction - actual_rul), 50)  # Should be within 50 cycles

if __name__ == '__main__':
    unittest.main()