from .models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

def token_authenticated(pk, request):
    try:
        user = CustomUser.objects.get(pk=pk)
        token, _ = Token.objects.get_or_create(user=user)
        assert request.META.get('HTTP_AUTHORIZATION').replace('Token', '').strip() == token.key
        return True, user, token
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND), user, token
    except AssertionError:
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED), user, token