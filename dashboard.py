import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import time
from src.agent.environment.sensor_interface import SensorInterface
from src.agent.learning.reinforcement_learner import ReinforcementLearner
from src.agent.decision.adaptive_decision import AdaptiveDecisionMaker
def main():
    st.title("AI-Powered Predictive Maintenance System")
    
    # Initialize components
    sensor = SensorInterface()
    learner = ReinforcementLearner()
    decision_maker = AdaptiveDecisionMaker(learner)
    
    # Create dashboard sections
    col1, col2, col3 = st.columns(3)
    
    while True:
        # Get current readings
        readings = sensor.read_sensors()
        health = sensor.get_sensor_health(readings)
        
        # Display current readings
        with col1:
            st.header("Sensor Readings")
            st.metric("Temperature", f"{readings['temperature']:.1f}°C")
            st.metric("Vibration", f"{readings['vibration']:.2f}mm")
            st.metric("Pressure", f"{readings['pressure']:.1f}PSI")
        
        # Display health status
        with col2:
            st.header("Health Status")
            for sensor_name, status in health.items():
                color = "green" if status['status'] == 'NORMAL' else "red"
                st.markdown(f":{color}[{sensor_name}: {status['status']}]")
        
        # Display maintenance decisions
        with col3:
            st.header("Maintenance Action")
            decision = decision_maker.make_decision(readings, health)
            st.write(f"Recommended Action: {decision}")
        
        time.sleep(1)
        st.experimental_rerun()

if __name__ == "__main__":
    main()
