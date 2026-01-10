-- Create PostgreSQL database with PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Users Table (Authorities)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('traffic_police', 'emergency_services', 'road_safety_admin', 'public_user')),
    department VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Accident Reports Table
CREATE TABLE accident_reports (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(50) UNIQUE NOT NULL,
    officer_id INTEGER REFERENCES users(id),
    location GEOGRAPHY(Point, 4326) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    accident_time TIMESTAMP NOT NULL,
    severity VARCHAR(20) CHECK (severity IN ('minor', 'major', 'dangerous')),
    predicted_severity VARCHAR(20),
    confidence_score DECIMAL(5, 2),
    weather_condition VARCHAR(50),
    fatalities BOOLEAN DEFAULT FALSE,
    hospitalized BOOLEAN DEFAULT FALSE,
    vehicle_count INTEGER,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_location ON accident_reports USING GIST (location);
CREATE INDEX idx_time ON accident_reports (accident_time);
CREATE INDEX idx_severity ON accident_reports (severity);

-- Accident Evidence Table
CREATE TABLE accident_evidence (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES accident_reports(id),
    image_url TEXT NOT NULL,
    exif_data JSONB,
    gps_latitude DECIMAL(10, 8),
    gps_longitude DECIMAL(11, 8),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hotspots Table (AI-generated)
CREATE TABLE hotspots (
    id SERIAL PRIMARY KEY,
    location GEOGRAPHY(Polygon, 4326) NOT NULL,
    center_point GEOGRAPHY(Point, 4326),
    risk_level VARCHAR(20) CHECK (risk_level IN ('low', 'medium', 'high')),
    accident_count INTEGER DEFAULT 0,
    severity_score DECIMAL(5, 2),
    time_patterns JSONB, -- Stores JSON of peak hours
    weather_patterns JSONB, -- Stores JSON of weather correlations
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hotspot_location ON hotspots USING GIST (location);

-- Alert History Table
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    location GEOGRAPHY(Point, 4326),
    hotspot_id INTEGER REFERENCES hotspots(id),
    alert_type VARCHAR(50),
    message TEXT NOT NULL,
    triggered_time TIMESTAMP NOT NULL,
    acknowledged BOOLEAN DEFAULT FALSE
);
