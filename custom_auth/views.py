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
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    

class LibrarienViewSet(mixins.RetrieveModelMixin, 
                       mixins.UpdateModelMixin, 
                       mixins.DestroyModelMixin, 
                       viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LibrarianSerializer
    queryset = Librarian.objects.select_for_update("user").all()
    
    