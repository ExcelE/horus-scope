from .models import Classification, CustomUser
from .serializers import UserSerializer, ClassificationSerializer
from rest_framework import generics, permissions, authentication, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .authenticate import token_authenticated
import sys

# Generic classes automatically handle multiple methods, and have responses pre-made
# https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview

# GET, POST Classifications
class ClassificationList(generics.ListCreateAPIView):
    # What set of queries to return for GET, for example
    queryset = Classification.objects.all()

    # What serializer to use to convert objects from JSON to native objects in python
    serializer_class = ClassificationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (authentication.TokenAuthentication,)
    
    # Override the serialization save method in the POST method by passing in the owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ClassificationUserList(generics.ListAPIView):
    serializer_class = ClassificationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (authentication.TokenAuthentication,)

    # Make a custom queryset instead of defining it above for only the ones with this owner
    def get_queryset(self):
        return Classification.objects.filter(owner=self.kwargs['pk'])

    def list(self, request, pk):
        response, _, _ = token_authenticated(pk, request)
        if response is not True:
            return response


        queryset = self.get_queryset()

        serializer = ClassificationSerializer(queryset, many=True)
        return Response(serializer.data)

# GET, DELETE a single Classification
class ClassificationDetail(generics.RetrieveDestroyAPIView):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (authentication.TokenAuthentication,)

# GET, PUT, PATCH, DELETE a User
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    # Make sure a user can only retrieve itself by providing their own token in the Authorization header
    def retrieve(self, request, pk):
        response, user, _ = token_authenticated(pk, request)
        if response is not True:
            return response
        serializer = UserSerializer(user)
        return Response(serializer.data)

# POST for User registration
class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data=request.data) # Can also do self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer) # The parent class function that actually does the serialization
            headers = self.get_success_headers(serializer.data)
            token, _ = Token.objects.get_or_create(user=serializer.instance) # Second variable is created
            return Response({'id': serializer.instance.id, 'token': token.key}, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# POST request for login. No need for a generics.View (that has built in serializer support) since there is no model to use, thuse no serializer to use
class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'id': user.id, 'token': token.key}, status.HTTP_200_OK)
