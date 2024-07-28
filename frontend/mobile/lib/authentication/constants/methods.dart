// ignore_for_file: non_constant_identifier_names

import 'package:flutter/material.dart';
import 'package:mobile/utils/api.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:mobile/widgets/box_dialogue.dart';

class LoginHelper {
  static Future<void> postData({
    required BuildContext context,
    required String username,
    required String password,
  }) async {
    // Function to post data to backend
    try {
      http.Response res = await http.post(
        Uri.parse('$api/auth/login/'),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, dynamic>{
          "username": username,
          "password": password,
        }),
      );

      if (res.statusCode == 200) {
        // Decode the JSON response
        var data = jsonDecode(res.body);

        print('Response data: $data');

        // For example, you can extract specific fields:
        var user = data['user'];
        print('User: $user');
      } else {
        print("Failed to post data: ${res.statusCode}");
        // Optionally, decode the error response
        var data = jsonDecode(res.body);
        showNotification(context, 'Error', data['message']);
        print('Error response data: ${data['message']}');
      }
    } catch (e) {
      print("Error: $e");
      showNotification(context, 'Exception', e.toString());
    }
  }
}

// class HelperFunction {
//   Future<void> postData({String title = "", String desc = ""}) async {
//     // Function to post data to backend
//     try {
//       http.Response res = await http.post(
//         Uri.parse(api),
//         headers: <String, String>{
//           'Content-Type': 'application/json; charset=UTF-8',
//         },
//         body: jsonEncode(<String, dynamic>{
//           "title": title,
//           "desc": desc,
//           "isDone": false,
//         }),
//       );
//       if (res.statusCode == 201) {
//         await fetchData();
//       } else {
//         print("Failed to post data: ${res.statusCode}");
//       }
//     } catch (e) {
//       print("Error: $e");
//     }
//   }

//   Future<List> fetchData() async {
//     // Function to get data from backend
//     List myTodos = [];
//     try {
//       http.Response response = await http.get(Uri.parse(api));
//       if (response.statusCode == 200) {
//         var data = json.decode(response.body);
//         data.forEach((todo) {
//           myTodos.add(todo);
//         });
//       } else {
//         print("Failed to fetch data: ${response.statusCode}");
//       }
//     } catch (e) {
//       print("Error: $e");
//     }
//     return myTodos;
//   }

//   Future<void> putData(BuildContext context, String idRecord, Widget pageName,
//       {String title = "", String desc = ""}) async {
//     try {
//       final response = await http.put(
//         Uri.parse("$api/$idRecord"),
//         headers: <String, String>{
//           'Content-Type': 'application/json; charset=UTF-8',
//         },
//         body: jsonEncode(<String, dynamic>{
//           "title": title,
//           "desc": desc,
//           "isDone": false,
//         }),
//       );

//       if (response.statusCode == 200 || response.statusCode == 201) {
//         Navigator.pop(context); // Close the modal
//       } else {
//         print("Failed to update data: ${response.statusCode}");
//       }
//     } catch (e) {
//       print("Error: $e");
//     }
//   }

//   Future<void> delete_todo(String idRecord) async {
//     // Function to delete a record from backend
//     try {
//       http.Response response = await http.delete(Uri.parse("$api/$idRecord"));
//       if (response.statusCode == 200) {
//         await fetchData();
//       } else {
//         print("Failed to delete data: ${response.statusCode}");
//       }
//     } catch (e) {
//       print("Error: $e");
//     }
//   }
// }
