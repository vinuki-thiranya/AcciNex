# alert_engine.py
from datetime import datetime, timedelta
import math

class AlertEngine:
    def __init__(self, hotspots_data, current_weather=None):
        self.hotspots = hotspots_data
        self.current_weather = current_weather or {}
        self.alerts = []
        
    def check_user_location(self, user_lat, user_lng, user_time=None, user_weather=None):
        """Check if user is entering a high-risk zone"""
        if user_time is None:
            user_time = datetime.now()
        
        current_hour = user_time.hour
        current_weather = user_weather or self.current_weather
        
        alerts = []
        
        for hotspot in self.hotspots:
            # Calculate distance to hotspot center
            distance = self._calculate_distance(
                user_lat, user_lng,
                hotspot['center']['lat'], hotspot['center']['lng']
            )
            
            # If within 500 meters of hotspot
            if distance <= 0.5:  # 0.5km = 500 meters
                # Check if current conditions match risk patterns
                risk_match = self._check_risk_conditions(
                    hotspot, current_hour, current_weather
                )
                
                if risk_match['is_risky']:
                    alert = self._generate_alert(hotspot, risk_match, distance)
                    alerts.append(alert)
        
        return alerts
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates in kilometers"""
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon/2) * math.sin(delta_lon/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def _check_risk_conditions(self, hotspot, current_hour, current_weather):
        """Check if current conditions match hotspot risk patterns"""
        time_patterns = hotspot.get('time_patterns', {})
        weather_patterns = hotspot.get('weather_patterns', {})
        
        # Check time patterns
        is_peak_hour = current_hour in time_patterns.get('peak_hours', [])
        is_night_risk = time_patterns.get('is_night_hotspot', False) and current_hour >= 18
        
        # Check weather patterns
        current_weather_lower = current_weather.get('condition', '').lower()
        hotspot_weather = weather_patterns.get('most_common_weather', '').lower()
        
        is_weather_match = (
            'rain' in hotspot_weather and 'rain' in current_weather_lower
        ) or (
            current_weather_lower in hotspot_weather
        )
        
        # Calculate risk score
        risk_score = 0
        if is_peak_hour: risk_score += 2
        if is_night_risk: risk_score += 1
        if is_weather_match: risk_score += 2
        
        return {
            'is_risky': risk_score >= 2,  # At least 2 risk factors
            'is_peak_hour': is_peak_hour,
            'is_night_risk': is_night_risk,
            'is_weather_match': is_weather_match,
            'risk_score': risk_score,
            'hotspot_risk_level': hotspot['risk_level']
        }
    
    def _generate_alert(self, hotspot, risk_match, distance_km):
        """Generate alert message based on risk assessment"""
        # Convert distance to meters for display
        distance_m = int(distance_km * 1000)
        
        # Base alert message
        messages = []
        
        # Add distance information
        if distance_m < 100:
            proximity = "Approaching"
        elif distance_m < 300:
            proximity = "Near"
        else:
            proximity = "Approaching"
        
        messages.append(f"{proximity} high-risk accident zone ({distance_m}m ahead)")
        
        # Add risk factors
        risk_factors = []
        if risk_match['is_peak_hour']:
            risk_factors.append("peak accident hour")
        if risk_match['is_night_risk']:
            risk_factors.append("nighttime risk area")
        if risk_match['is_weather_match']:
            risk_factors.append("current weather conditions match historical accident patterns")
        
        if risk_factors:
            messages.append(f"High risk due to: {', '.join(risk_factors)}")
        
        # Add hotspot statistics
        stats = []
        if hotspot['total_accidents'] > 10:
            stats.append(f"{hotspot['total_accidents']} previous accidents")
        
        severity_dist = hotspot['severity_distribution']
        if severity_dist.get('dangerous', 0) > 0:
            stats.append(f"{severity_dist['dangerous']} dangerous accidents recorded")
        
        if stats:
            messages.append(f"Location history: {', '.join(stats)}")
        
        # Safety recommendations
        messages.append("Safety recommendation: Reduce speed, increase following distance")
        
        if hotspot['risk_level'] == 'high':
            messages.append("⚠️ EXTREME CAUTION REQUIRED ⚠️")
        
        # Construct final alert
        alert = {
            'type': 'risk_alert',
            'severity': hotspot['risk_level'],
            'message': " | ".join(messages),
            'hotspot_id': hotspot['cluster_id'],
            'distance_meters': distance_m,
            'risk_score': risk_match['risk_score'],
            'recommended_action': 'reduce_speed',
            'valid_until': (datetime.now() + timedelta(minutes=10)).isoformat()
        }
        
        return alert
