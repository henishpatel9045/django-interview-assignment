from rest_framework import serializers
from .models import *
from custom_auth import models
from .utils import has_full_access, is_librarian

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "category", "published_year", "isbn", "bar_code", "available", "stack_location")
    available = serializers.BooleanField(read_only=True, default=True)        
        
class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ('id', 'book', 'issue_date', 'return_date', 'late_charges')
        
    def create(self, validated_data):
        book = validated_data['book']
        if not book.available:
            raise ValidationError("Selected book is not available.")
        else:
            with transaction.atomic():
                book.available = False
                book.save()        
                user = self.context.user
                print(user)
                if not is_librarian(user):
                    validated_data['borrower'] = models.Member.objects.get(user=self.context.get('request').user)
                user = models.Member.objects.get(pk=validated_data['borrower'])
                count = user.currently_borrowed_books_count
                user.currently_borrowed_books_count = count+1
                user.save()
                return super().create(validated_data)
            
        
class ReturnApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnApproval
        fields = "__all__"
        
    def save(self, **kwargs):
        return super().save(**kwargs)
        
    def save(self, **kwargs):
        return super().save(**kwargs)
        