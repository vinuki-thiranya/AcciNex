const db = require('../config/database');
const axios = require('axios');

exports.getHotspots = async (req, res) => {
  try {
    const result = await db.query('SELECT * FROM hotspots');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

exports.checkAlerts = async (req, res) => {
  const { latitude, longitude, weather } = req.body;
  try {
    // Get all hotspots from DB
    const hotspotsResult = await db.query('SELECT * FROM hotspots');
    const hotspots = hotspotsResult.rows;

    // Call AI service to check if user is in a risk zone
    const response = await axios.post(`${process.env.AI_SERVICE_URL || 'http://localhost:5000'}/check-alerts`, {
      latitude,
      longitude,
      hotspots,
      weather
    });

    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
