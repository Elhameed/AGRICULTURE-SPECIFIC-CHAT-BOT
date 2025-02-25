import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  TextEditingController _controller = TextEditingController();
  List<Map<String, String>> messages = [];

  // Function to send the user's message to FastAPI and receive a response
  Future<void> _sendMessage() async {
    if (_controller.text.isNotEmpty) {
      setState(() {
        messages.add({"sender": "user", "text": _controller.text});
      });

      // Send the message to FastAPI backend
      var response = await http.post(
        Uri.parse(
            'http://localhost:8000/chat'), // Change to your FastAPI server URL
        headers: {"Content-Type": "application/json"},
        body: json.encode({"message": _controller.text}),
      );

      if (response.statusCode == 200) {
        var responseData = json.decode(response.body);
        setState(() {
          messages.add({
            "sender": "bot",
            "text": responseData["response"],
          });
        });
      } else {
        setState(() {
          messages.add({
            "sender": "bot",
            "text": "Sorry, something went wrong. Please try again later.",
          });
        });
      }

      _controller.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("COVID-19 Chatbot"),
        backgroundColor: Colors.green.shade700,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: EdgeInsets.all(10),
              itemCount: messages.length,
              itemBuilder: (context, index) {
                bool isUser = messages[index]["sender"] == "user";
                return Align(
                  alignment:
                      isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: EdgeInsets.symmetric(vertical: 5),
                    padding: EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color:
                          isUser ? Colors.green.shade300 : Colors.grey.shade200,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      messages[index]["text"]!,
                      style: TextStyle(fontSize: 16),
                    ),
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: "Type a message...",
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(30),
                      ),
                      contentPadding: EdgeInsets.symmetric(horizontal: 15),
                    ),
                  ),
                ),
                SizedBox(width: 8),
                FloatingActionButton(
                  onPressed: _sendMessage,
                  backgroundColor: Colors.green.shade700,
                  child: Icon(Icons.send, color: Colors.white),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
