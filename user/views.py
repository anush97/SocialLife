from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import check_password
# Create your views here.
class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url 
    permission_classes = (AllowAny,)
    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']
        user = User.objects.get(email=email)
        if user and check_password(password, user.password):
            refresh = RefreshToken.for_user(user)
            user_details = {
                'name': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'token': str(refresh.access_token),
            }
            return Response(user_details, status=status.HTTP_200_OK)
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        res = {'error': 'User with given email does not exist'}
        return Response(res, status=status.HTTP_404_NOT_FOUND)
