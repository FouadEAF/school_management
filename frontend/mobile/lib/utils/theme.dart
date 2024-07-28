// ignore_for_file: non_constant_identifier_names

import 'package:flutter/material.dart';

//baisc color Color(0xff53b0ea)

//===Define the light theme======================================================
final ThemeData LightTheme = ThemeData(
//===brightness=================================================================
  brightness: Brightness.light,

//===scaffoldBackgroundColor====================================================
  scaffoldBackgroundColor: const Color(0xffe2f0fc),

//===drawerTheme================================================================
  drawerTheme: const DrawerThemeData(
      width: 300.0,
      backgroundColor: Color(0xffbfe0f8),
      elevation: 0.7,
      shadowColor: Color(0xff144266)),

//===primaryColor===============================================================
  primaryColor: const Color(0xff53b0ea),

//===appBarTheme================================================================
  appBarTheme: const AppBarTheme(
    backgroundColor: Color(0xffbfe0f8),
    iconTheme: IconThemeData(color: Color(0xff0d2a44)),
    titleTextStyle: TextStyle(
        color: Color(0xff0d2a44), fontSize: 20, fontWeight: FontWeight.bold),
    centerTitle: true,
  ),

//===elevatedButtonTheme========================================================
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ButtonStyle(
      foregroundColor: WidgetStateProperty.all<Color>(Colors.white),
      backgroundColor: WidgetStateProperty.resolveWith<Color>(
        (Set<WidgetState> states) {
          if (states.contains(WidgetState.pressed)) {
            // Background color when button is pressed
            return const Color(0xff105b94);
          } else if (states.contains(WidgetState.hovered)) {
            // Background color when button is hovered
            return const Color(0xff1272b7);
          } else if (states.contains(WidgetState.disabled)) {
            // Background color when button is disabled
            return const Color(0xffe2f0fc);
          }
          // Default background color
          return const Color(0xff2090d7);
        },
      ),
      minimumSize: WidgetStateProperty.all<Size>(const Size(150, 50)),
      padding: WidgetStateProperty.all<EdgeInsets>(
        const EdgeInsets.symmetric(horizontal: 16),
      ),
      textStyle: WidgetStateProperty.all<TextStyle>(
        const TextStyle(
          color: Colors.white,
          fontSize: 20.0,
          fontWeight: FontWeight.bold,
        ),
      ),
      shape: WidgetStateProperty.all<RoundedRectangleBorder>(
        RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    ),
  ),

//===TextField==================================================================
  inputDecorationTheme: InputDecorationTheme(
    labelStyle: const TextStyle(
      color: Colors.blue, // Change the color of the label text
      fontSize: 16.0, // Change the size of the label text
    ),
    hintStyle: const TextStyle(
      color: Colors.grey, // Change the color of the hint text
      fontSize: 14.0, // Change the size of the hint text
    ),
    enabledBorder: OutlineInputBorder(
      borderSide: const BorderSide(
        color: Colors.blue, // Change the color of the enabled border
        width: 2.0, // Change the width of the enabled border
      ),
      borderRadius: BorderRadius.circular(8.0), // Rounded corners
    ),
    focusedBorder: OutlineInputBorder(
      borderSide: const BorderSide(
        color: Colors.green, // Change the color of the focused border
        width: 2.0, // Change the width of the focused border
      ),
      borderRadius: BorderRadius.circular(8.0), // Rounded corners
    ),
    errorBorder: OutlineInputBorder(
      borderSide: const BorderSide(
        color: Colors.red, // Change the color of the error border
        width: 2.0, // Change the width of the error border
      ),
      borderRadius: BorderRadius.circular(8.0), // Rounded corners
    ),
    focusedErrorBorder: OutlineInputBorder(
      borderSide: const BorderSide(
        color: Colors.redAccent, // Change the color of the focused error border
        width: 2.0, // Change the width of the focused error border
      ),
      borderRadius: BorderRadius.circular(8.0), // Rounded corners
    ),
    prefixIconColor: Colors.blue, // Change the color of the prefix icon
    suffixIconColor: Colors.grey, // Change the color of the suffix icon
    filled: true, // Enable background fill
    fillColor: Colors.lightBlue[50], // Set background fill color
    contentPadding: const EdgeInsets.symmetric(
      vertical: 15.0,
      horizontal: 10.0,
    ), // Adjust the content padding
  ),

//===Text=======================================================================
  textTheme: const TextTheme(
    displayLarge: TextStyle(
      color: Colors.black,
      fontSize: 32,
      fontWeight: FontWeight.bold,
    ),
    headlineMedium: TextStyle(
      color: Colors.black,
      fontSize: 20,
      fontWeight: FontWeight.bold,
    ),
    bodyLarge: TextStyle(
      color: Colors.black,
      fontSize: 16,
    ),
    bodyMedium: TextStyle(
      color: Colors.black,
      fontSize: 14,
    ),
  ),

//===dialogTheme================================================================
  dialogTheme: DialogTheme(
    backgroundColor: const Color(0xffbfe0f8),
    shape: RoundedRectangleBorder(
      side: const BorderSide(color: const Color(0xff0d2a44)),
      borderRadius: BorderRadius.circular(15),
    ),
    titleTextStyle: const TextStyle(
      color: Color(0xff0d2a44),
      fontSize: 20,
      fontWeight: FontWeight.bold,
    ),
    contentTextStyle: const TextStyle(
      color: Colors.black,
      fontSize: 16,
    ),
  ),
);

