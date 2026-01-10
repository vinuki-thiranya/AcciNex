const db = require('../config/database');

exports.getSummary = async (req, res) => {
  try {
    // Get today's accident count
    const todayResult = await db.query(
      `SELECT COUNT(*) as count FROM accident_reports 
       WHERE DATE(accident_time) = CURRENT_DATE`
    );

    // Get severity distribution
    const severityResult = await db.query(
      `SELECT severity, COUNT(*) as count 
       FROM accident_reports 
       WHERE accident_time >= NOW() - INTERVAL '30 days'
       GROUP BY severity`
    );

    // Get hourly distribution
    const hourlyResult = await db.query(
      `SELECT EXTRACT(HOUR FROM accident_time) as hour, COUNT(*) as accidents
       FROM accident_reports 
       WHERE accident_time >= NOW() - INTERVAL '7 days'
       GROUP BY hour
       ORDER BY hour`
    );

    const summary = {
      today_accidents: parseInt(todayResult.rows[0]?.count || 0),
      avg_response_time: 15, // This would come from actual response tracking
      severity_distribution: severityResult.rows.map(row => ({
        name: row.severity.charAt(0).toUpperCase() + row.severity.slice(1),
        value: parseInt(row.count)
      })),
      hourly_distribution: hourlyResult.rows.map(row => ({
        hour: `${String(row.hour).padStart(2, '0')}:00`,
        accidents: parseInt(row.accidents)
      }))
    };

    res.json(summary);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

exports.getTrends = async (req, res) => {
  try {
    const result = await db.query(
      `SELECT DATE(accident_time) as date, COUNT(*) as count, 
              AVG(CASE WHEN severity = 'dangerous' THEN 1 ELSE 0 END) as danger_rate
       FROM accident_reports 
       WHERE accident_time >= NOW() - INTERVAL '30 days'
       GROUP BY DATE(accident_time)
       ORDER BY date`
    );

    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

exports.getHeatmapData = async (req, res) => {
  try {
    const result = await db.query(
      `SELECT latitude, longitude, severity 
       FROM accident_reports 
       WHERE accident_time >= NOW() - INTERVAL '90 days'
       AND latitude IS NOT NULL 
       AND longitude IS NOT NULL`
    );

    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
