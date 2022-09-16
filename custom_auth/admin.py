from urllib import request
from django.contrib import admin

from django.db import transaction
from .models import Librarian
from . import models, forms
from django.contrib.auth import get_user_model, models as auth_models

User = get_user_model()
admin.site.site_header = "Library Management System"
admin.site.index_title = "Dashboard"

# Register your models here.
class UserAdmin(admin.ModelAdmin):   
    exclude = ['is_new'] 

    def get_form(self, req, obj, **kwargs):
        form = super().get_form(req, obj, **kwargs)
        try:
            form.base_fields['first_name'].initial = obj.user.first_name
            form.base_fields['last_name'].initial = obj.user.last_name
            form.base_fields['email'].initial = obj.user.email        
            form.base_fields.get('user').widget.attrs['readonly'] = True
            print(request.user.is_superuser)
            form.base_fields['user'].queryset = User.objects.exclude(is_superuser=True).filter(pk=obj.user.pk)
            return form
        except Exception as e:
            return form
    
    def get_queryset(self, request):
        res = super().get_queryset(request)
        user = request.user
        if Librarian.objects.filter(user=user).exists() or request.user.is_superuser:
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

@admin.register(models.Librarian)
class LibrarianAdmin(UserAdmin):
    list_display = ['id']
    form = forms.LibrarianForm
    
    def get_queryset(self, request):
        return (super()
                .get_queryset(request)
                .filter(user=request.user) 
                if not request.user.is_superuser
                else super().get_queryset(request))
    
    