from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
from custom_auth.models import Librarian

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if Librarian.objects.filter(user=self.user).exists():
            return super().create(request, *args, **kwargs)
        return Response({"detail": "Only librarian allowed to add new category."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        if Librarian.objects.filter(user=self.user).exists():
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": "Only librarian allowed to delete category."}, status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        if Librarian.objects.filter(user=self.user).exists():
            return super().update(request, *args, **kwargs)
        return Response({"detail": "Only librarian allowed to add new category."}, status=status.HTTP_401_UNAUTHORIZED)
    
    