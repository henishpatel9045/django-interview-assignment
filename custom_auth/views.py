import json
from rest_framework import status, viewsets, mixins, permissions, views
from rest_framework.response import Response
from .serializers import *
from .models import *
import requests

# Create your views here.

    
class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    # def create(self, request, *args, **kwargs)
    