# src/main.py

from agent.environment.sensor_interface import SensorInterface
from agent.learning.reinforcement_learner import ReinforcementLearner
from agent.decision.adaptive_decision import AdaptiveDecisionMaker
import time
import logging

class MaintenanceAgent:
    def __init__(self):
        # Initialize components
        self.sensor_interface = SensorInterface()
        self.learner = ReinforcementLearner()
        self.decision_maker = AdaptiveDecisionMaker(self.learner)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def run(self, interval=5):
        """Run the maintenance agent"""
        self.logger.info("Starting Maintenance Agent...")
        
        try:
            while True:
                # 1. Get current state
                current_state = self.sensor_interface.read_sensors()
                sensor_health = self.sensor_interface.get_sensor_health(current_state)
                
                # 2. Make decision
                action = self.decision_maker.make_decision(
                    current_state,
                    sensor_health
                )
                
                # 3. Execute action and get result
                result = self._execute_action(action, current_state)
                
                # 4. Calculate reward
                reward = self._calculate_reward(result, sensor_health)
                
                # 5. Learn from experience
                self.learner.process_experience(
                    current_state,
                    action,
                    result,
                    reward
                )
                
                # 6. Log status
                self._log_status(current_state, action, result)
                
                # Wait for next cycle
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.logger.info("Shutting down Maintenance Agent...")
            self._save_state()
            
    def _execute_action(self, action, state):
        """Execute maintenance action"""
        # Simulate action execution
        result = {
            'action': action,
            'success': True,
            'timestamp': datetime.now(),
            'effects': self._simulate_action_effects(action, state)
        }
        return result
        
    def _calculate_reward(self, result, sensor_health):
        """Calculate reward for taken action"""
        reward = 0
        
        # Penalty for critical states
        if any(status['status'] == 'CRITICAL' for status in sensor_health.values()):
            reward -= 10
            
        # Reward for successful maintenance
        if result['success']:
            if result['action'] == 'emergency_shutdown':
                reward += 5 if any(status['status'] == 'CRITICAL' 
                                 for status in sensor_health.values()) else -5
            elif result['action'] == 'schedule_maintenance':
                reward += 3
                
        return reward
        
    def _log_status(self, state, action, result):
        """Log current status"""
        metrics = self.decision_maker.get_decision_metrics()
        self.logger.info(f"""
Status Update:
--------------
Action Taken: {action}
Success: {result['success']}
Total Decisions: {metrics['total_decisions']}
Average Confidence: {metrics['average_confidence']:.2f}
        """)
        
    def _save_state(self):
        """Save agent state"""
        self.learner.save_model('models/maintenance_agent.joblib')

if __name__ == "__main__":
    agent = MaintenanceAgent()
    agent.run()
