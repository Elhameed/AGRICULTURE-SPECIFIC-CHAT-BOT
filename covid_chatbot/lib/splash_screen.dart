import 'package:flutter/material.dart';
import 'chat_screen.dart';

class SplashScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.green.shade700,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.agriculture, size: 100, color: Colors.white),
            SizedBox(height: 20),
            Text(
              "Hello, I'm AgriBot",
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white),
            ),
            SizedBox(height: 10),
            Text(
              "How can I assist you today?",
              style: TextStyle(fontSize: 16, color: Colors.white70),
            ),
            SizedBox(height: 30),
            ElevatedButton(
              onPressed: () {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => ChatScreen()),
                );
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.white,
                foregroundColor: Colors.green.shade700,
                padding: EdgeInsets.symmetric(horizontal: 30, vertical: 12),
                textStyle: TextStyle(fontSize: 18),
              ),
              child: Text("Start Chat"),
            ),
          ],
        ),
      ),
    );
  }
}
