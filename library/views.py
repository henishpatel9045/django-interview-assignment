from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
from custom_auth.models import Librarian

# Create your views here.

class LibrarianPermissionViewSet(viewsets.ModelViewSet):
    record = None
    
    def create(self, request, *args, **kwargs):
        if Librarian.objects.filter(user=self.request.user).exists():
            return super().create(request, *args, **kwargs)
        return Response({"detail": f"Only librarian allowed to add new {self.record}."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        if Librarian.objects.filter(user=self.request.user).exists():
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": f"Only librarian allowed to delete {self.record}."}, status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        if Librarian.objects.filter(user=self.request.user).exists():
            return super().update(request, *args, **kwargs)
        return Response({"detail": f"Only librarian allowed to update {self.record}."}, status=status.HTTP_401_UNAUTHORIZED)

class CategoryViewSet(LibrarianPermissionViewSet, viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    record = "category"


class BookViewSet(LibrarianPermissionViewSet, viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    record = "book"
    

class BorrowViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.all()
    permission_classes = [permissions.IsAuthenticated]
       
    def update(self, request, *args, **kwargs):
        if Librarian.objects.filter(user=self.request.user).exists():
            return super().update(request, *args, **kwargs)
        return Response({"detail": f"Only librarian allowed to update borrow record."}, status=status.HTTP_401_UNAUTHORIZED)
    

class ReturnApprovalViewSet(viewsets.ModelViewSet):
    serializer_class = ReturnApprovalSerializer
    queryset = ReturnApproval.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    