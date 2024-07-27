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
            decoration: const InputDecoration(
              label: Text('Username'),
            ),
          ),
        ),
        SizedBox(
          height: 10.0,
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(50.0, 20.0, 50.0, 20.0),
          child: TextField(
            decoration: const InputDecoration(
              label: Text('Password'),
            ),
          ),
        ),
        SizedBox(
          height: 10.0,
        ),
        ElevatedButton(onPressed: null, child: Text('Login')),
      ],
    );
  }
}
