from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import BlacklistedToken

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print("🔍 CustomJWTAuthentication called")
        return super().authenticate(request)
    

    def get_user(self, validated_token):
        jti = validated_token.get('jti')
        token_type = validated_token.get('token_type')

        # Reject refresh tokens for normal API access
        if token_type != 'access':
            raise InvalidToken("Only access tokens are allowed for authentication")

        # Reject blacklisted tokens
        if BlacklistedToken.objects.filter(jti=jti).exists():
            raise InvalidToken("Token has been blacklisted")

        return super().get_user(validated_token)
