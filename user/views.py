from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django.http import Response
from user.serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView

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