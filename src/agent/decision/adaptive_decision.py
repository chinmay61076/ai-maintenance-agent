# src/agent/decision/adaptive_decision.py

import numpy as np
from datetime import datetime
import pandas as pd

class AdaptiveDecisionMaker:
    def __init__(self, learner):
        self.learner = learner
        self.decisions_history = []
        self.action_space = {
            'no_action': 0,
            'increase_monitoring': 1,
            'schedule_maintenance': 2,
            'immediate_maintenance': 3,
            'emergency_shutdown': 4
        }
        
    def make_decision(self, current_state, sensor_health):
        """Make adaptive decision based on current state and learned experiences"""
        # Get predictions for each possible action
        action_predictions = {}
        for action_name, action_id in self.action_space.items():
            prediction = self.learner.predict_outcome(current_state, action_id)
            if prediction:
                action_predictions[action_name] = prediction
                
        # Evaluate situation severity
        severity = self._evaluate_severity(sensor_health)
        
        # Select action based on predictions and severity
        selected_action = self._select_action(action_predictions, severity)
        
        # Record decision
        self.decisions_history.append({
            'timestamp': datetime.now(),
            'state': current_state,
            'sensor_health': sensor_health,
            'severity': severity,
            'selected_action': selected_action,
            'predictions': action_predictions
        })
        
        return selected_action
        
    def _evaluate_severity(self, sensor_health):
        """Evaluate situation severity"""
        severity_score = 0
        
        for sensor, status in sensor_health.items():
            if status['status'] == 'CRITICAL':
                severity_score += 3
            elif status['status'] == 'WARNING':
                severity_score += 1
                
        if severity_score >= 5:
            return 'CRITICAL'
        elif severity_score >= 2:
            return 'WARNING'
        return 'NORMAL'
        
    def _select_action(self, predictions, severity):
        """Select best action based on predictions and severity"""
        if severity == 'CRITICAL':
            # In critical situations, prioritize safety
            return 'emergency_shutdown'
            
        if not predictions:
            # If no predictions available, use rule-based decision
            if severity == 'WARNING':
                return 'schedule_maintenance'
            return 'increase_monitoring'
            
        # Select action with highest predicted reward
        best_action = max(predictions.items(), 
                         key=lambda x: x[1]['predicted_reward'])
        
        return best_action[0]
        
    def get_decision_metrics(self):
        """Get metrics about decision making performance"""
        df = pd.DataFrame(self.decisions_history)
        return {
            'total_decisions': len(df),
            'action_distribution': df['selected_action'].value_counts().to_dict(),
            'severity_distribution': df['severity'].value_counts().to_dict(),
            'average_confidence': np.mean([
                list(d['predictions'].values())[0]['confidence'] 
                for d in self.decisions_history 
                if d['predictions']
            ])
        }
