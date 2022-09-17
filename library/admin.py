from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'author', 'published_year', 'isbn', 'available', 'stack_location']
    search_fields = ('title__icontains',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'stack_location', 'issue_period']
    search_fields = ('name__icontains',)
    
admin.site.register([Borrow, ReturnApproval])
