from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id']
    
@admin.register(models.Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ['id']
    