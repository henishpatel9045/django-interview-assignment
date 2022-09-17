from rest_framework import status, viewsets, mixins, permissions
from rest_framework.response import Response
from .serializers import *
from .models import *
from library.utils import has_full_access, is_librarian

# Create your views here.

    
class SignUpViewSet(mixins.CreateModelMixin, 
                    viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    # def create(self, request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    

class LibrarienViewSet(mixins.RetrieveModelMixin, 
                       mixins.ListModelMixin,
                       mixins.UpdateModelMixin, 
                       mixins.DestroyModelMixin, 
                       viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LibrarianSerializer
    queryset = Librarian.objects.prefetch_related("user").all()
    
    def list(self, request, *args, **kwargs):
        if has_full_access(request.user):
            return super().list(request, *args, **kwargs)
        return Response({"detail": "You are not a librarian"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, *args, **kwargs):
        if has_full_access(request.user):
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": "You are not a librarian"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        if has_full_access(request.user):
            return super().update(request, *args, **kwargs)
        return Response({"detail": "You are not a librarian"}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class MemberViewSet(mixins.RetrieveModelMixin, 
                    mixins.ListModelMixin,
                       mixins.UpdateModelMixin, 
                       mixins.DestroyModelMixin, 
                       viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MemberSerializer
    queryset = Member.objects.prefetch_related("user").all()
    
    def get_queryset(self):
        if has_full_access(self.request.user):
            return super().get_queryset()
        
        return super().get_queryset().filter(user=self.request.user)
            
    
    