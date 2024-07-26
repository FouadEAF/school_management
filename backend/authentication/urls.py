from django.urls import path
# , PasswordReset
from .views import CreateUser, UpdateUser, LoginView, LogoutView, AboutMeView, ChangePasswordView, RefreshToken, RequestPasswordReset, PasswordResetConfirm
# from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# from django.contrib.auth import views as auth_views


urlpatterns = [
    path('registre/', CreateUser.as_view(), name='create_user'),
    path('update/', UpdateUser.as_view(), name='update_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('me/', AboutMeView.as_view(), name='about_me'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('refresh/', RefreshToken.as_view(), name='refresh_token'),
    path('password-reset/', RequestPasswordReset.as_view(), name='password_reset'),
    path('password-reset-confirm/',
         PasswordResetConfirm.as_view(), name='password_reset'),



    # path('password-reset/', auth_views.PasswordResetView.as_view(),
    #      name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
    #      name='password_reset_complete'),

    # path('password-reset/', PasswordResetView.as_view(
    #     template_name='users/password_reset.html',
    #     html_email_template_name='users/password_reset_email.html'
    # ), name='password-reset'),
    # path('password_reset/done/', PasswordResetDoneView.as_view(
    #     template_name='users/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
    #     template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    # path('reset/done/', PasswordResetCompleteView.as_view(
    #     template_name='users/password_reset_complete.html'), name='password_reset_complete'),

]
