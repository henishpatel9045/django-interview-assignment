from django.contrib import admin

from django.db import transaction
from .models import Librarian
from . import models, forms
from django.contrib.auth import get_user_model

User = get_user_model()
# Register your models here.
class UserAdmin(admin.ModelAdmin):    
    def get_form(self, req, obj, **kwargs):
        form = super().get_form(req, obj, **kwargs)
        try:
            form.base_fields['first_name'].initial = obj.user.first_name
            form.base_fields['last_name'].initial = obj.user.last_name
            form.base_fields['email'].initial = obj.user.email        
            form.base_fields.get('user').widget.attrs['readonly'] = True
            form.base_fields['user'].queryset = User.objects.filter(pk=obj.user.pk)
            return form
        except Exception as e:
            return form
    
    def get_queryset(self, request):
        res = super().get_queryset(request)
        user = request.user
        if Librarian.objects.filter(user=user).exists():
            return res
        else:
            return res.filter(user=user)
    
    def save_form(self, request, form, change):
        with transaction.atomic():
            user = User.objects.get(pk=request.user.pk)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()    
            return super().save_form(request, form, change)

@admin.register(models.Member)
class MemberAdmin(UserAdmin):
    list_display = ['id']
    form = forms.MemberForm
    
    def get_readonly_fields(self, request,obj=None):
        res = ['phone_number', 'aadhaar_card_id', 'date_of_birth', 'address', 'pin_code', 'currently_borrowed_books_count', 'pending_charge']
        return res      

@admin.register(models.Librarian)
class LibrarianAdmin(UserAdmin):
    list_display = ['id']
    form = forms.LibrarianForm
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(user=request.user)
    
    