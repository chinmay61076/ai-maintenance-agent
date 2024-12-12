import numpy as np
from datetime import datetime
import pandas as pd

class SensorInterface:
    def __init__(self):
        self.sensors = {
            'temperature': {
                'normal_range': (70, 80),
                'critical': 85,
                'unit': '°C'
            },
            'vibration': {
                'normal_range': (0.5, 1.5),
                'critical': 2.0,
                'unit': 'mm',
                'std_dev': 0.1
            },
            'pressure': {
                'normal_range': (95, 105),
                'critical': 110,
                'unit': 'PSI'
            }
        }
        self.readings_history = pd.DataFrame()
        
    def read_sensors(self):
        """Read current sensor values with controlled noise"""
        timestamp = datetime.now()
        readings = {'timestamp': timestamp}
        
        for sensor, config in self.sensors.items():
            min_val, max_val = config['normal_range']
            base_value = (min_val + max_val) / 2
            std_dev = config.get('std_dev', (max_val - min_val) * 0.1)
            
            reading = np.random.normal(base_value, std_dev)
            reading = np.clip(reading, min_val, max_val)
            
            readings[sensor] = reading
            
        # Store in history
        self.readings_history = pd.concat([
            self.readings_history,
            pd.DataFrame([readings])
        ], ignore_index=True)
        
        return readings
    
    def get_sensor_health(self, readings):
        """Evaluate health status of sensor readings"""
        health_status = {}
        
        for sensor, value in readings.items():
            if sensor == 'timestamp':
                continue
                
            config = self.sensors[sensor]
            min_val, max_val = config['normal_range']
            
            if value >= config['critical']:
                status = 'CRITICAL'
            elif value < min_val or value > max_val:
                status = 'WARNING'
            else:
                status = 'NORMAL'
                
            health_status[sensor] = {
                'status': status,
                'value': value,
                'unit': config['unit']
            }
            
        return health_status
    
    def get_historical_data(self, hours=24):
        """Get historical sensor data"""
        if self.readings_history.empty:
            return pd.DataFrame()
            
        cutoff = datetime.now() - pd.Timedelta(hours=hours)
        return self.readings_history[self.readings_history['timestamp'] > cutoff]
