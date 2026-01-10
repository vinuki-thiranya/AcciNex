# hotspot_detection.py
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class HotspotDetector:
    def __init__(self, eps=0.01, min_samples=3):
        self.eps = eps  # ~1km in decimal degrees
        self.min_samples = min_samples
        self.dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='haversine')
        self.hotspots = []
        
    def detect_hotspots(self, accidents_df):
        """Detect accident hotspots using spatial-temporal clustering"""
        if accidents_df.empty:
            return []
            
        # Extract coordinates
        coords = np.radians(accidents_df[['latitude', 'longitude']].values)
        
        # Perform DBSCAN clustering
        clusters = self.dbscan.fit_predict(coords)
        
        # Add cluster labels to dataframe
        accidents_df['cluster'] = clusters
        
        # Filter out noise (cluster = -1)
        valid_clusters = accidents_df[accidents_df['cluster'] != -1]
        
        # Analyze each cluster
        hotspots = []
        for cluster_id in valid_clusters['cluster'].unique():
            cluster_data = valid_clusters[valid_clusters['cluster'] == cluster_id]
            
            # Calculate cluster center
            center_lat = cluster_data['latitude'].mean()
            center_lng = cluster_data['longitude'].mean()
            
            # Calculate risk metrics
            total_accidents = len(cluster_data)
            severity_scores = {
                'minor': len(cluster_data[cluster_data['severity'] == 'minor']),
                'major': len(cluster_data[cluster_data['severity'] == 'major']),
                'dangerous': len(cluster_data[cluster_data['severity'] == 'dangerous'])
            }
            
            # Calculate risk score (weighted)
            risk_score = (
                severity_scores['minor'] * 1 +
                severity_scores['major'] * 3 +
                severity_scores['dangerous'] * 5
            ) / total_accidents
            
            # Determine risk level
            if risk_score >= 4:
                risk_level = 'high'
            elif risk_score >= 2.5:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            # Analyze time patterns
            time_patterns = self._analyze_time_patterns(cluster_data)
            
            # Analyze weather patterns
            weather_patterns = self._analyze_weather_patterns(cluster_data)
            
            hotspot = {
                'cluster_id': int(cluster_id),
                'center': {'lat': center_lat, 'lng': center_lng},
                'bounding_box': self._calculate_bounding_box(cluster_data),
                'total_accidents': int(total_accidents),
                'severity_distribution': severity_scores,
                'risk_score': float(risk_score),
                'risk_level': risk_level,
                'time_patterns': time_patterns,
                'weather_patterns': weather_patterns,
                'last_accident': cluster_data['accident_time'].max().isoformat() if isinstance(cluster_data['accident_time'].max(), datetime) else str(cluster_data['accident_time'].max()),
                'recommendations': self._generate_recommendations(risk_level, time_patterns)
            }
            
            hotspots.append(hotspot)
        
        self.hotspots = hotspots
        return hotspots
    
    def _analyze_time_patterns(self, cluster_data):
        """Analyze when accidents occur in this hotspot"""
        # Ensure accident_time is datetime
        cluster_data['accident_time'] = pd.to_datetime(cluster_data['accident_time'])
        
        # Extract hour of day
        cluster_data['hour'] = cluster_data['accident_time'].dt.hour
        
        # Group by hour
        hourly_counts = cluster_data['hour'].value_counts().sort_index()
        
        # Find peak hours (top 3 hours with most accidents)
        peak_hours = hourly_counts.nlargest(3).index.tolist()
        
        # Analyze day of week patterns
        cluster_data['day_of_week'] = cluster_data['accident_time'].dt.dayofweek
        weekday_counts = cluster_data['day_of_week'].value_counts()
        
        return {
            'peak_hours': peak_hours,
            'hourly_distribution': hourly_counts.to_dict(),
            'busiest_day': int(weekday_counts.idxmax()) if not weekday_counts.empty else None,
            'is_night_hotspot': len(cluster_data[cluster_data['hour'].between(18, 6)]) > len(cluster_data) * 0.5
        }
    
    def _analyze_weather_patterns(self, cluster_data):
        """Analyze weather conditions during accidents"""
        if 'weather_condition' not in cluster_data.columns:
            return {}
        
        weather_counts = cluster_data['weather_condition'].value_counts()
        
        return {
            'most_common_weather': weather_counts.idxmax() if not weather_counts.empty else 'unknown',
            'rainy_percentage': (len(cluster_data[cluster_data['weather_condition'].str.contains('rain', case=False, na=False)]) / len(cluster_data) * 100) if not cluster_data.empty else 0
        }
    
    def _calculate_bounding_box(self, cluster_data, padding=0.001):
        """Calculate bounding box for hotspot visualization"""
        min_lat = cluster_data['latitude'].min() - padding
        max_lat = cluster_data['latitude'].max() + padding
        min_lng = cluster_data['longitude'].min() - padding
        max_lng = cluster_data['longitude'].max() + padding
        
        return {
            'north': float(max_lat),
            'south': float(min_lat),
            'east': float(max_lng),
            'west': float(min_lng)
        }
    
    def _generate_recommendations(self, risk_level, time_patterns):
        """Generate safety recommendations based on hotspot analysis"""
        recommendations = []
        
        if risk_level == 'high':
            recommendations.append("Immediate safety audit required")
            recommendations.append("Consider traffic calming measures")
        
        if time_patterns.get('is_night_hotspot'):
            recommendations.append("Improve street lighting")
            recommendations.append("Add reflective road markings")
        
        if time_patterns.get('peak_hours'):
            peak_str = ", ".join(map(str, time_patterns['peak_hours']))
            recommendations.append(f"Increase police patrols during hours: {peak_str}")
        
        return recommendations
