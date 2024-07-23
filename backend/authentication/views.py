from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from datetime import datetime, timedelta
import json
import random

from authentication.models import PasswordResetCode
from users.models import User
from users.forms import SignUpForm


@csrf_exempt
@permission_classes([IsAuthenticated])
def signup_view(request):
    """Signup new user"""
    # if not request.user.is_authenticated:
    #     return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'POST':
        data = json.loads(request.body)
        form = SignUpForm(data)
        if form.is_valid():
            user = form.save()
            # Explicitly specify the backend for authentication and login
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            # Uncomment to log in the user after signup
            auth_login(request, user)
            return JsonResponse({'success': True, 'message': 'User created and logged in successfully'})
        else:
            return JsonResponse({'success': False, 'message': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'POST method required'}, status=405)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """Login to application"""

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'success': False, 'message': 'Username and password are required.'}, status=400)

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            auth_login(request, user)

            # Generate tokens
            refresh_token = RefreshToken.for_user(user)
            access_token = AccessToken.for_user(user)

            # Define the expiration time for refresh and access tokens
            refresh_token_lifetime = datetime.now() + timedelta(days=1)
            access_token_lifetime = datetime.now() + timedelta(minutes=60)

            # Serialize user data
            user_data = {
                'id': user.id,
                'username': user.username,
                'cnie': user.cnie,
            }

            response_data = {
                'success': True,
                'user': user_data,
                'refresh_token': str(refresh_token),
                'access_token': str(access_token)
            }

            response = Response(response_data, status=200)

            # Set cookies for tokens
            response.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=refresh_token_lifetime
            )

            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                expires=access_token_lifetime
            )

            # Set CORS headers
            response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:3000'
            response['Access-Control-Allow-Credentials'] = 'true'

            return response
        else:
            return Response({'success': False, 'message': 'Invalid credentials'}, status=401)


class LogoutView(APIView):
    """Logout"""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logout(request)

            response = Response({
                'success': True,
                'message': 'Logout successful'
            }, status=200)

            response.delete_cookie('refresh_token')
            response.delete_cookie('access_token')
            response.delete_cookie('csrftoken')
            response.delete_cookie('sessionid')

            return response
        else:
            return Response({
                'success': False,
                'message': 'Authentication Required'
            }, status=401)


@permission_classes([IsAuthenticated])
class AboutMeView(View):
    """About me - get all information about user"""

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        user = request.user

        user_data = {
            'idUser': user.id,
            'username': user.username,
            'cnie': user.cnie,
            'Role': user.groups.first().name if user.groups.exists() else user.role,
        }
        return JsonResponse({'success': True, 'user': user_data}, status=200)


@permission_classes([IsAuthenticated])
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON'}, status=400)

        current_password = data.get('current_password')
        new_password = data.get('new_password')
        new_password_confirm = data.get('new_password_confirm')

        if not current_password or not new_password or not new_password_confirm:
            return Response({'success': False, 'message': 'All fields are required'}, status=400)

        if not check_password(current_password, request.user.password):
            return Response({'success': False, 'message': 'Current password is incorrect'}, status=400)

        if new_password != new_password_confirm:
            return Response({'success': False, 'message': 'New passwords do not match'}, status=400)

        request.user.set_password(new_password)
        request.user.save()

        return Response({'success': True, 'message': 'Password changed successfully'}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    # if not request.user.is_authenticated:
    #     return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

    refresh = request.COOKIES.get('refresh_token', None)

    if refresh is None:
        return Response({'success': False, 'message': "Refresh token is required"}, status=400)

    try:
        refresh_token = RefreshToken(refresh)
        new_access_token = refresh_token.access_token

        refresh_token_lifetime = datetime.now() + timedelta(days=1)

        refresh_token.set_jti()
        # refresh_token.set_exp(lifetime=refresh_token_lifetime)
        refresh_token.set_exp()

        response = Response({
            'success': True,
            "access_token": str(new_access_token),
            # "refresh_token": str(refresh_token),
        })

        response.set_cookie('refresh_token', str(refresh_token), httponly=True)

        return response
    except TokenError:
        return Response({'success': False, 'message': "Refresh token is expired or invalid"}, status=400)
    except InvalidToken:
        return Response({'success': False, 'message': "Invalid token"}, status=400)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=400)


activation_codes = {}


@method_decorator(csrf_exempt, name='dispatch')
@permission_classes([IsAuthenticated])
class PasswordResetRequestView(View):
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

        username = data.get('username')
        cnie = data.get('cnie')

        if not username or not cnie:
            return JsonResponse({'success': False, 'message': 'Username and cnie are required'}, status=401)

        try:
            user = User.objects.get(username=username, cnie=cnie)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User with this username and cnie does not exist'}, status=404)

        existing_code = PasswordResetCode.objects.filter(user=user).first()

        codeActivation = str(random.randint(1000, 9999))
        expiration_time = make_aware(datetime.now() + timedelta(minutes=10))

        if existing_code:
            existing_code.activation_code = codeActivation
            existing_code.expires_at = expiration_time
            existing_code.save()
        else:
            activation_codes[user.id] = {
                'codeActivation': codeActivation,
                'expires_at': expiration_time
            }

            PasswordResetCode.objects.create(
                user=user,
                activation_code=codeActivation,
                expires_at=expiration_time
            )

        return JsonResponse({'success': True, 'codeActivation': codeActivation, 'expires_at': expiration_time}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
@permission_classes([IsAuthenticated])
class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'success': False, 'message': 'Invalid JSON'}, status=400)

        codeActivation = data.get('codeActivation')
        new_password = data.get('new_password')
        new_password_confirm = data.get('new_password_confirm')

        if not codeActivation or not new_password or not new_password_confirm:
            return Response({'success': False, 'message': 'All fields are required'}, status=400)

        if new_password != new_password_confirm:
            return Response({'success': False, 'message': 'New passwords do not match'}, status=400)

        try:
            password_reset_code = PasswordResetCode.objects.get(
                user=request.user, activation_code=codeActivation)
        except PasswordResetCode.DoesNotExist:
            return Response({'success': False, 'message': 'Invalid activation code'}, status=400)

        if password_reset_code.expires_at < make_aware(datetime.now()):
            return Response({'success': False, 'message': 'Activation code has expired'}, status=400)

        user = password_reset_code.user
        user.set_password(new_password)
        user.save()

        password_reset_code.delete()

        return Response({'success': True, 'message': 'Password reset successfully'}, status=200)
