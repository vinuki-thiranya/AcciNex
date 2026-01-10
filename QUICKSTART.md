# AcciNex Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Docker Desktop installed
- Google Maps API key

### Step 1: Configure Environment
```powershell
cd backend
copy .env.example .env
```

Edit `.env` and add your Google Maps API key:
```
GOOGLE_MAPS_API_KEY=your_key_here
```

### Step 2: Start Services
```powershell
cd ..
docker-compose up --build
```

### Step 3: Initialize Database
Open new terminal:
```powershell
docker exec -i accinex-postgres-1 psql -U admin -d accinex < database\schema.sql
```

### Step 4: Access System
- Backend API: http://localhost:3000/api
- Test endpoint: http://localhost:3000/api/health

### Step 5: Create Test User
```powershell
curl -X POST http://localhost:3000/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{
    "username": "test_officer",
    "email": "test@police.lk",
    "password": "Test123!",
    "role": "traffic_police",
    "department": "Test Division"
  }'
```

### Step 6: Login and Get Token
```powershell
curl -X POST http://localhost:3000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@police.lk",
    "password": "Test123!"
  }'
```

Save the returned `token` for authenticated requests.

### Step 7: Create Sample Accident Report
```powershell
curl -X POST http://localhost:3000/api/reports `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE" `
  -d '{
    "latitude": 6.9271,
    "longitude": 79.8612,
    "accident_time": "2026-01-10T18:30:00Z",
    "severity": "major",
    "weather_condition": "rainy",
    "vehicle_count": 2,
    "description": "Test accident report"
  }'
```

### Step 8: View Hotspots
```powershell
curl http://localhost:3000/api/ai/hotspots
```

## 🎨 Frontend Setup

### Dashboard
```powershell
cd dashboard
npm install
copy .env.example .env
# Edit .env with your API URL and Google Maps key
npm start
```

Access at: http://localhost:3001

### Mobile App
```powershell
cd mobile_app
flutter pub get
flutter run
```

## 📊 Sample Test Scenario

1. **Create 3-5 accident reports** in the same area (vary time/weather)
2. **System automatically detects hotspot** using DBSCAN clustering
3. **View on dashboard** - hotspot appears on map
4. **Test mobile app** - navigate near hotspot to receive alert

## 🛠️ Troubleshooting

**Database not connecting?**
```powershell
docker ps  # Check if postgres container is running
docker logs accinex-postgres-1  # Check logs
```

**AI Service error?**
```powershell
docker logs accinex-ai-service-1
```

**Backend error?**
```powershell
docker logs accinex-backend-1
```

## 📚 Next Steps

1. Read full [README.md](README.md) for detailed documentation
2. Explore API endpoints in Postman
3. Import sample data for testing
4. Customize AI models with your data

## 💡 Key Features to Test

✅ User registration and authentication  
✅ Accident report submission with GPS  
✅ AI severity prediction  
✅ Hotspot detection with DBSCAN  
✅ Real-time alerts based on location  
✅ Dashboard analytics and heatmaps  
✅ Safe route navigation  

---

**Need Help?** Check the main README or contact the development team.
