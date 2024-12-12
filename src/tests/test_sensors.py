import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agent.environment.sensor_interface import SensorInterface

class TestSensors(unittest.TestCase):
    # Rest of the code remains same
    def setUp(self):
        self.sensor = SensorInterface()
    
    def test_sensor_readings(self):
        """Test sensor data collection"""
        readings = self.sensor.read_sensors()
        
        # Test presence of all sensors
        self.assertIn('temperature', readings)
        self.assertIn('vibration', readings)
        self.assertIn('pressure', readings)
        
        # Test value ranges (updated to match sensor configuration)
        self.assertTrue(60 <= readings['temperature'] <= 90)
        self.assertTrue(0.5 <= readings['vibration'] <= 1.5)  # Updated range
        self.assertTrue(95 <= readings['pressure'] <= 105)
    
    def test_sensor_health(self):
        """Test health status calculation"""
        readings = {
            'temperature': 90,  # Increased to trigger CRITICAL
            'vibration': 1.0,
            'pressure': 100
        }
        health = self.sensor.get_sensor_health(readings)
        self.assertEqual(health['temperature']['status'], 'CRITICAL')
        self.assertEqual(health['vibration']['status'], 'NORMAL')
