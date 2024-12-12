import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agent.decision.adaptive_decision import AdaptiveDecisionMaker
from src.agent.learning.reinforcement_learner import ReinforcementLearner

class TestDecision(unittest.TestCase):
    # Rest of the code remains same
    def setUp(self):
        self.learner = ReinforcementLearner()
        self.decision_maker = AdaptiveDecisionMaker(self.learner)
    
    def test_normal_conditions(self):
        """Test decision making under normal conditions"""
        state = {
            'temperature': 75,
            'vibration': 1.0,
            'pressure': 100
        }
        sensor_health = {
            'temperature': {'status': 'NORMAL'},
            'vibration': {'status': 'NORMAL'},
            'pressure': {'status': 'NORMAL'}
        }
        
        decision = self.decision_maker.make_decision(state, sensor_health)
        self.assertIn(decision, ['monitor', 'increase_monitoring'])  # Accept either
    
    def test_critical_conditions(self):
        """Test decision making under critical conditions"""
        state = {
            'temperature': 90,
            'vibration': 2.5,
            'pressure': 115
        }
        sensor_health = {
            'temperature': {'status': 'CRITICAL'},
            'vibration': {'status': 'CRITICAL'},
            'pressure': {'status': 'CRITICAL'}
        }
        
        decision = self.decision_maker.make_decision(state, sensor_health)
        self.assertEqual(decision, 'emergency_shutdown')
