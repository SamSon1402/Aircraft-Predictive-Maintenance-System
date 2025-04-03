import unittest
import pandas as pd
import numpy as np
from app.utils.data_processing import create_synthetic_data, preprocess_data

class TestDataProcessing(unittest.TestCase):
    
    def setUp(self):
        # Create a small synthetic dataset for testing
        self.test_data = create_synthetic_data()
    
    def test_synthetic_data_creation(self):
        # Test that synthetic data has expected columns
        self.assertIn('unit_number', self.test_data.columns)
        self.assertIn('cycle', self.test_data.columns)
        self.assertIn('RUL', self.test_data.columns)
        self.assertIn('sensor_1', self.test_data.columns)
        
        # Test that data has rows
        self.assertGreater(len(self.test_data), 0)
    
    def test_preprocess_data(self):
        # Test preprocessing function
        X_scaled, y, scaler, sensor_cols = preprocess_data(self.test_data)
        
        # Check that output shapes match
        self.assertEqual(X_scaled.shape[0], len(self.test_data))
        self.assertEqual(len(y), len(self.test_data))
        
        # Check that all sensor columns were identified
        expected_sensor_count = len([col for col in self.test_data.columns if 'sensor' in col])
        self.assertEqual(len(sensor_cols), expected_sensor_count)
        
        # Check that scaling worked (should have mean ~0 and std ~1)
        self.assertAlmostEqual(np.mean(X_scaled), 0, delta=0.1)
        self.assertAlmostEqual(np.std(X_scaled), 1, delta=0.1)

if __name__ == '__main__':
    unittest.main()