from django.shortcuts import render
from django.utils import timezone
# from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSignupSerializer, UserLoginSerializer, UserProfileSerializer
from datetime import datetime
from .models import ActiveToken, BlacklistedToken, User

# Create your views here.
@swagger_auto_schema(
    method='post',
    request_body=UserSignupSerializer,
    responses={
        201: openapi.Response("User registered successfully"),
        400: "Validation Error",
    },
    operation_summary="Register a new user",
    operation_description="Create a new user account and receive JWT access and refresh tokens.",
)
@api_view(['POST'])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "user_type": user.user_type
            },
            "token": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=UserLoginSerializer,
    responses={
        200: openapi.Response("Login successful"),
        400: "Invalid credentials",
    },
    operation_summary="Login existing user",
    operation_description="Authenticate using email and password, receive JWT tokens.",
)
@api_view(['POST'])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = issue_tokens_for_user(user)
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "user_type": user.user_type
            },
            "token": {
                "access": str(refresh['access']),
                "refresh": str(refresh['refresh']),
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_summary="Refresh access token",
    operation_description=(
        "Use a valid, non-blacklisted refresh token to obtain a new access token.\n\n"
        "**Rules:**\n"
        "- The refresh token must not be expired.\n"
        "- The refresh token must not be blacklisted (logged out).\n"
        "- Returns a new short-lived access token for further API calls."
    ),
    tags=['auth'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['refresh'],
        properties={
            'refresh': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Valid refresh token obtained during login'
            ),
        },
        example={'refresh': 'refresh_token'},
    ),
    responses={
        200: openapi.Response(
            description="Access token refreshed successfully",
            examples={
                "application/json": {"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
            },
        ),
        400: openapi.Response(
            description="Refresh token missing or invalid",
            examples={"application/json": {"detail": "Refresh token required."}},
        ),
        401: openapi.Response(
            description="Blacklisted or expired refresh token",
            examples={"application/json": {"detail": "This refresh token has been blacklisted."}},
        ),
    },
)
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_access_token(request):
    """
    Generate a new access token using a non-blacklisted refresh token.
    """
    refresh_token_str = request.data.get('refresh')

    if not refresh_token_str:
        return Response(
            {"detail": "Refresh token required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        refresh_token = RefreshToken(refresh_token_str)
        jti = refresh_token['jti']
        exp = timezone.datetime.fromtimestamp(refresh_token['exp'], tz=timezone.utc)
    except TokenError:
        raise InvalidToken("Invalid refresh token.")
    except Exception as e:
        print("Refresh token decode error:", e)
        raise InvalidToken("Invalid refresh token format.")

    if BlacklistedToken.objects.filter(jti=jti).exists():
        raise InvalidToken("This refresh token has been blacklisted.")

    if exp < timezone.now():
        raise InvalidToken("Refresh token has expired.")

    new_access = str(refresh_token.access_token)
    return Response({"access": new_access}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_summary="Logout user (blacklist both access & refresh tokens)",
    operation_description=(
        "Requires a valid **access token** in the Authorization header. "
        "Blacklists both provided `access` and `refresh` tokens if valid."
    ),
    tags=['auth'],
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Bearer access token',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['refresh'],
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
        },
    ),
    responses={
        205: openapi.Response("Logout successful (tokens blacklisted)"),
        400: openapi.Response("Missing or invalid token(s)"),
        401: openapi.Response("Authentication required"),
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Blacklist both access and refresh tokens.
    Requires valid access token in Authorization header.
    """
    auth_header = request.headers.get('Authorization')
    refresh_token_str = request.data.get('refresh')
    revoked_tokens = []

    if auth_header and auth_header.startswith('Bearer '):
        access_token_str = auth_header.split(' ')[1]
        try:
            access_token = AccessToken(access_token_str)
            jti = access_token['jti']
            BlacklistedToken.objects.get_or_create(
                user_id=request.user.id,
                jti=jti,
                token_type='access',
                defaults={'revoked_at': timezone.now(),
                          'expires_at': timezone.make_aware(
                              timezone.datetime.fromtimestamp(access_token['exp']))}
            )
            revoked_tokens.append('access')
        except Exception as e:
            print("Access token blacklist error:", e)

    if refresh_token_str:
        try:
            refresh_token = RefreshToken(refresh_token_str)
            jti = refresh_token['jti']
            BlacklistedToken.objects.get_or_create(
                user_id=request.user.id,
                jti=jti,
                token_type='refresh',
                defaults={'revoked_at': timezone.now(),
                          'expires_at': timezone.make_aware(
                              timezone.datetime.fromtimestamp(refresh_token['exp']))}
            )
            revoked_tokens.append('refresh')
        except Exception as e:
            print("Refresh token blacklist error:", e)

    if not revoked_tokens:
        return Response({"error": "No valid tokens provided."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "message": "Logout successful",
        "blacklisted_tokens": revoked_tokens
    }, status=status.HTTP_205_RESET_CONTENT)


@swagger_auto_schema(
    method='get',
    operation_summary="Get user profile (requires access token)",
    operation_description=(
        "Fetches the authenticated user's details from the database. "
        "Requires a valid **access token** in the Authorization header."
    ),
    tags=['user'],
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Bearer access token',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: openapi.Response("User profile retrieved successfully"),
        401: openapi.Response("Invalid or expired access token"),
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    try:
        user = User.objects.get(pk=request.user.id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Util methods Section [will migrate this section as utils.py code later]
def issue_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    # Save both in ActiveToken table
    ActiveToken.objects.update_or_create(
        jti=refresh['jti'],
        defaults={
            'user': user,
            'token_type': 'refresh',
            'expires_at': timezone.datetime.fromtimestamp(access['exp'], tz=timezone.utc)
        },
    )
    ActiveToken.objects.update_or_create(
        jti=access['jti'],
        defaults={
            'user': user,
            'token_type': 'access',
            'expires_at': timezone.datetime.fromtimestamp(access['exp'], tz=timezone.utc)
        },
    )

    return {
        'access': str(access),
        'refresh': str(refresh),
    }
