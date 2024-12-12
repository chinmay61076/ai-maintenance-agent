# src/agent/learning/enhanced_learner.py

from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import numpy as np

class EnhancedLearner:
    def __init__(self):
        self.models = {
            'rf': self._create_rf_model(),
            'nn': self._create_nn_model(),
            'lstm': self._create_lstm_model()
        }
        self.active_model = 'rf'  # default model
        
    def _create_rf_model(self):
        """Create Random Forest model"""
        return RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
    def _create_nn_model(self):
        """Create Neural Network model"""
        model = Sequential([
            Dense(64, activation='relu', input_shape=(3,)),
            Dense(32, activation='relu'),
            Dense(16, activation='relu'),
            Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mse')
        return model
        
    def _create_lstm_model(self):
        """Create LSTM model for sequence learning"""
        model = Sequential([
            LSTM(64, input_shape=(10, 3)),
            Dense(32, activation='relu'),
            Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mse')
        return model
        
    def train(self, X, y, model_type=None):
        """Train specified model"""
        if model_type:
            self.active_model = model_type
            
        model = self.models[self.active_model]
        
        if self.active_model == 'lstm':
            # Reshape data for LSTM
            X = self._prepare_sequences(X)
            
        return model.fit(X, y)
        
    def predict(self, X):
        """Make prediction using active model"""
        model = self.models[self.active_model]
        
        if self.active_model == 'lstm':
            X = self._prepare_sequences(X)
            
        return model.predict(X)
        
    def _prepare_sequences(self, data, sequence_length=10):
        """Prepare data for LSTM"""
        sequences = []
        for i in range(len(data) - sequence_length + 1):
            sequences.append(data[i:i + sequence_length])
        return np.array(sequences)
