// ignore_for_file: prefer_const_constructors

// import 'package:flutter/material.dart';
// import 'package:mobile/constants/colors.dart';

// AppBar customAppBar() {
//   return AppBar(
//     title: const Text(
//       'Django Todos',
//       style: TextStyle(color: Color(0xFFffffff)),
//     ),
//     elevation: 0.0,
//     backgroundColor: darkBlue,
//   );
// }

import 'package:flutter/material.dart';

class MyAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  final Widget? leading;
  final List<Widget>? actions;

  MyAppBar({
    required this.title,
    this.leading,
    this.actions,
  });

  @override
  Widget build(BuildContext context) {
    return PreferredSize(
      preferredSize: Size.fromHeight(60.0),
      child: Container(
        color: Colors.blue,
        child: SafeArea(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  leading ?? SizedBox.shrink(),
                  Text(
                    title,
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 20.0,
                    ),
                  ),
                  Row(
                    children: actions ?? [],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(60.0);
}
