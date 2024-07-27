// ignore_for_file: file_names, prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';

class LoginContainer extends StatelessWidget {
  LoginContainer({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Padding(
          padding: EdgeInsets.fromLTRB(50.0, 20.0, 50.0, 20.0),
          child: TextField(
            autofocus: true,
            decoration: InputDecoration(
              labelText: 'Username',
              labelStyle: TextStyle(
                color: Colors.blue, // Change the color of the label text
                fontSize: 16.0, // Change the size of the label text
              ),
              hintText: 'Enter your username',
              hintStyle: TextStyle(
                color: Colors.grey, // Change the color of the hint text
                fontSize: 14.0, // Change the size of the hint text
              ),
              enabledBorder: OutlineInputBorder(
                borderSide: BorderSide(
                  color: Colors.blue, // Change the color of the enabled border
                  width: 2.0, // Change the width of the enabled border
                ),
                borderRadius: BorderRadius.circular(8.0), // Rounded corners
              ),
              focusedBorder: OutlineInputBorder(
                borderSide: BorderSide(
                  color: Colors.green, // Change the color of the focused border
                  width: 2.0, // Change the width of the focused border
                ),
                borderRadius: BorderRadius.circular(8.0), // Rounded corners
              ),
              prefixIcon: Icon(Icons.person,
                  color: Colors.blue), // Add an icon before the text
              suffixIcon: Icon(Icons.check,
                  color: Colors.green), // Add an icon after the text
              filled: true, // Enable background fill
              fillColor: Colors.lightBlue[50], // Set background fill color
              contentPadding: EdgeInsets.symmetric(
                  vertical: 15.0,
                  horizontal: 10.0), // Adjust the content padding
            ),
          ),
        ),
        SizedBox(
          height: 10.0,
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(50.0, 20.0, 50.0, 20.0),
          child: TextField(
            obscureText:
                true, // Ensures the text is obscured for password input
            decoration: InputDecoration(
              labelText: 'Password',
              labelStyle: TextStyle(
                color: Colors.blue, // Change the color of the label text
                fontSize: 16.0, // Change the size of the label text
              ),
              hintText: 'Enter your password',
              hintStyle: TextStyle(
                color: Colors.grey, // Change the color of the hint text
                fontSize: 14.0, // Change the size of the hint text
              ),
              enabledBorder: OutlineInputBorder(
                borderSide: BorderSide(
                  color: Colors.blue, // Change the color of the enabled border
                  width: 2.0, // Change the width of the enabled border
                ),
                borderRadius: BorderRadius.circular(8.0), // Rounded corners
              ),
              focusedBorder: OutlineInputBorder(
                borderSide: BorderSide(
                  color: Colors.green, // Change the color of the focused border
                  width: 2.0, // Change the width of the focused border
                ),
                borderRadius: BorderRadius.circular(8.0), // Rounded corners
              ),
              prefixIcon: Icon(Icons.lock,
                  color: Colors.blue), // Add an icon before the text
              suffixIcon: Icon(Icons.visibility_off,
                  color: Colors.grey), // Add an icon after the text
              filled: true, // Enable background fill
              fillColor: Colors.lightBlue[50], // Set background fill color
              contentPadding: EdgeInsets.symmetric(
                  vertical: 15.0,
                  horizontal: 10.0), // Adjust the content padding
            ),
          ),
        ),
        SizedBox(
          height: 10.0,
        ),
        ElevatedButton(
          onPressed: () {
            // Your login logic here
          },
          child: Text(
            'Login',
            style: TextStyle(
              color: Colors.white, // Text color
              fontSize: 16.0, // Font size
            ),
          ),
          style: ElevatedButton.styleFrom(
            // primary: Colors.blue, // Background color
            // onPrimary: Colors.white, // Splash color
            padding: EdgeInsets.symmetric(
                horizontal: 32.0, vertical: 12.0), // Padding
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8.0), // Rounded corners
            ),
            elevation: 5, // Elevation
          ),
        ),
      ],
    );
  }
}
