// ignore_for_file: non_constant_identifier_names

class CreateUser {
  String username;
  String firstName;
  String lastName;
  String cnie;
  String email;
  String password1;
  String password2;
  String role;
  bool is_superuser;
  bool is_active;
  bool is_staff;

  CreateUser({
    required this.username,
    required this.firstName,
    required this.lastName,
    required this.cnie,
    required this.email,
    required this.password1,
    required this.password2,
    required this.role,
    this.is_superuser = false,
    this.is_active = true,
    this.is_staff = false,
  });

  factory CreateUser.fromJson(Map<String, dynamic> json) {
    return CreateUser(
      username: json['username'] ?? '',
      firstName: json['first_name'] ?? '',
      lastName: json['last_name'] ?? '',
      cnie: json['cnie'] ?? '',
      email: json['email'] ?? '',
      password1: json['password1'] ?? '',
      password2: json['password2'] ?? '',
      role: json['role'] ?? '',
      is_superuser: json['is_superuser'] ?? false,
      is_active: json['is_active'] ?? true,
      is_staff: json['is_staff'] ?? false,
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
      'is_superuser': is_superuser,
      'is_active': is_active,
      'is_staff': is_staff,
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

  factory Login.fromJson(Map<String, dynamic> json) {
    return Login(
      username: json['username'] ?? '',
      password: json['password'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'username': username,
      'password': password,
    };
  }
}

class ResetPassword {
  String email;

  ResetPassword({required this.email});

  factory ResetPassword.fromJson(Map<String, dynamic> json) {
    return ResetPassword(
      email: json['email'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'email': email,
    };
  }
}

class ResetPasswordConfirm {
  String resetCode;
  String newPassword;
  String confirmPassword;

  ResetPasswordConfirm({
    required this.resetCode,
    required this.newPassword,
    required this.confirmPassword,
  });

  factory ResetPasswordConfirm.fromJson(Map<String, dynamic> json) {
    return ResetPasswordConfirm(
      resetCode: json['reset_code'] ?? '',
      newPassword: json['new_password'] ?? '',
      confirmPassword: json['confirm_password'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'reset_code': resetCode,
      'new_password': newPassword,
      'confirm_password': confirmPassword,
    };
  }
}
