// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:mobile/authentication/widgets/registre_form.dart';

class RegisterPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Register'),
      ),
      body: Center(
        child: RegistreForm(),
      ),
    );
  }
}
