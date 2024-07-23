from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'api'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.LoginView.as_view(), name='login'),
    path('me/', views.AboutMeView.as_view(), name='aboutme'),
    path('signout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', views.refresh_token, name='refresh_token'),
    # path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change_password'),
    path('password-reset/', views.PasswordResetRequestView.as_view(),
         name='password_reset'),
    path('password-reset-confirm/',
         views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
