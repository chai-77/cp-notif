from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset =  User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    # only get is defined
    def get(self, request):
        return Response(UserSerializer(request.user).data)