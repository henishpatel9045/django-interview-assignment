from django.db import models, transaction
from django.contrib.auth import get_user_model, models as auth_models


# Create your models here.
User = get_user_model()
Permission = auth_models.Permission
FORBIDDEN_PERMISSIONS = Permission.objects.exclude(models.Q(codename__iendswith='user')
                                                             | models.Q(codename__istartswith='permission')
                                                             | models.Q(codename__istartswith='contenttype')
                                                             | models.Q(codename__istartswith='logentry')
                                                             | models.Q(codename__istartswith='group')
                                                             | models.Q(codename__istartswith='session')
                                                             | models.Q(codename__iendswith='group'))

MEMBER_ALLOWED = [
    'add_returnapproval',
    'delete_returnapproval',
    'view_member',
    'delete_member',
    'add_borrow',
    'view_borrow',
    'add_user',
    'change_user'
]

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    is_new = models.BooleanField(default=True)
    
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name
        
    def __str__(self):
        return self.full_name()
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_new:
                self.user.is_staff = True
                self.user.user_permissions.set(FORBIDDEN_PERMISSIONS)
                self.user.save()
                self.is_new = False    
            return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        with transaction.atomic():
            User.objects.get(pk=self.user.pk).delete()
            return super().delete(*args, **kwargs)
    
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
    is_new = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_new:
                user = User.objects.get(pk=self.user.pk)
                user.is_staff = True
                user.user_permissions.set(Permission.objects.filter(codename__in=MEMBER_ALLOWED))
                user.save()
                self.is_new = False
            return super().save(*args, **kwargs)
    
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name
        
    def __str__(self):
        return self.full_name()
    
    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"
        