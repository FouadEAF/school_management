from django.urls import path
from .views import CreateUser, UpdateUser, LoginView, LogoutView, AboutMeView, ChangePasswordView, RefreshToken, PasswordReset

urlpatterns = [
    path('registre/', CreateUser.as_view(), name='create_user'),
    path('update/', UpdateUser.as_view(), name='update_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('me/', AboutMeView.as_view(), name='about_me'),
    path('refresh/', RefreshToken.as_view(), name='refresh_token'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', PasswordReset.as_view(), name='reset_password'),
]
