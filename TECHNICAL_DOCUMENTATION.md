# AcciNex System Architecture & Technical Details

## 1. System Components

### 1.1 Backend API (Node.js + Express)

**Purpose**: Central API gateway handling all business logic

**Key Features**:
- RESTful API endpoints
- JWT-based authentication
- Role-based access control (RBAC)
- PostgreSQL with PostGIS integration
- Real-time data processing

**Key Files**:
- `src/index.js` - Express server initialization
- `src/config/database.js` - PostgreSQL connection pool
- `src/controllers/*` - Request handlers
- `src/middleware/auth.js` - JWT authentication
- `src/routes/api.js` - API route definitions

**Dependencies**:
```json
{
  "express": "Server framework",
  "pg": "PostgreSQL client",
  "bcryptjs": "Password hashing",
  "jsonwebtoken": "JWT tokens",
  "axios": "HTTP client",
  "cors": "CORS middleware",
  "multer": "File upload"
}
```

### 1.2 AI Microservice (Python + Flask)

**Purpose**: Machine learning models for prediction and analysis

**Key Features**:
- Severity prediction using ensemble models
- Hotspot detection with DBSCAN
- Real-time alert generation
- Pattern analysis

**Key Files**:
- `ai_service.py` - Flask API server
- `severity_prediction.py` - ML model for severity classification
- `hotspot_detection.py` - Spatial clustering algorithm
- `alert_engine.py` - Risk assessment engine

**Models**:
1. **Severity Predictor**
   - Random Forest Classifier (100 estimators)
   - Logistic Regression
   - Ensemble averaging for final prediction

2. **Hotspot Detector**
   - DBSCAN clustering (eps=0.01, min_samples=3)
   - Haversine distance metric for geographic data
   - Temporal pattern analysis

3. **Alert Engine**
   - Multi-factor risk scoring
   - Context matching (time + weather + location)
   - Distance-based alert generation

### 1.3 Database (PostgreSQL + PostGIS)

**Purpose**: Spatial database for geographic data

**Key Features**:
- Geographic data types (GEOGRAPHY, GEOMETRY)
- Spatial indexing with GiST
- Complex spatial queries
- JSONB for flexible data storage

**Schema**:
```
users
├── id (SERIAL PRIMARY KEY)
├── username, email, password_hash
├── role (traffic_police | emergency_services | road_safety_admin)
└── department, created_at

accident_reports
├── id (SERIAL PRIMARY KEY)
├── report_id (UNIQUE)
├── officer_id (FK → users)
├── location (GEOGRAPHY Point)
├── latitude, longitude
├── accident_time
├── severity (minor | major | dangerous)
├── weather_condition
├── vehicle_count
└── description

hotspots
├── id (SERIAL PRIMARY KEY)
├── location (GEOGRAPHY Polygon)
├── center_point (GEOGRAPHY Point)
├── risk_level (low | medium | high)
├── time_patterns (JSONB)
└── weather_patterns (JSONB)

alerts
├── id (SERIAL PRIMARY KEY)
├── user_id (FK → users)
├── location (GEOGRAPHY Point)
├── hotspot_id (FK → hotspots)
└── message, triggered_time
```

### 1.4 Authority Dashboard (React.js)

**Purpose**: Web interface for authorities to manage accident data

**Key Features**:
- Interactive Leaflet maps
- Real-time data visualization
- Analytics dashboard with Recharts
- Report submission forms
- WebSocket for live updates

**Key Components**:
- `Dashboard.jsx` - Main dashboard layout
- Map visualization with heatmaps
- Severity distribution charts
- Time-pattern analysis graphs

### 1.5 Mobile Navigation App (Flutter)

**Purpose**: Public-facing mobile app for safety alerts

**Key Features**:
- Google Maps integration
- Real-time GPS tracking
- Risk zone visualization
- Context-aware alerts
- Incident reporting

---

## 2. Data Flow

### 2.1 Accident Report Submission Flow

```
1. Officer submits report via Dashboard
   ↓
2. Backend receives POST /api/reports
   ↓
3. Data validated and stored in PostgreSQL
   ↓
4. Backend calls AI Service for severity prediction
   ↓
5. AI Service returns prediction
   ↓
6. Backend triggers hotspot recalculation
   ↓
7. Hotspots updated in database
   ↓
8. WebSocket broadcasts update to connected clients
   ↓
9. Dashboard updates in real-time
```

### 2.2 Alert Generation Flow

```
1. User location tracked by mobile app
   ↓
2. App sends location to GET /api/navigation/alerts
   ↓
3. Backend queries nearby hotspots from database
   ↓
4. Backend calls AI Service POST /check-alerts
   ↓
5. AI Service evaluates risk conditions:
   - Distance to hotspot
   - Current time vs peak hours
   - Weather condition match
   - Risk score calculation
   ↓
6. If risk_score >= threshold:
   - Generate alert message
   - Return alert to backend
   ↓
7. Backend sends alerts to mobile app
   ↓
8. App displays visual + voice warning
```

---

## 3. AI/ML Implementation Details

### 3.1 Severity Prediction Model

