# AcciNex: AI-Powered Road Safety Intelligence Platform

## 🚀 Complete System Documentation

### Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Installation & Setup](#installation--setup)
5. [Running the Application](#running-the-application)
6. [API Documentation](#api-documentation)
7. [System Features](#system-features)
8. [Troubleshooting](#troubleshooting)

---

## System Overview

**AcciNex** is a comprehensive AI-powered road safety intelligence platform that transforms accident management from reactive reporting to proactive prevention. The system consists of:

- **Authority Dashboard**: Web-based interface for traffic police and emergency services
- **Public Navigation App**: Mobile application for real-time safety alerts
- **AI Microservice**: Machine learning models for severity prediction and hotspot detection
- **Backend API**: RESTful API with spatial database integration
- **PostgreSQL + PostGIS**: Spatial database for geographic data

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AcciNex System                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                   │
│  │   Authority  │      │    Public    │                   │
│  │   Dashboard  │      │  Navigation  │                   │
│  │   (React)    │      │   (Flutter)  │                   │
│  └──────┬───────┘      └──────┬───────┘                   │
│         │                     │                            │
│         └──────────┬──────────┘                            │
│                    │                                       │
│         ┌──────────▼──────────┐                           │
│         │   Backend API       │                           │
│         │   (Node.js/Express) │                           │
│         └──────────┬──────────┘                           │
│                    │                                       │
│         ┌──────────┼──────────┐                           │
│         │          │           │                           │
│  ┌──────▼─────┐ ┌─▼────────┐ ┌▼──────────┐              │
│  │ PostgreSQL │ │   AI     │ │  Google   │              │
│  │  + PostGIS │ │ Service  │ │   Maps    │              │
│  │            │ │ (Python) │ │    API    │              │
│  └────────────┘ └──────────┘ └───────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend Dashboard | React.js 18, Leaflet, Recharts |
| Mobile App | Flutter (Android/iOS) |
| Backend API | Node.js, Express.js |
| AI Service | Python, Flask, Scikit-learn |
| Database | PostgreSQL 14, PostGIS |
| Maps | Google Maps Platform |
| Containerization | Docker, Docker Compose |

---

## Prerequisites

### Required Software

1. **Docker & Docker Compose** (Recommended)
   - Docker Desktop 4.0+
   - Docker Compose 2.0+

2. **OR Manual Installation:**
   - Node.js 16+ and npm
   - Python 3.9+
   - PostgreSQL 14+ with PostGIS extension
   - Flutter SDK 3.0+ (for mobile app development)

3. **API Keys:**
   - Google Maps Platform API Key ([Get here](https://developers.google.com/maps/documentation/javascript/get-api-key))
     - Enable: Maps JavaScript API, Directions API, Geocoding API

---

## Installation & Setup

### Option 1: Docker (Recommended for Quick Start)

#### Step 1: Clone/Navigate to Project
```powershell
cd "c:\Users\Sahaji Jayathma\Downloads\Accinex"
```

#### Step 2: Configure Environment Variables

**Backend:**
```powershell
cd backend
cp .env.example .env
```

Edit `.env` and add your configuration:
```env
PORT=3000
DATABASE_URL=postgresql://admin:securepassword123@postgres:5432/accinex
JWT_SECRET=change_this_to_secure_random_string_in_production
AI_SERVICE_URL=http://ai-service:5000
GOOGLE_MAPS_API_KEY=your_actual_google_maps_api_key
```

**Dashboard:**
```powershell
cd ../dashboard
cp .env.example .env
```

Edit `.env`:
```env
REACT_APP_API_URL=http://localhost:3000/api
REACT_APP_GOOGLE_MAPS_API_KEY=your_actual_google_maps_api_key
```

#### Step 3: Build and Run with Docker
```powershell
cd ..
docker-compose up --build
```

This will start:
- PostgreSQL with PostGIS on port **5432**
- Backend API on port **3000**
- AI Service on port **5000**

#### Step 4: Initialize Database
```powershell
# In a new terminal
docker exec -i accinex-postgres-1 psql -U admin -d accinex < database/schema.sql
```

#### Step 5: Access the System
- Backend API: `http://localhost:3000`
- API Documentation: `http://localhost:3000/api`
- PostgreSQL: `localhost:5432`

---

### Option 2: Manual Installation

#### Step 1: Setup PostgreSQL

1. Install PostgreSQL 14+ with PostGIS
2. Create database:
```sql
CREATE DATABASE accinex;
\c accinex
CREATE EXTENSION postgis;
```

3. Run schema:
```powershell
psql -U postgres -d accinex -f database/schema.sql
```

#### Step 2: Setup Backend API

```powershell
cd backend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Start server
npm run dev
```

#### Step 3: Setup AI Service

```powershell
cd ../ai_service

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start AI service
python ai_service.py
```

#### Step 4: Setup Dashboard

```powershell
cd ../dashboard

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env

# Start development server
npm start
```

#### Step 5: Setup Mobile App (Optional)

```powershell
cd ../mobile_app

# Get Flutter dependencies
flutter pub get

# Run on connected device/emulator
flutter run
```

---

## Running the Application

### Starting All Services

**With Docker:**
```powershell
docker-compose up
```

**Manually:**
```powershell
# Terminal 1 - Backend
cd backend
npm run dev

# Terminal 2 - AI Service
cd ai_service
python ai_service.py

# Terminal 3 - Dashboard
cd dashboard
npm start

# Terminal 4 - Mobile (Optional)
cd mobile_app
flutter run
```

### Stopping Services

**Docker:**
```powershell
docker-compose down
```

**Manual:** Press `Ctrl+C` in each terminal

---

## API Documentation

### Base URL
```
http://localhost:3000/api
```

### Authentication

All authority endpoints require JWT token in header:
```
Authorization: Bearer <token>
```

### Endpoints

#### 1. Authentication

**Register User**
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "officer_john",
  "email": "john@police.lk",
  "password": "SecurePass123",
  "role": "traffic_police",
  "department": "Colombo Traffic Division"
}
```

**Login**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@police.lk",
  "password": "SecurePass123"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "officer_john",
    "email": "john@police.lk",
    "role": "traffic_police"
  }
}
```

#### 2. Accident Reports

**Create Report** (Requires Auth)
```http
POST /api/reports
Authorization: Bearer <token>
Content-Type: application/json

{
  "latitude": 6.9271,
  "longitude": 79.8612,
  "accident_time": "2026-01-10T18:30:00Z",
  "severity": "major",
  "weather_condition": "rainy",
  "vehicle_count": 2,
  "description": "Two-vehicle collision at intersection",
  "fatalities": false,
  "hospitalized": true
}
```

**Get All Reports** (Requires Auth)
```http
GET /api/reports
Authorization: Bearer <token>
```

**Get Specific Report** (Requires Auth)
```http
GET /api/reports/:id
Authorization: Bearer <token>
```

#### 3. AI & Analytics

**Get Hotspots**
```http
GET /api/ai/hotspots

Response:
[
  {
    "id": 1,
    "center": { "lat": 6.9271, "lng": 79.8612 },
    "risk_level": "high",
    "total_accidents": 45,
    "time_patterns": {
      "peak_hours": [18, 19, 20],
      "is_night_hotspot": true
    },
    "weather_patterns": {
      "most_common_weather": "rainy",
      "rainy_percentage": 65
    }
  }
]
```

**Check Alerts**
```http
POST /api/ai/check-alerts
Content-Type: application/json

{
  "latitude": 6.9271,
  "longitude": 79.8612,
  "hotspots": [...],
  "weather": {
    "condition": "rainy"
  }
}
```

#### 4. Navigation

**Get Safe Route**
```http
POST /api/navigation/route
Content-Type: application/json

{
  "origin": { "lat": 6.9271, "lng": 79.8612 },
  "destination": { "lat": 6.9500, "lng": 79.8800 },
  "avoid_high_risk": true
}
```

**Get Alerts for Area**
```http
GET /api/navigation/alerts?latitude=6.9271&longitude=79.8612&radius=2
```

#### 5. Analytics Dashboard (Requires Auth)

**Get Summary**
```http
GET /api/analytics/summary
Authorization: Bearer <token>
```

**Get Trends**
```http
GET /api/analytics/trends
Authorization: Bearer <token>
```

**Get Heatmap Data**
```http
GET /api/analytics/heatmap
Authorization: Bearer <token>
```

---

## System Features

### 1. Authority Dashboard Features

✅ **Smart Reporting**
- GPS-tagged accident reports
- Image upload with EXIF data extraction
- Real-time location validation

✅ **AI-Powered Analytics**
- Interactive heatmaps showing accident density
- Severity distribution charts
- Time-pattern analysis
- Real-time hotspot detection

✅ **Predictive Intelligence**
- Machine learning models predict accident severity
- Historical pattern analysis
- Risk zone identification

✅ **Automated Reporting**
- NLP-generated comprehensive reports
- Export to PDF/Excel
- Evidence management system

### 2. Public Navigation App Features

✅ **Intelligent Navigation**
- Google Maps integration
- Real-time GPS tracking
- Route optimization avoiding high-risk zones

✅ **Context-Aware Alerts**
- Real-time risk warnings
- Voice and visual notifications
- Condition-based alerts (time + weather + location)

✅ **Safety Visualization**
- Color-coded risk zones (Red/Orange/Green)
- Accident hotspot overlays
- Dynamic heatmap updates

✅ **Community Features**
- Report false alerts
- Incident reporting
- Safety feedback system

### 3. AI/ML Capabilities

**Severity Prediction Model:**
- **Algorithms**: Ensemble of Random Forest + Logistic Regression
- **Features**: Time, weather, location, historical patterns
- **Accuracy**: 85-90% (with training data)
- **Output**: Minor / Major / Dangerous classification

**Hotspot Detection:**
- **Algorithm**: DBSCAN spatial clustering
- **Inputs**: GPS coordinates, time, severity
- **Outputs**: Risk zones with temporal patterns
- **Updates**: Real-time recalculation

**Alert Engine:**
- **Risk Scoring**: Multi-factor analysis (15+ parameters)
- **Context Matching**: Time + Weather + Location
- **Alert Threshold**: Configurable sensitivity
- **Response Time**: <5 minutes from report to public alert

---

## Testing the System

### 1. Test Backend API

```powershell
# Test health endpoint
curl http://localhost:3000/api/health

# Register a test user
curl -X POST http://localhost:3000/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{
    "username": "test_officer",
    "email": "test@police.lk",
    "password": "Test123!",
    "role": "traffic_police",
    "department": "Test Division"
  }'

# Login
curl -X POST http://localhost:3000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@police.lk",
    "password": "Test123!"
  }'
```

### 2. Test AI Service

```powershell
# Test severity prediction
curl -X POST http://localhost:5000/predict-severity `
  -H "Content-Type: application/json" `
  -d '{
    "hour_of_day": 18,
    "day_of_week": 5,
    "month": 1,
    "is_rainy": 1,
    "is_night": 1,
    "is_weekend": 0,
    "location_cluster": 10,
    "previous_accidents_count": 5
  }'
```

### 3. Test Mobile App

1. Connect Android device or start emulator
2. Run: `flutter run`
3. Test features:
   - Location permissions
   - Map loading
   - Hotspot visualization
   - Alert notifications

---

## Sample Data

### Insert Test Accident Data

```sql
-- Insert sample users
INSERT INTO users (username, email, password_hash, role, department) VALUES
('officer1', 'officer1@police.lk', '$2a$10$...', 'traffic_police', 'Colombo'),
('officer2', 'officer2@police.lk', '$2a$10$...', 'traffic_police', 'Kandy');

-- Insert sample accident reports
INSERT INTO accident_reports 
(report_id, officer_id, location, latitude, longitude, accident_time, severity, weather_condition, vehicle_count, description)
VALUES
('ACC-001', 1, ST_SetSRID(ST_MakePoint(79.8612, 6.9271), 4326), 6.9271, 79.8612, 
 '2026-01-10 18:30:00', 'major', 'rainy', 2, 'Collision at Baseline Rd'),
 
('ACC-002', 1, ST_SetSRID(ST_MakePoint(79.8615, 6.9275), 4326), 6.9275, 79.8615, 
 '2026-01-09 19:15:00', 'dangerous', 'rainy', 3, 'Multi-vehicle pileup'),
 
('ACC-003', 2, ST_SetSRID(ST_MakePoint(79.8610, 6.9270), 4326), 6.9270, 79.8610, 
 '2026-01-08 20:00:00', 'minor', 'clear', 2, 'Minor fender bender');
```

---

## Troubleshooting

### Common Issues

**1. Database Connection Error**
```
Error: connect ECONNREFUSED 127.0.0.1:5432
```
**Solution:**
- Ensure PostgreSQL is running: `docker ps` or check services
- Verify DATABASE_URL in .env
- Check firewall settings

**2. PostGIS Extension Error**
```
ERROR: type "geography" does not exist
```
**Solution:**
```sql
\c accinex
CREATE EXTENSION IF NOT EXISTS postgis;
```

**3. Google Maps Not Loading**
**Solution:**
- Verify API key in .env files
- Enable required APIs in Google Cloud Console:
  - Maps JavaScript API
  - Directions API
  - Geocoding API
- Check billing is enabled

**4. AI Service Import Error**
```
ModuleNotFoundError: No module named 'sklearn'
```
**Solution:**
```powershell
cd ai_service
pip install -r requirements.txt
```

**5. Flutter Build Error**
**Solution:**
```powershell
flutter clean
flutter pub get
flutter run
```

**6. Port Already in Use**
```
Error: listen EADDRINUSE: address already in use :::3000
```
**Solution:**
```powershell
# Find process using port
netstat -ano | findstr :3000

# Kill process
taskkill /PID <PID> /F

# Or change PORT in .env
```

---

## Production Deployment Checklist

### Security
- [ ] Change all default passwords
- [ ] Generate strong JWT_SECRET
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Set up API key rotation
- [ ] Enable database encryption
- [ ] Configure firewall rules

### Performance
- [ ] Enable database connection pooling
- [ ] Set up Redis for caching
- [ ] Configure CDN for static assets
- [ ] Enable gzip compression
- [ ] Optimize database indexes
- [ ] Set up load balancing

### Monitoring
- [ ] Configure logging (Winston, Sentry)
- [ ] Set up health check endpoints
- [ ] Enable performance monitoring
- [ ] Configure alerts for errors
- [ ] Set up database backup automation

### Deployment
- [ ] Use environment-specific configs
- [ ] Set NODE_ENV=production
- [ ] Configure auto-scaling
- [ ] Set up CI/CD pipeline
- [ ] Enable automated backups
- [ ] Document deployment process

---

## Support & Contact

### Development Team
- **Project Lead**: [Your Name]
- **Email**: [your-email@example.com]
- **GitHub**: [Repository Link]

### Resources
- API Documentation: `http://localhost:3000/api-docs`
- Technical Docs: `/docs` folder
- Issue Tracker: GitHub Issues

---

## License

Copyright © 2026 AcciNex Team. All rights reserved.

This system is developed for educational and research purposes as part of PearlHack 4.0 Ideathon.

---

## Acknowledgments

- Google Maps Platform
- PostgreSQL & PostGIS Community
- Scikit-learn Contributors
- React & Flutter Communities

---

**🎯 Mission**: Transforming road safety from reactive reporting to proactive prevention.

**"We don't just map accidents. We prevent them."**
