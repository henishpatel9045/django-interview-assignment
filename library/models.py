from django.db import models, transaction
from django.utils import timezone
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

Member = settings.LIBRARY_MEMBER_MODEL
Librarian = settings.LIBRARY_LIBRARIAN_MODEL

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    stack_location = models.CharField(max_length=20)
    issue_period = models.IntegerField(default=15)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_year = models.IntegerField(validators=[MaxValueValidator(timezone.now().year, "Published year can't be in future."),
                                                     MinValueValidator(0, "Published year can't be negative.")])
    isbn = models.CharField(max_length=20)
    bar_code = models.CharField(max_length=50, unique=True)
    available = models.BooleanField(default=True)
    stack_location = models.CharField(max_length=20, blank=True)
    
    def save(self, *args, **kwargs):
        if self.stack_location == "":
            self.stack_location = self.category.stack_location
        return super().save(*args, **kwargs)
    
class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)    
    late_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    
    def save(self, *args, **kwargs):
        if not self.book.available:
            raise ValidationError("Selected book is not available.")
        else:
            with transaction.atomic():
                self.book.available = False
                self.book.available.save()
                return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.book.title} - {self.borrower.full_name()}"
    
class ReturnApproval(models.Model):
    borrow = models.ForeignKey(Borrow, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(Librarian, on_delete=models.CASCADE)
    approved_on = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.borrow.book.title} - {self.borrow.borrower.full_name()}"
        
