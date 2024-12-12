# src/tests/test_framework.py

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MaintenanceAgentTests(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.sensor_interface = SensorInterface()
        self.learner = ReinforcementLearner()
        self.decision_maker = AdaptiveDecisionMaker(self.learner)
        
    def test_sensor_readings(self):
        """Test sensor data collection"""
        readings = self.sensor_interface.read_sensors()
        
        self.assertIn('temperature', readings)
        self.assertIn('vibration', readings)
        self.assertIn('pressure', readings)
        
        # Test value ranges
        self.assertTrue(60 <= readings['temperature'] <= 90)
        self.assertTrue(0 <= readings['vibration'] <= 3)
        self.assertTrue(90 <= readings['pressure'] <= 110)
        
    def test_learning_mechanism(self):
        """Test learning capabilities"""
        # Generate test data
        state = {
            'temperature': 75,
            'vibration': 1.0,
            'pressure': 100
        }
        action = 'no_action'
        result = {'success': True}
        reward = 1
        
        # Test learning
        self.learner.process_experience(state, action, result, reward)
        prediction = self.learner.predict_outcome(state, action)
        
        self.assertIsNotNone(prediction)
        
    def test_decision_making(self):
        """Test decision making process"""
        state = {
            'temperature': 85,  # Critical
            'vibration': 1.0,
            'pressure': 100
        }
        
        sensor_health = self.sensor_interface.get_sensor_health(state)
        decision = self.decision_maker.make_decision(state, sensor_health)
        
        # Should recommend immediate action for critical temperature
        self.assertIn(decision, ['immediate_maintenance', 'emergency_shutdown'])
        
    def test_scenario_handling(self):
        """Test handling of different scenarios"""
        scenarios = MaintenanceScenarios()
        
        for scenario in ['normal_operation', 'sudden_failure']:
            data = scenarios.generate_scenario(scenario, duration_hours=1)
            
            self.assertIsInstance(data, pd.DataFrame)
            self.assertGreater(len(data), 0)
            
            # Process scenario data
            for _, row in data.iterrows():
                readings = {
                    k: v for k, v in row.items() 
                    if k not in ['timestamp']
                }
                sensor_health = self.sensor_interface.get_sensor_health(readings)
                decision = self.decision_maker.make_decision(readings, sensor_health)
                
                # Verify decision is valid
                self.assertIn(decision, self.decision_maker.action_space.keys())

def run_tests():
    unittest.main()

if __name__ == '__main__':
    run_tests()
