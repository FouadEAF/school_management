import 'package:flutter/material.dart';
import 'package:mobile/authentication/pages/login.dart';
import 'package:mobile/authentication/pages/registre.dart';
import 'package:mobile/utils/theme.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  ThemeMode _themeMode = ThemeMode.system;

  @override
  void initState() {
    super.initState();
    _loadThemeMode();
  }

  Future<void> _loadThemeMode() async {
    final prefs = await SharedPreferences.getInstance();
    final themeModeString = prefs.getString('themeMode');
    if (themeModeString != null) {
      setState(() {
        _themeMode = ThemeMode.values.firstWhere(
          (mode) => mode.toString() == themeModeString,
        );
      });
    }
  }

  Future<void> _saveThemeMode(ThemeMode themeMode) async {
    final prefs = await SharedPreferences.getInstance();
    prefs.setString('themeMode', themeMode.toString());
  }

  void _toggleThemeMode() {
    setState(() {
      _themeMode =
          _themeMode == ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
      _saveThemeMode(_themeMode);
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: true,
      title: 'School Management',
      theme: LightTheme,
      darkTheme: DarkTheme,
      themeMode: _themeMode,
      home: LoginPage(), //(onThemeToggle: _toggleThemeMode),
      routes: {
        '/register': (context) => RegisterPage(),
      },
    );
  }
}


// import 'package:flutter/material.dart';
// import 'package:mobile/authentication/pages/login.dart';
// import 'package:mobile/utils/theme.dart';
// import 'package:shared_preferences/shared_preferences.dart';

// void main() {
//   runApp(const MyApp());
// }

// bool isDark = true;

// class MyApp extends StatelessWidget {
//   const MyApp({super.key});

//   // This widget is the root of your application.
//   @override
//   Widget build(BuildContext context) {
//     bool isDark =
//         true; // Or determine this value based on user preference or system settings

//     return MaterialApp(
//       debugShowCheckedModeBanner: true,
//       title: 'School Management',
//       theme: isDark ? DarkMode() : LightMode(),
//       home: LoginPage(),
//       routes: {
//         // '/register': (context) => RegisterPage(),
//       },
//     );
//   }
// }
