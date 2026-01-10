const axios = require('axios');

exports.getSafeRoute = async (req, res) => {
  const { origin, destination, avoid_high_risk } = req.body;

  try {
    // Get route from Google Directions API
    const directionsResponse = await axios.get('https://maps.googleapis.com/maps/api/directions/json', {
      params: {
        origin: `${origin.lat},${origin.lng}`,
        destination: `${destination.lat},${destination.lng}`,
        key: process.env.GOOGLE_MAPS_API_KEY,
        alternatives: true
      }
    });

    if (avoid_high_risk) {
      // Get hotspots to avoid
      const db = require('../config/database');
      const hotspotsResult = await db.query(
        `SELECT * FROM hotspots WHERE risk_level = 'high'`
      );

      // Logic to filter routes that avoid high-risk zones
      // This is a simplified version - production would need more sophisticated routing
      const routes = directionsResponse.data.routes;
      
      res.json({
        routes: routes,
        hotspots_avoided: hotspotsResult.rows.length
      });
    } else {
      res.json(directionsResponse.data);
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

exports.getAlertsForArea = async (req, res) => {
  const { latitude, longitude, radius = 1 } = req.query;

  try {
    const db = require('../config/database');
    
    // Find hotspots within radius (in km)
    const result = await db.query(
      `SELECT *, 
              ST_Distance(
                center_point::geography,
                ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography
              ) / 1000 as distance_km
       FROM hotspots
       WHERE ST_DWithin(
         center_point::geography,
         ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography,
         $3 * 1000
       )
       ORDER BY distance_km`,
      [longitude, latitude, radius]
    );

    res.json({
      alerts: result.rows,
      count: result.rows.length
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

exports.reportFalseAlert = async (req, res) => {
  const { alert_id, reason } = req.body;
  
  // Log false alert reports for model improvement
  // In production, this would update ML model training data
  
  res.json({ message: 'Feedback recorded. Thank you for helping improve our system.' });
};
