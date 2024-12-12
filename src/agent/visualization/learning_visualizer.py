# src/agent/visualization/learning_visualizer.py

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class LearningVisualizer:
    def __init__(self, learner, decision_maker):
        self.learner = learner
        self.decision_maker = decision_maker
        
    def create_learning_dashboard(self):
        """Create interactive dashboard of learning process"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Learning Progress',
                'Decision Distribution',
                'Sensor States',
                'Reward History'
            )
        )
        
        # Learning Progress
        learning_df = pd.DataFrame(self.learner.learning_history)
        fig.add_trace(
            go.Scatter(
                x=learning_df['timestamp'],
                y=learning_df['model_score'],
                mode='lines',
                name='Model Score'
            ),
            row=1, col=1
        )
        
        # Decision Distribution
        decisions = pd.DataFrame(self.decision_maker.decisions_history)
        decision_counts = decisions['selected_action'].value_counts()
        fig.add_trace(
            go.Bar(
                x=decision_counts.index,
                y=decision_counts.values,
                name='Decisions Made'
            ),
            row=1, col=2
        )
        
        # Sensor States
        sensor_data = decisions['state'].apply(pd.Series)
        for column in ['temperature', 'vibration', 'pressure']:
            fig.add_trace(
                go.Scatter(
                    x=decisions['timestamp'],
                    y=sensor_data[column],
                    name=column,
                    mode='lines'
                ),
                row=2, col=1
            )
        
        # Reward History
        fig.add_trace(
            go.Scatter(
                x=learning_df['timestamp'],
                y=learning_df['buffer_size'],
                name='Experience Buffer Size'
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=800, title_text="Learning Process Dashboard")
        return fig
