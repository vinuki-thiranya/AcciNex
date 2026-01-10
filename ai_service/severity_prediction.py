# severity_prediction.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import json

class SeverityPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.features = ['hour_of_day', 'day_of_week', 'month', 
                        'is_rainy', 'is_night', 'is_weekend',
                        'location_cluster', 'previous_accidents_count',
                        'road_type', 'speed_limit']
        
    def load_training_data(self, db_connection):
        """Load historical accident data from database"""
        query = """
        SELECT EXTRACT(HOUR FROM accident_time) as hour_of_day,
               EXTRACT(DOW FROM accident_time) as day_of_week,
               EXTRACT(MONTH FROM accident_time) as month,
               CASE WHEN weather_condition LIKE '%rain%' THEN 1 ELSE 0 END as is_rainy,
               CASE WHEN EXTRACT(HOUR FROM accident_time) BETWEEN 18 AND 6 THEN 1 ELSE 0 END as is_night,
               CASE WHEN EXTRACT(DOW FROM accident_time) IN (0, 6) THEN 1 ELSE 0 END as is_weekend,
               severity,
               latitude, longitude
        FROM accident_reports
        WHERE severity IS NOT NULL
        """
        df = pd.read_sql(query, db_connection)
        return df
    
    def preprocess_data(self, df):
        """Preprocess and feature engineering"""
        # Add location clustering
        from sklearn.cluster import KMeans
        coords = df[['latitude', 'longitude']].fillna(0)
        kmeans = KMeans(n_clusters=50, random_state=42)
        df['location_cluster'] = kmeans.fit_predict(coords)
        
        # Add previous accidents count per location
        df['previous_accidents_count'] = df.groupby('location_cluster').cumcount()
        
        # Encode target variable
        df['severity_encoded'] = self.label_encoder.fit_transform(df['severity'])
        
        # Prepare features and target
        X = df[self.features]
        y = df['severity_encoded']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y, df
    
    def train_model(self, X, y):
        """Train ensemble model"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Random Forest
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        
        # Train Logistic Regression
        lr_model = LogisticRegression(max_iter=1000, random_state=42)
        lr_model.fit(X_train, y_train)
        
        # Create ensemble (simple averaging)
        self.model = {
            'random_forest': rf_model,
            'logistic_regression': lr_model
        }
        
        # Evaluate
        rf_score = rf_model.score(X_test, y_test)
        lr_score = lr_model.score(X_test, y_test)
        
        print(f"RF Accuracy: {rf_score:.2%}")
        print(f"LR Accuracy: {lr_score:.2%}")
        
        return self.model
    
    def predict(self, features_dict):
        """Predict severity for new accident"""
        # Convert input to dataframe
        input_df = pd.DataFrame([features_dict])
        
        # Ensure all features are present
        for feature in self.features:
            if feature not in input_df.columns:
                input_df[feature] = 0
        
        # Scale features
        input_scaled = self.scaler.transform(input_df[self.features])
        
        # Get predictions from both models
        rf_pred = self.model['random_forest'].predict_proba(input_scaled)
        lr_pred = self.model['logistic_regression'].predict_proba(input_scaled)
        
        # Average probabilities
        avg_proba = (rf_pred + lr_pred) / 2
        
        # Get predicted class and confidence
        predicted_class = np.argmax(avg_proba[0])
        confidence = np.max(avg_proba[0])
        
        severity = self.label_encoder.inverse_transform([predicted_class])[0]
        
        return {
            'severity': severity,
            'confidence': float(confidence),
            'probabilities': {
                'minor': float(avg_proba[0][0]),
                'major': float(avg_proba[0][1]),
                'dangerous': float(avg_proba[0][2])
            }
        }
    
    def save_model(self, path='models/'):
        """Save trained model and preprocessing objects"""
        import os
        if not os.path.exists(path):
            os.makedirs(path)
        joblib.dump(self.model, f'{path}/severity_model.pkl')
        joblib.dump(self.scaler, f'{path}/scaler.pkl')
        joblib.dump(self.label_encoder, f'{path}/label_encoder.pkl')
        
        # Save feature list
        with open(f'{path}/features.json', 'w') as f:
            json.dump(self.features, f)
    
    def load_model(self, path='models/'):
        """Load trained model"""
        self.model = joblib.load(f'{path}/severity_model.pkl')
        self.scaler = joblib.load(f'{path}/scaler.pkl')
        self.label_encoder = joblib.load(f'{path}/label_encoder.pkl')
        
        with open(f'{path}/features.json', 'r') as f:
            self.features = json.load(f)
