from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ContestSerializer
from .models import Contest

# Create your views here.

class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer