from rest_framework import status, viewsets, mixins, permissions
from rest_framework.response import Response
from .serializers import *
from .models import *

# Create your views here.

    
class SignUpViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    # def create(self, request, *args, **kwargs)
        
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)