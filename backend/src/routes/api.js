const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');
const reportController = require('../controllers/reportController');
const aiController = require('../controllers/aiController');
const navigationController = require('../controllers/navigationController');
const analyticsController = require('../controllers/analyticsController');
const auth = require('../middleware/auth');

// Auth
router.post('/auth/register', authController.register);
router.post('/auth/login', authController.login);

// Reports
router.post('/reports', auth, reportController.createReport);
router.get('/reports', auth, reportController.getReports);
router.get('/reports/:id', auth, reportController.getReportById);

// AI
router.get('/ai/hotspots', aiController.getHotspots);
router.post('/ai/check-alerts', aiController.checkAlerts);

// Navigation
router.post('/navigation/route', navigationController.getSafeRoute);
router.get('/navigation/alerts', navigationController.getAlertsForArea);
router.post('/navigation/alert', navigationController.reportFalseAlert);

// Analytics
router.get('/analytics/summary', auth, analyticsController.getSummary);
router.get('/analytics/trends', auth, analyticsController.getTrends);
router.get('/analytics/heatmap', auth, analyticsController.getHeatmapData);

module.exports = router;