//===Define the dark theme======================================================
final ThemeData DarkTheme = ThemeData(
  // Brightness
  brightness: Brightness.dark,

  // Scaffold background color
  scaffoldBackgroundColor: const Color(0xff0d2a44), //Color(0xff121212)

  // Drawer theme
  drawerTheme: DrawerThemeData(
    width: 300.0,
    backgroundColor: const Color(0xff1e1e1e),
    elevation: 0.7,
    shadowColor: Colors.lightBlue[50],
  ),

  // Primary color
  primaryColor: Colors.lightBlue[50],

  // AppBar theme
  appBarTheme: AppBarTheme(
    backgroundColor: const Color(0xff1e1e1e),
    iconTheme: IconThemeData(color: Colors.lightBlue[50]),
    titleTextStyle: TextStyle(
      color: Colors.lightBlue[50],
      fontSize: 20,
      fontWeight: FontWeight.bold,
    ),
    centerTitle: true,
  ),

  // ElevatedButton theme
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ButtonStyle(
      foregroundColor: WidgetStateProperty.all<Color>(Colors.black),
      backgroundColor: WidgetStateProperty.resolveWith<Color>(
        (Set<WidgetState> states) {
          if (states.contains(WidgetState.pressed)) {
            // Background color when button is pressed
            return const Color(0xff1272b7);
          } else if (states.contains(WidgetState.hovered)) {
            // Background color when button is hovered
            return const Color(0xff1272b7);
          } else if (states.contains(WidgetState.disabled)) {
            // Background color when button is disabled
            return const Color(0xff0d2a44);
          }
          // Default background color
          return const Color(0xff2090d7);
        },
      ),
      minimumSize: WidgetStateProperty.all<Size>(const Size(150, 50)),
      padding: WidgetStateProperty.all<EdgeInsets>(
        const EdgeInsets.symmetric(horizontal: 16),
      ),
      textStyle: WidgetStateProperty.all<TextStyle>(
        const TextStyle(
          color: Colors.white, // Change text color to white
          fontSize: 20.0,
          fontWeight: FontWeight.bold,
        ),
      ),
      shape: WidgetStateProperty.all<RoundedRectangleBorder>(
        RoundedRectangleBorder(
          side: const BorderSide(color: Color(0xff2090d7)),
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    ),
  ),

  // TextField
  inputDecorationTheme: InputDecorationTheme(
    labelStyle: const TextStyle(
      color: Colors.white, // Change the color of the label text
      fontSize: 16.0, // Change the size of the label text
    ),
    hintStyle: const TextStyle(
      color: Colors.grey, // Change the color of the hint text
      fontSize: 14.0, // Change the size of the hint text
    ),
    enabledBorder: OutlineInputBorder(
      borderSide: const BorderSide(
        color: Colors.blue, // Change the color of the enabled border
        width: 2.0, // Change the width of the enabled border
      ),
      borderRadius: BorderRadius.circular(8.0), // Rounded corners
    ),
    focusedBorder: OutlineInputBorder(
      borderSide: const BorderSide(
        color: Colors.green, // Change the color of the focused border
        width: 2.0, // Change the width of the focused border
      ),
      borderRadius: BorderRadius.circular(8.0), // Rounded corners
    ),
    errorBorder: OutlineInputBorder(
      borderSide: const BorderSide(
        color: Colors.red, // Change the color of the error border
        width: 2.0, // Change the width of the error border
      ),
      borderRadius: BorderRadius.circular(8.0), // Rounded corners
    ),
    focusedErrorBorder: OutlineInputBorder(
      borderSide: const BorderSide(
        color: Colors.redAccent, // Change the color of the focused error border
        width: 2.0, // Change the width of the focused error border
      ),
      borderRadius: BorderRadius.circular(8.0), // Rounded corners
    ),
    prefixIconColor: Colors.blue, // Change the color of the prefix icon
    suffixIconColor: Colors.grey, // Change the color of the suffix icon
    filled: true, // Enable background fill
    fillColor: Colors.black45, // Set background fill color
    contentPadding: const EdgeInsets.symmetric(
      vertical: 15.0,
      horizontal: 10.0,
    ), // Adjust the content padding
  ),

  // Text
  textTheme: const TextTheme(
    displayLarge: TextStyle(
      color: Colors.white,
      fontSize: 32,
      fontWeight: FontWeight.bold,
    ),
    headlineMedium: TextStyle(
      color: Colors.white,
      fontSize: 20,
      fontWeight: FontWeight.bold,
    ),
    bodyLarge: TextStyle(
      color: Colors.white,
      fontSize: 16,
    ),
    bodyMedium: TextStyle(
      color: Colors.white,
      fontSize: 14,
    ),
  ),

  // Dialog theme
  dialogTheme: DialogTheme(
    backgroundColor: const Color(0xff1e1e1e),
    shape: RoundedRectangleBorder(
      side: const BorderSide(color: Color(0xff2090d7)),
      borderRadius: BorderRadius.circular(15),
    ),
    titleTextStyle: TextStyle(
      color: Colors.lightBlue[50],
      fontSize: 20,
      fontWeight: FontWeight.bold,
    ),
    contentTextStyle: const TextStyle(
      color: Colors.white,
      fontSize: 16,
    ),
  ),
);
