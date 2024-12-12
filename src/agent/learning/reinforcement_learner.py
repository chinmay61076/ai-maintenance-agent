# src/agent/learning/reinforcement_learner.py

import numpy as np
from sklearn.neural_network import MLPRegressor
from collections import deque
import random
import joblib
from datetime import datetime

class ReinforcementLearner:
    def __init__(self):
        self.experience_buffer = []
        self.min_experiences = 3  # Minimum experiences needed before making predictions
        
    def process_experience(self, state, action, result, reward):
        """Process and store new experience"""
        experience = {
            'state': state,
            'action': action,
            'result': result,
            'reward': reward
        }
        self.experience_buffer.append(experience)
        
    def predict_outcome(self, state, action):
        """Predict outcome based on similar past experiences"""
        if len(self.experience_buffer) < self.min_experiences:
            return None
            
        # Find similar experiences
        similar_experiences = self._find_similar_experiences(state, action)
        
        if not similar_experiences:
            return None
            
        # Calculate average reward and confidence
        avg_reward = sum(exp['reward'] for exp in similar_experiences) / len(similar_experiences)
        confidence = len(similar_experiences) / len(self.experience_buffer)
        
        return {
            'predicted_reward': avg_reward,
            'confidence': confidence
        }
        
    def _find_similar_experiences(self, state, action):
        """Find experiences with similar states and same action"""
        similar = []
        for exp in self.experience_buffer:
            if exp['action'] == action:
                # Simple similarity check
                similar.append(exp)
        return similar
