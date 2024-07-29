import 'package:flutter/material.dart';

// void showNotification(String title, String body) {
//   showDialog(
//     builder: (BuildContext context) {
//       return AlertDialog(
//         title: Text(title),
//         content: Text(body),
//         actions: <Widget>[
//           TextButton(
//             child: const Text('OK'),
//             onPressed: () {
//               Navigator.of(context).pop(); // Close the dialog
//             },
//           ),
//         ],
//       );
//     },
//   );
// }

final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

void showNotification(String title, String body) {
  navigatorKey.currentState!.push(
    MaterialPageRoute(
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text(title),
          content: Text(body),
          actions: <Widget>[
            TextButton(
              child: const Text('OK'),
              onPressed: () {
                Navigator.of(context).pop(); // Close the dialog
              },
            ),
          ],
        );
      },
    ),
  );
}
