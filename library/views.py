from datetime import date
from datetime import date
from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
from custom_auth.models import Librarian
from drf_yasg.utils import swagger_auto_schema
from .utils import has_full_access, is_librarian

# Create your views here.

class LibrarianPermissionViewSet(viewsets.ModelViewSet):
    record = None
    
    def create(self, request, *args, **kwargs):
        if has_full_access(request.user):
            return super().create(request, *args, **kwargs)
        return Response({"detail": f"Only librarian allowed to add new {self.record}."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        if has_full_access(request.user):
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": f"Only librarian allowed to delete {self.record}."}, status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        if has_full_access(request.user):
            return super().update(request, *args, **kwargs)
        return Response({"detail": f"Only librarian allowed to update {self.record}."}, status=status.HTTP_401_UNAUTHORIZED)

class CategoryViewSet(LibrarianPermissionViewSet, viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    record = "category"


class BookViewSet(LibrarianPermissionViewSet, viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.prefetch_related("category").all()
    permission_classes = [permissions.IsAuthenticated]
    record = "book"
    

class BorrowViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.prefetch_related("book").prefetch_related("borrower").all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        return self.request
           record = "category"


class BookViewSet(LibrarianPermissionViewSet, viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.prefetch_related("category").all()
    permission_classes = [permissions.IsAuthenticated]
    record = "book"
    

class BorrowViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.prefetch_related("book").prefetch_related("borrower").all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        return self.request
       
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": e.args[0]}, status.HTTP_400_BAD_REQUEST)
    

class BorrowByUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = BorrowSerializer
    def get_queryset(self):
        return Borrow.objects.filter(borrower__user=self.request.user)
    

def calculate_fine(issue_date, fine_per_day, day_limit):
    today = date.today() - issue_date.date()
    return max(fine_per_day * (day_limit-today.days), 0)

class ReturnApprovalViewSet(viewsets.ModelViewSet):
    serializer_class = ReturnApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        res = ReturnApproval.objects.prefetch_related("borrow").all()
        if not is_librarian(self.request.user):
            return res.filter(res.filter(borrow__borrower__user=self.request.user))
        return res
    
    def update(self, request, *args, **kwargs):
        return_obj = ReturnApproval.objects.get(pk=kwargs['pk'])
        with transaction.atomic():
            if return_obj.approved:
                return_obj.approved_by = self.request.user
                charge = calculate_fine(return_obj.borrow.issue_date, 2,
                                        return_obj.borrow.book.category.issue_period)
                return_obj.borrow.return_date = timezone.now().today()
                return_obj.borrow.returned = True
                return_obj.borrow.book.available = True
                return_obj.borrow.late_charges = charge
                pending_charge = return_obj.borrow.borrower.pending_charge
                return_obj.borrow.borrower.pending_charge = pending_charge + charge
                return_obj.borrow.borrower.save()
                return_obj.borrow.book.save()
                return_obj.borrow.save()
                return_obj.save()
            return super().update(request, *args, **kwargs)
            
            