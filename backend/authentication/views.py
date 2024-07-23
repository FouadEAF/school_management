from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
# from django.http import Response
from rest_framework.response import Response
from authentication.utils import get_tokens_for_user
from users.forms import SignUpForm, UserUpdateForm
import json
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from users.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


@method_decorator(csrf_exempt, name='dispatch')
class CreateUser(APIView):
    """ Create new user """
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON'}, status=400)

        form = SignUpForm(data)
        if form.is_valid():
            user = form.save()
            # user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.backend = 'users.authentication.UserBackend'
            auth_login(request, user)
            return Response({'success': True, 'message': 'User created and logged in successfully'})
        else:
            return Response({'success': False, 'message': form.errors}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateUser(APIView):
    """ Update information of user """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User not found'}, status=404)

        form = UserUpdateForm(data, instance=user)
        if form.is_valid():
            updated_user = form.save()
            return Response({'success': True, 'message': 'User updated successfully'})
        else:
            return Response({'success': False, 'message': form.errors}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """ Login to server Backend """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON data'}, status=400)

        if not username or not password:
            return Response({'success': False, 'message': 'Username and password are required.'}, status=400)

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            auth_login(request, user)

            # Generate tokens
            tokens = get_tokens_for_user(user)

            # Define the expiration time for refresh and access tokens
            refresh_token_lifetime = datetime.now() + timedelta(days=1)
            access_token_lifetime = datetime.now() + timedelta(minutes=60)

            # Serialize user data
            response_data = {
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'matricule': user.matricule,
                    'departement': user.departement
                },
                'refresh_token': tokens['refresh'],
                'access_token': tokens['access']
            }

            response = Response(response_data, status=200)

            # Set cookies for tokens
            response.set_cookie(
                key='refresh_token',
                value=tokens['refresh'],
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=datetime.now() + timedelta(days=1)
            )

            response.set_cookie(
                key='access_token',
                value=tokens['access'],
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=datetime.now() + timedelta(minutes=60)
            )

            # Set CORS headers
            response["Access-Control-Allow-Origin"] = "http://localhost:8000"
            response["Access-Control-Allow-Credentials"] = "true"

            return response
        else:
            return Response({'success': False, 'message': 'Invalid credentials'}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    """ Logout from the server backend """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logout(request)

            response = Response(
                {'success': True, 'message': 'Logout successful'}, status=200)

            response.delete_cookie('refresh_token')
            response.delete_cookie('access_token')
            response.delete_cookie('csrftoken')
            response.delete_cookie('sessionid')

            return response

        else:
            return Response({'success': False, 'message': 'Authentication Required'}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class AboutMeView(APIView):
    """About me - get all information about user"""
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'success': False, 'message': 'User is not authenticated'}, status=401)

        user = request.user
        user_data = {
            'idUser': user.id,
            'username': user.username,
            'matricule': user.matricule,
            'section': user.groups.first().name if user.groups.exists() else user.departement,
        }
        return Response({'success': True, 'user': user_data}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ChangePasswordView(APIView):
    """ Change the password of connected user """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            new_password_confirm = data.get('new_password_confirm')
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON'}, status=400)

        user = request.user

        if not current_password or not new_password or not new_password_confirm:
            return Response({'success': False, 'message': 'All fields are required'}, status=400)

        if not check_password(current_password, user.password):
            return Response({'success': False, 'message': 'Current password is incorrect'}, status=400)

        if new_password != new_password_confirm:
            return Response({'success': False, 'message': 'New passwords do not match'}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({'success': True, 'message': 'Password changed successfully'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class RefreshToken(APIView):
    """ Refresh token """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh_token', None)

        if refresh is None:
            return Response({'success': False, 'message': "Refresh token is required"}, status=400)

        try:
            print('refreshToken======>', refresh)
            refresh_token = AccessToken(refresh)
            new_access_token = refresh_token.access_token
            access_token_lifetime = datetime.now() + timedelta(minutes=60)

            new_refresh_token = RefreshToken.for_user(refresh_token.user)
            refresh_token_lifetime = datetime.now() + timedelta(days=1)

            response_data = {
                'success': True,
                "access_token": str(new_access_token),
                "refresh_token": str(new_refresh_token)
            }

            response = Response(response_data, status=200)

            response.set_cookie(
                key='refresh_token',
                value=str(new_refresh_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=refresh_token_lifetime
            )

            response.set_cookie(
                key='access_token',
                value=str(new_access_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=access_token_lifetime
            )

            return response

        except TokenError:
            return Response({'success': False, 'message': "Refresh token is expired or invalid"}, status=400)
        except InvalidToken:
            return Response({'success': False, 'message': "Invalid token"}, status=400)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordReset(APIView):
    """Reset password in case of forgetfulness."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Parse JSON data from request
        try:
            data = json.loads(request.body)
            username = data.get('username')
            matricule = data.get('matricule')
            security_question = data.get('security_question')
            security_answer = data.get('security_answer')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON'}, status=400)

        # # Validate new password confirmation
        # if new_password != confirm_password:
        #     return Response({'success': False, 'message': 'New passwords do not match'}, status=400)

        # # Try to retrieve the user
        # try:
        #     user = User.objects.get(
        #         username=username, matricule=matricule, security_question=security_question
        #     )
        #     if user.security_answer != security_answer:
        #         return Response({'success': False, 'message': 'Invalid security question or answer'}, status=400)
        # except User.DoesNotExist:
        #     return Response({'success': False, 'message': 'User not found'}, status=404)

        # # Update user password and save
        # user.set_password(new_password)
        # user.save()

        # return Response({'success': True, 'message': 'Password reset successfully'}, status=200)
