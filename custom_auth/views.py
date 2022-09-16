from rest_framework import status, viewsets, mixins, permissions
from rest_framework.response import Response
from .serializers import *
from .models import *

# Create your views here.

    
class SignUpViewSet(mixins.CreateModelMixin, 
                    viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    # def create(self, request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        # try:
            return super().create(request, *args, **kwargs)
        # except Exception as e:
        #     return Response({"detail": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    

class LibrarienViewSet(mixins.RetrieveModelMixin, 
                       mixins.ListModelMixin,
                       mixins.UpdateModelMixin, 
                       mixins.DestroyModelMixin, 
                       viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LibrarianSerializer
    queryset = Librarian.objects.prefetch_related("user").all()
    
    def list(self, request, *args, **kwargs):
        if Librarian.objects.filter(user=self.request.user).exists() or self.request.user.is_superuser:
            return super().list(request, *args, **kwargs)
        return Response({"detail": "You are not a librarian"}, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, *args, **kwargs):
        if Librarian.objects.filter(user=self.request.user).exists() or self.request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": "You are not a librarian"}, status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, *args, **kwargs):
        if Librarian.objects.filter(user=self.request.user).exists() or self.request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        return Response({"detail": "You are not a librarian"}, status=status.HTTP_403_FORBIDDEN)
    
    
class MemberViewSet(mixins.RetrieveModelMixin, 
                    mixins.ListModelMixin,
                       mixins.UpdateModelMixin, 
                       mixins.DestroyModelMixin, 
                       viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MemberSerializer
    queryset = Member.objects.prefetch_related("user").all()
    
    def get_queryset(self):
        if Librarian.objects.filter(user=self.request.user).exists() or self.request.user.is_superuser:
            return super().get_queryset()
        
        return super().get_queryset().filter(user=self.request.user)
            
    
    