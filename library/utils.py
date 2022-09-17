from .models import *
from custom_auth.models import Librarian

def is_librarian(user):
    return Librarian.objects.filter(user=user).exists()

def has_full_access(user):
    return is_librarian(user) or user.is_superuser
