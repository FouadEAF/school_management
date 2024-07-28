// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';

class ResetPasswordPage extends StatelessWidget {
  ResetPasswordPage({super.key});
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _txtEmail = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text('Reset password'),
        ),
        body: Center(
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const Text('Input your Email to reset your account'),
                Padding(
                  padding: EdgeInsets.fromLTRB(50.0, 20.0, 50.0, 20.0),
                  child: TextFormField(
                    controller: _txtEmail,
                    decoration: const InputDecoration(
                      labelText: 'Email',
                      hintText: 'Enter your email',
                      prefixIcon: Icon(
                        Icons.email,
                      ),
                    ),
                    keyboardType: TextInputType.emailAddress,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter your email';
                      }
                      if (!RegExp(r'^[^@]+@[^@]+\.[^@]+').hasMatch(value)) {
                        return 'Please enter a valid email address';
                      }
                      return null;
                    },
                  ),
                ),
                ElevatedButton(
                  onPressed: () {
                    if (_formKey.currentState!.validate()) {
                      // Add registration logic here
                      print('==========Reset============');
                      print(_txtEmail.text);
                    }
                  },
                  child: const Text('Reset'),
                ),
              ],
            ),
          ),
        ));
  }
}
