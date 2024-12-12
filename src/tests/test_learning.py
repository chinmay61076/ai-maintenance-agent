import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agent.learning.reinforcement_learner import ReinforcementLearner

class TestLearning(unittest.TestCase):
    # Rest of the code remains same
    def setUp(self):
        self.learner = ReinforcementLearner()
    
    def test_experience_processing(self):
        """Test experience processing"""
        # Process multiple experiences to build up data
        for _ in range(5):  # Add multiple experiences
            state = {'temperature': 75, 'vibration': 1.0, 'pressure': 100}
            action = 'monitor'
            result = {'success': True}
            reward = 1
            
            self.learner.process_experience(state, action, result, reward)
        
        # Now test prediction
        state = {'temperature': 75, 'vibration': 1.0, 'pressure': 100}
        prediction = self.learner.predict_outcome(state, 'monitor')
        self.assertIsNotNone(prediction)
