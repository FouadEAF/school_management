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
                Text(
                  'Input your Email to reset your account',
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
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
                SizedBox(height: 20.0),
                ElevatedButton(
                  onPressed: () {
                    if (_formKey.currentState!.validate()) {
                      // Add registration logic here
                      print('==========Send the code============');
                      Navigator.pushNamed(
                        context,
                        '/resetPasswordConfirm', // Replace with your named route
                        // (Route<dynamic> route) =>
                        //     false, // This removes all the previous routes
                      );
                    }
                  },
                  child: const Text('Next'),
                ),
              ],
            ),
          ),
        ));
  }
}

//==============================================================================

class ResetPasswordConfirmPage extends StatelessWidget {
  ResetPasswordConfirmPage({super.key});
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _txtEmail = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _confirmPasswordController =
      TextEditingController();
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
                const Text('Code activation is sent to your email, check it'),
                Padding(
                  padding: EdgeInsets.fromLTRB(50.0, 20.0, 50.0, 20.0),
                  child: TextFormField(
                    controller: _txtEmail,
                    decoration: const InputDecoration(
                      labelText: 'Code activation',
                      hintText: 'Enter your code activation',
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter your code activation';
                      }

                      return null;
                    },
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(50.0, 20.0, 50.0, 20.0),
                  child: TextFormField(
                    controller: _passwordController,
                    decoration: InputDecoration(
                      labelText: 'Password',
                    ),
                    obscureText: true,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter your password';
                      }
                      return null;
                    },
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(50.0, 20.0, 50.0, 20.0),
                  child: TextFormField(
                    controller: _confirmPasswordController,
                    decoration: InputDecoration(
                      labelText: 'Confirm Password',
                    ),
                    obscureText: true,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please confirm your password';
                      }
                      if (value != _passwordController.text) {
                        return 'Passwords do not match';
                      }
                      return null;
                    },
                  ),
                ),
                SizedBox(height: 20.0),
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
