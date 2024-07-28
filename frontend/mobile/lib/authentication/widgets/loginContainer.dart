// ignore_for_file: file_names, prefer_const_constructors, prefer_const_literals_to_create_immutables, sort_child_properties_last

import 'package:flutter/material.dart';
import 'package:mobile/authentication/constants/methods.dart';

class LoginContainer extends StatelessWidget {
  LoginContainer({super.key});

  final TextEditingController txtUsername = TextEditingController();
  final TextEditingController txtPassword = TextEditingController();

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
              controller: txtUsername,
              decoration: InputDecoration(
                labelText: 'Username or email',
                hintText: 'Enter your username or email',
                prefixIcon: Icon(
                  Icons.person,
                ),
              )),
        ),
        SizedBox(
          height: 10.0,
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(50.0, 20.0, 50.0, 20.0),
          child: TextField(
              controller: txtPassword,
              obscureText: true,
              decoration: InputDecoration(
                labelText: 'Password',
                hintText: 'Enter your password',
                prefixIcon: Icon(
                  Icons.lock,
                ),
              )),
        ),
        SizedBox(
          height: 10.0,
        ),
        ElevatedButton(
          onPressed: () {
            LoginHelper.postData(
              username: txtUsername.text,
              password: txtPassword.text,
            );
          },
          child: Text(
            'Login',
          ),
        ),
      ],
    );
  }
}
