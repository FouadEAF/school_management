// ignore_for_file: prefer_const_constructors

import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:mobile/authentication/widgets/loginContainer.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          LoginContainer(),
          const Padding(padding: EdgeInsets.only(top: 50.0)),
          RichText(
            text: TextSpan(
              text: 'Password forget? ',
              style: TextStyle(color: Colors.black),
              children: <TextSpan>[
                TextSpan(
                  text: 'Reset',
                  style: TextStyle(
                      color: Colors.blue, decoration: TextDecoration.underline),
                  recognizer: TapGestureRecognizer()
                    ..onTap = () {
                      Navigator.pushNamed(context, '/resetPassword');
                    },
                ),
              ],
            ),
          ),
          const Padding(padding: EdgeInsets.only(top: 30.0)),
          RichText(
            text: TextSpan(
              text: 'You don\'t have an account? ',
              style: TextStyle(color: Colors.black),
              children: <TextSpan>[
                TextSpan(
                  text: 'Click here',
                  style: TextStyle(
                      color: Colors.blue, decoration: TextDecoration.underline),
                  recognizer: TapGestureRecognizer()
                    ..onTap = () {
                      Navigator.pushNamed(context, '/register');
                    },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
