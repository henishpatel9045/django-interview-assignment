from django.contrib import admin
from . import models, forms

class UserAdmin(admin.ModelAdmin):    
    def get_form(self, req, obj, **kwargs):
        form = super().get_form(req, obj, **kwargs)
        try:
            form.base_fields['first_name'].initial = obj.user.first_name
            form.base_fields['last_name'].initial = obj.user.last_name
            form.base_fields['email'].initial = obj.user.email        
            return form
        except Exception as e:
            return form

# Register your models here.
@admin.register(models.Member)
class MemberAdmin(UserAdmin):
    list_display = ['id']
    form = forms.MemberForm
    
@admin.register(models.Librarian)
class LibrarianAdmin(UserAdmin):
    list_display = ['id']
    form = forms.LibrarianForm
    