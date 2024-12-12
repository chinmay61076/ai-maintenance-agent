# src/agent/scenarios/maintenance_scenarios.py

from datetime import datetime, timedelta
import numpy as np

class MaintenanceScenarios:
    def __init__(self):
        self.scenarios = {
            'normal_operation': self._normal_operation,
            'gradual_degradation': self._gradual_degradation,
            'sudden_failure': self._sudden_failure,
            'multiple_issues': self._multiple_issues,
            'seasonal_pattern': self._seasonal_pattern
        }
        
    def generate_scenario(self, scenario_name, duration_hours=24):
        """Generate scenario data"""
        if scenario_name not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_name}")
            
        return self.scenarios[scenario_name](duration_hours)
        
    def _normal_operation(self, duration_hours):
        """Generate normal operation data"""
        timestamps = pd.date_range(
            start=datetime.now(),
            periods=duration_hours * 60,
            freq='1min'
        )
        
        data = []
        for ts in timestamps:
            reading = {
                'timestamp': ts,
                'temperature': np.random.normal(75, 1),
                'vibration': np.random.normal(1.0, 0.1),
                'pressure': np.random.normal(100, 2)
            }
            data.append(reading)
            
        return pd.DataFrame(data)
        
    def _gradual_degradation(self, duration_hours):
        """Generate gradual degradation scenario"""
        data = []
        base_temp = 75
        base_vibration = 1.0
        
        timestamps = pd.date_range(
            start=datetime.now(),
            periods=duration_hours * 60,
            freq='1min'
        )
        
        for i, ts in enumerate(timestamps):
            progress = i / (duration_hours * 60)
            reading = {
                'timestamp': ts,
                'temperature': base_temp + progress * 15 + np.random.normal(0, 1),
                'vibration': base_vibration + progress * 1.5 + np.random.normal(0, 0.1),
                'pressure': np.random.normal(100, 2)
            }
            data.append(reading)
            
        return pd.DataFrame(data)
        
    def _sudden_failure(self, duration_hours):
        """Generate sudden failure scenario"""
        failure_point = int(duration_hours * 0.7 * 60)  # 70% through duration
        
        timestamps = pd.date_range(
            start=datetime.now(),
            periods=duration_hours * 60,
            freq='1min'
        )
        
        data = []
        for i, ts in enumerate(timestamps):
            if i < failure_point:
                reading = {
                    'timestamp': ts,
                    'temperature': np.random.normal(75, 1),
                    'vibration': np.random.normal(1.0, 0.1),
                    'pressure': np.random.normal(100, 2)
                }
            else:
                reading = {
                    'timestamp': ts,
                    'temperature': np.random.normal(90, 2),
                    'vibration': np.random.normal(2.5, 0.2),
                    'pressure': np.random.normal(115, 3)
                }
            data.append(reading)
            
        return pd.DataFrame(data)
