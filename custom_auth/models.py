from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
        
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name
        
    def __str__(self):
        return self.full_name()
    
    class Meta:
        verbose_name = "Librarian"
        verbose_name_plural = "Librarians"


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    aadhaar_card_id = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    currently_borrowed_books_count = models.IntegerField(default=0)
    pending_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)        
        
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name
        
    def __str__(self):
        return self.full_name()
    
    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"
        