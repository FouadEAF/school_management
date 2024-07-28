import 'package:flutter/material.dart';
import 'package:mobile/authentication/widgets/registre_form.dart';
import 'package:mobile/widgets/app_bar.dart';

class RegisterPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // appBar: AppBar(        title: const Text('Register'),      ),
      appBar: MyAppBar(
        title: 'Registre',
        leading: IconButton(
          icon: const Icon(
            Icons.arrow_back,
            color: Colors.white,
          ),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        actions: null,
      ),
      body: Center(
        child: RegistreForm(),
      ),
    );
  }
}
