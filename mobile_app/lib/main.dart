import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:location/location.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(const AcciNexApp());
}

class AcciNexApp extends StatelessWidget {
  const AcciNexApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AcciNex',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.red),
        useMaterial3: true,
      ),
      home: const NavigationScreen(),
    );
  }
}

class NavigationScreen extends StatefulWidget {
  const NavigationScreen({super.key});

  @override
  State<NavigationScreen> createState() => _NavigationScreenState();
}

class _NavigationScreenState extends State<NavigationScreen> {
  GoogleMapController? _controller;
  final Location _location = Location();
  LatLng _currentPos = const LatLng(6.9271, 79.8612);
  final Set<Marker> _markers = {};
  final List<dynamic> _alerts = [];

  @override
  void initState() {
    super.initState();
    _initLocation();
  }

  void _initLocation() async {
    bool serviceEnabled = await _location.serviceEnabled();
    if (!serviceEnabled) {
      serviceEnabled = await _location.requestService();
      if (!serviceEnabled) return;
    }

    PermissionStatus permission = await _location.hasPermission();
    if (permission == PermissionStatus.denied) {
      permission = await _location.requestPermission();
      if (permission != PermissionStatus.granted) return;
    }

    _location.onLocationChanged.listen((LocationData locationData) {
      if (locationData.latitude != null && locationData.longitude != null) {
        setState(() {
          _currentPos = LatLng(locationData.latitude!, locationData.longitude!);
          _checkForAlerts();
        });
      }
    });
  }

  void _checkForAlerts() async {
    // Simulated API call for checking alerts
    // http.post(Uri.parse('http://YOUR_BACKEND_URL/api/ai/check-alerts'), body: ...)
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AcciNex Safe Navigator'),
        backgroundColor: Colors.red.shade800,
        foregroundColor: Colors.white,
      ),
      body: Stack(
        children: [
          GoogleMap(
            initialCameraPosition: CameraPosition(target: _currentPos, zoom: 15),
            onMapCreated: (controller) => _controller = controller,
            myLocationEnabled: true,
            markers: _markers,
            trafficEnabled: true,
          ),
          if (_alerts.isNotEmpty)
            Positioned(
              top: 10,
              left: 10,
              right: 10,
              child: Card(
                color: Colors.amber.shade100,
                child: Padding(
                  padding: const EdgeInsets.all(12.0),
                  child: Row(
                    children: [
                      const Icon(Icons.warning, color: Colors.red),
                      const SizedBox(width: 10),
                      const Expanded(
                        child: Text(
                          'High-risk zone ahead! Rainy evening pattern detected. Please reduce speed.',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        label: const Text('Report Accident'),
        icon: const Icon(Icons.add_alert),
        backgroundColor: Colors.red,
      ),
    );
  }
}
