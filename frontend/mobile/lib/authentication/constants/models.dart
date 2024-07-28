class UserModel {
  String username;
  String firstName;
  String lastName;
  String cnie;
  String email;
  String password1;
  String password2;
  String role;

  UserModel({
    required this.username,
    required this.firstName,
    required this.lastName,
    required this.cnie,
    required this.email,
    required this.password1,
    required this.password2,
    required this.role,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      username: json['username'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      cnie: json['cnie'],
      email: json['email'],
      password1: json['password1'],
      password2: json['password2'],
      role: json['role'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'username': username,
      'first_name': firstName,
      'last_name': lastName,
      'cnie': cnie,
      'email': email,
      'password1': password1,
      'password2': password2,
      'role': role,
    };
  }
}

class Login {
  String username;
  String password;

  Login({
    required this.username,
    required this.password,
  });

  // Factory constructor to create a Login instance from a JSON map
  factory Login.fromJson(Map<String, dynamic> json) {
    return Login(
      username: json['username'],
      password: json['password'],
    );
  }

  // Method to convert a Login instance to a JSON map
  Map<String, dynamic> toJson() {
    return {
      'username': username,
      'password': password,
    };
  }
}
