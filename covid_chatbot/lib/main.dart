import 'package:flutter/material.dart';
import 'splash_screen.dart';  // Import Splash Screen

void main() {
  runApp(AgriBotApp());
}

class AgriBotApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false, // Hide debug banner
      title: 'AgriBot',
      theme: ThemeData(
        primarySwatch: Colors.green, // Set green theme
      ),
      home: SplashScreen(), // Start with Splash Screen
    );
  }
}
