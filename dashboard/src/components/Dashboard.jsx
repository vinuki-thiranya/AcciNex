import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import HeatmapLayer from 'react-leaflet-heatmap-layer';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  PieChart, Pie, Cell, ResponsiveContainer 
} from 'recharts';
import 'leaflet/dist/leaflet.css';

const AuthorityDashboard = () => {
  const [reports, setReports] = useState([]);
  const [hotspots, setHotspots] = useState([]);
  const [stats, setStats] = useState({
    today_accidents: 0,
    avg_response_time: 15,
    severity_distribution: [
      { name: 'Minor', value: 45 },
      { name: 'Major', value: 30 },
      { name: 'Dangerous', value: 25 }
    ],
    hourly_distribution: [
      { hour: '08:00', accidents: 5 },
      { hour: '12:00', accidents: 8 },
      { hour: '18:00', accidents: 12 },
      { hour: '20:00', accidents: 7 }
    ]
  });

  useEffect(() => {
    // In a real app, fetch from backend
    // fetchDashboardData();
  }, []);

  return (
    <div style={{ padding: '20px', backgroundColor: '#f5f7fa', minHeight: '100vh', fontFamily: 'sans-serif' }}>
      <header style={{ marginBottom: '30px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ color: '#1a1a1a' }}>AcciNex Authority Dashboard</h1>
        <div style={{ display: 'flex', gap: '20px' }}>
          <div style={{ padding: '15px 25px', backgroundColor: '#fff', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.05)' }}>
            <h3 style={{ margin: 0, color: '#666', fontSize: '14px' }}>Today's Accidents</h3>
            <p style={{ margin: '5px 0 0 0', fontSize: '24px', fontWeight: 'bold', color: '#e53e3e' }}>{stats.today_accidents}</p>
          </div>
          <div style={{ padding: '15px 25px', backgroundColor: '#fff', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.05)' }}>
            <h3 style={{ margin: 0, color: '#666', fontSize: '14px' }}>Active Hotspots</h3>
            <p style={{ margin: '5px 0 0 0', fontSize: '24px', fontWeight: 'bold', color: '#d69e2e' }}>{hotspots.length}</p>
          </div>
        </div>
      </header>

      <main style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '30px' }}>
        <section style={{ backgroundColor: '#fff', borderRadius: '15px', padding: '10px', boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }}>
          <div style={{ height: '600px', width: '100%', borderRadius: '10px', overflow: 'hidden' }}>
            <MapContainer 
              center={[6.9271, 79.8612]} 
              zoom={12}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; OpenStreetMap contributors'
              />
              
              <HeatmapLayer
                points={reports.map(r => ({ lat: r.latitude, lng: r.longitude, intensity: 1 }))}
                longitudeExtractor={p => p.lng}
                latitudeExtractor={p => p.lat}
                intensityExtractor={p => p.intensity}
                radius={20}
              />
              
              {hotspots.map(hotspot => (
                <CircleMarker
                  key={hotspot.id}
                  center={[hotspot.center.lat, hotspot.center.lng]}
                  radius={10}
                  color={hotspot.risk_level === 'high' ? 'red' : 'orange'}
                >
                  <Popup>
                    <strong>{hotspot.risk_level.toUpperCase()} RISK HOTSPOT</strong><br/>
                    Accidents: {hotspot.accident_count}
                  </Popup>
                </CircleMarker>
              ))}
            </MapContainer>
          </div>
        </section>

        <section style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
          <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '15px', boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }}>
            <h3 style={{ marginBottom: '20px' }}>Severity Distribution</h3>
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie
                  data={stats.severity_distribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  <Cell fill="#4299e1" />
                  <Cell fill="#ed8936" />
                  <Cell fill="#e53e3e" />
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div style={{ backgroundColor: '#fff', padding: '20px', borderRadius: '15px', boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }}>
            <h3 style={{ marginBottom: '20px' }}>Accidents by Time</h3>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={stats.hourly_distribution}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="accidents" fill="#4c51bf" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
      </main>
    </div>
  );
};

export default AuthorityDashboard;