**Input Features** (10 features):
- `hour_of_day` (0-23)
- `day_of_week` (0-6, 0=Monday)
- `month` (1-12)
- `is_rainy` (0/1)
- `is_night` (0/1, 18:00-06:00)
- `is_weekend` (0/1)
- `location_cluster` (K-Means cluster ID)
- `previous_accidents_count`
- `road_type` (optional)
- `speed_limit` (optional)

**Training Process**:
```python
# 1. Load data from database
df = load_training_data(db_connection)

# 2. Feature engineering
df = add_location_clusters(df)  # K-Means n_clusters=50
df = add_temporal_features(df)

# 3. Train ensemble
rf_model = RandomForestClassifier(n_estimators=100)
lr_model = LogisticRegression(max_iter=1000)

# 4. Prediction (ensemble averaging)
prediction = (rf_pred + lr_pred) / 2
```

**Output**:
```json
{
  "severity": "major",
  "confidence": 0.87,
  "probabilities": {
    "minor": 0.10,
    "major": 0.67,
    "dangerous": 0.23
  }
}
```

### 3.2 Hotspot Detection with DBSCAN

**Algorithm**: DBSCAN (Density-Based Spatial Clustering)

**Parameters**:
- `eps = 0.01` (~1km in decimal degrees)
- `min_samples = 3` (minimum accidents to form cluster)
- `metric = 'haversine'` (great-circle distance)

**Process**:
```python
# 1. Convert coordinates to radians
coords = np.radians(df[['latitude', 'longitude']])

# 2. Perform clustering
clusters = DBSCAN(eps=0.01, min_samples=3, metric='haversine')
labels = clusters.fit_predict(coords)

# 3. For each cluster:
for cluster_id in unique_labels:
    # Calculate centroid
    center = calculate_center(cluster_coords)
    
    # Calculate risk score
    risk_score = weighted_severity_sum / total_accidents
    
    # Analyze temporal patterns
    time_patterns = analyze_peak_hours(cluster_data)
    
    # Analyze weather patterns
    weather_patterns = analyze_weather(cluster_data)
    
    # Generate recommendations
    recommendations = generate_safety_reco(risk_level, patterns)
```

**Hotspot Output**:
```json
{
  "cluster_id": 5,
  "center": { "lat": 6.9271, "lng": 79.8612 },
  "bounding_box": {
    "north": 6.9280,
    "south": 6.9262,
    "east": 79.8620,
    "west": 79.8604
  },
  "risk_level": "high",
  "total_accidents": 45,
  "severity_distribution": {
    "minor": 10,
    "major": 25,
    "dangerous": 10
  },
  "time_patterns": {
    "peak_hours": [18, 19, 20],
    "is_night_hotspot": true,
    "busiest_day": 5
  },
  "weather_patterns": {
    "most_common_weather": "rainy",
    "rainy_percentage": 65.0
  },
  "recommendations": [
    "Immediate safety audit required",
    "Improve street lighting",
    "Increase police patrols during hours: 18, 19, 20"
  ]
}
```

### 3.3 Alert Engine Risk Scoring

**Risk Score Calculation**:
```python
risk_score = 0

if is_peak_hour:           risk_score += 2
if is_night_risk:          risk_score += 1
if is_weather_match:       risk_score += 2
if hotspot_risk == 'high': risk_score += 1

# Alert generated if risk_score >= 2
```

**Alert Message Template**:
```
[PROXIMITY] high-risk accident zone ([DISTANCE]m ahead)
| High risk due to: [RISK_FACTORS]
| Location history: [STATISTICS]
| Safety recommendation: [ACTION]
| [SEVERITY_WARNING]
```

---

## 4. API Integration

### 4.1 Google Maps Platform

**APIs Used**:
1. **Maps JavaScript API** - Dashboard map rendering
2. **Directions API** - Route calculation
3. **Geocoding API** - Address ↔ Coordinates conversion

**Usage in Backend**:
```javascript
// Get route from Google Directions API
const response = await axios.get(
  'https://maps.googleapis.com/maps/api/directions/json',
  {
    params: {
      origin: `${lat},${lng}`,
      destination: `${dest_lat},${dest_lng}`,
      key: process.env.GOOGLE_MAPS_API_KEY,
      alternatives: true
    }
  }
);
```

### 4.2 Weather API Integration (Optional)

For production, integrate with weather services:
```javascript
// Example with OpenWeatherMap
const weather = await axios.get(
  `https://api.openweathermap.org/data/2.5/weather`,
  {
    params: {
      lat: latitude,
      lon: longitude,
      appid: process.env.WEATHER_API_KEY
    }
  }
);
```

---

## 5. Security Implementation

### 5.1 Authentication Flow

1. **Registration**:
   - Password hashed with bcryptjs (10 salt rounds)
   - User created in database
   - No token returned (must login)

2. **Login**:
   - Password verified with bcrypt.compare()
   - JWT token generated with 1-day expiration
   - Token includes: user_id, role, username

3. **Protected Routes**:
   - Token extracted from Authorization header
   - JWT verified with secret key
   - User object attached to req.user

### 5.2 Role-Based Access Control

**Roles**:
- `traffic_police` - Create/view reports
- `emergency_services` - View reports, access analytics
- `road_safety_admin` - Full access + train models
- `public_user` - Limited access (navigation only)

**Implementation**:
```javascript
// middleware/roleCheck.js
const roleCheck = (allowedRoles) => {
  return (req, res, next) => {
    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Access denied' });
    }
    next();
  };
};

