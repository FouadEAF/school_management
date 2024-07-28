// import 'package:flutter/material.dart';
// import 'package:toggle_switch/toggle_switch.dart';
// import 'package:font_awesome_flutter/font_awesome_flutter.dart';
// import 'package:shared_preferences/shared_preferences.dart';
// import 'package:mobile/utils/theme.dart';

// void main() {
//   runApp(MyApp());
// }

// class MyApp extends StatefulWidget {
//   @override
//   _MyAppState createState() => _MyAppState();
// }

// class _MyAppState extends State<MyApp> {
//   ThemeMode _themeMode = ThemeMode.system;

//   @override
//   void initState() {
//     super.initState();
//     _loadThemeMode();
//   }

//   Future<void> _loadThemeMode() async {
//     final prefs = await SharedPreferences.getInstance();
//     final themeModeString = prefs.getString('themeMode');
//     if (themeModeString != null) {
//       setState(() {
//         _themeMode = ThemeMode.values.firstWhere(
//           (mode) => mode.toString() == themeModeString,
//         );
//       });
//     }
//   }

//   Future<void> _saveThemeMode(ThemeMode themeMode) async {
//     final prefs = await SharedPreferences.getInstance();
//     prefs.setString('themeMode', themeMode.toString());
//   }

//   void _toggleThemeMode(int index) {
//     setState(() {
//       _themeMode = index == 0 ? ThemeMode.light : ThemeMode.dark;
//       _saveThemeMode(_themeMode);
//     });
//   }

//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       debugShowCheckedModeBanner: false,
//       title: 'Theme Switcher',
//       theme: LightTheme,
//       darkTheme: DarkTheme,
//       themeMode: _themeMode,
//       home: HomePage(onThemeToggle: _toggleThemeMode),
//     );
//   }
// }

// class HomePage extends StatelessWidget {
//   final ValueChanged<int> onThemeToggle;
//   HomePage({required this.onThemeToggle});

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         title: Text('Theme Switcher'),
//       ),
//       body: Center(
//         child: Column(
//           mainAxisAlignment: MainAxisAlignment.center,
//           children: [
//             ToggleSwitch(
//               minWidth: 90.0,
//               minHeight: 70.0,
//               initialLabelIndex:
//                   Theme.of(context).brightness == Brightness.dark ? 1 : 0,
//               cornerRadius: 20.0,
//               activeFgColor: Colors.white,
//               inactiveBgColor: Colors.grey,
//               inactiveFgColor: Colors.white,
//               totalSwitches: 2,
//               icons: [
//                 FontAwesomeIcons.lightbulb,
//                 FontAwesomeIcons.solidLightbulb,
//               ],
//               iconSize: 30.0,
//               activeBgColors: [
//                 [Colors.black45, Colors.black26],
//                 [Colors.yellow, Colors.orange]
//               ],
//               animate:
//                   true, // with just animate set to true, default curve = Curves.easeIn
//               curve: Curves
//                   .bounceInOut, // animate must be set to true when using custom curve
//               onToggle: onThemeToggle,
//             ),
//           ],
//         ),
//       ),
//     );
//   }
// }