// Usage
router.post('/reports', auth, roleCheck(['traffic_police']), reportController.create);
```

---

## 6. Performance Optimization

### 6.1 Database Indexing

```sql
-- Spatial indexes for fast geographic queries
CREATE INDEX idx_location ON accident_reports USING GIST (location);
CREATE INDEX idx_hotspot_location ON hotspots USING GIST (location);

-- B-tree indexes for common queries
CREATE INDEX idx_time ON accident_reports (accident_time);
CREATE INDEX idx_severity ON accident_reports (severity);
CREATE INDEX idx_user_role ON users (role);
```

### 6.2 Query Optimization

**Spatial Query Example**:
```sql
-- Find accidents within 2km radius
SELECT *, 
       ST_Distance(
         location::geography,
         ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography
       ) / 1000 as distance_km
FROM accident_reports
WHERE ST_DWithin(
  location::geography,
  ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography,
  2000  -- 2km in meters
)
ORDER BY distance_km;
```

### 6.3 Caching Strategy

For production, implement Redis caching:
```javascript
// Cache hotspots for 5 minutes
const cachedHotspots = await redis.get('hotspots');
if (cachedHotspots) {
  return JSON.parse(cachedHotspots);
}

const hotspots = await db.query('SELECT * FROM hotspots');
await redis.setex('hotspots', 300, JSON.stringify(hotspots));
```

---

## 7. Deployment Architecture

### Production Deployment

```
                    ┌─────────────┐
                    │   Nginx     │
                    │   (SSL)     │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
      ┌───────▼────────┐        ┌──────▼──────┐
      │  Node.js API   │        │   React     │
      │  (PM2 Cluster) │        │   (Static)  │
      └───────┬────────┘        └─────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼────┐ ┌──▼────────┐
│ Redis │ │Python │ │PostgreSQL │
│       │ │  AI   │ │ + PostGIS │
└───────┘ └───────┘ └───────────┘
```

**Recommended Stack**:
- **Server**: AWS EC2 / GCP Compute Engine
- **Database**: AWS RDS PostgreSQL with PostGIS
- **Cache**: AWS ElastiCache (Redis)
- **Storage**: AWS S3 (images/evidence)
- **CDN**: CloudFront / Cloudflare
- **Monitoring**: CloudWatch / Datadog
- **CI/CD**: GitHub Actions / GitLab CI

---

## 8. Testing Strategy

### 8.1 Unit Tests (Backend)

```javascript
// Example test for report creation
describe('POST /api/reports', () => {
  it('should create accident report with valid data', async () => {
    const response = await request(app)
      .post('/api/reports')
      .set('Authorization', `Bearer ${validToken}`)
      .send({
        latitude: 6.9271,
        longitude: 79.8612,
        accident_time: '2026-01-10T18:30:00Z',
        severity: 'major',
        weather_condition: 'rainy',
        vehicle_count: 2
      });
    
    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('report_id');
  });
});
```

### 8.2 Integration Tests (AI Service)

```python
# Test hotspot detection
def test_hotspot_detection():
    # Create sample data
    df = pd.DataFrame({
        'latitude': [6.9271, 6.9275, 6.9270],
        'longitude': [79.8612, 79.8615, 79.8610],
        'severity': ['major', 'dangerous', 'minor'],
        'accident_time': [datetime.now()] * 3
    })
    
    # Detect hotspots
    detector = HotspotDetector()
    hotspots = detector.detect_hotspots(df)
    
    # Assertions
    assert len(hotspots) > 0
    assert hotspots[0]['risk_level'] in ['low', 'medium', 'high']
    assert 'time_patterns' in hotspots[0]
```

---

## 9. Future Enhancements

### Phase 2 Features
- [ ] Real-time weather API integration
- [ ] WebSocket for live alerts
- [ ] Voice alerts in mobile app
- [ ] Predictive accident forecasting
- [ ] Integration with traffic cameras
- [ ] Automated emergency dispatch

### Phase 3 Features
- [ ] Computer vision for accident detection from images
- [ ] Deep learning models (CNN, LSTM)
- [ ] Connected vehicle integration (V2X)
- [ ] Multi-language support (Sinhala, Tamil)
- [ ] Offline mode for mobile app

---

## 10. Maintenance & Monitoring

### Log Files
- Backend: `logs/backend.log`
- AI Service: `logs/ai_service.log`
- Database: PostgreSQL logs

### Health Checks
```
GET /api/health - Backend health
GET /health - AI service health
```

### Metrics to Monitor
- API response times
- Database connection pool usage
- AI model prediction latency
- Alert generation rate
- User engagement metrics

---

**Last Updated**: January 10, 2026  
**Version**: 1.0.0  
**Status**: Production Ready
