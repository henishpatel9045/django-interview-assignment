from django import forms
from .models import Member, Librarian
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import Q

class CustomUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField()
    
    class Meta:
        fields = ['user', 'first_name', 'last_name', 'email']        
    
    def save(self, *args, **kwargs):
        with transaction.atomic():
            user = get_user_model().objects.get(pk=self.cleaned_data.get('user').pk)
            user.first_name = self.cleaned_data.get('first_name')
            user.last_name = self.cleaned_data.get('last_name')
            user.email = self.cleaned_data.get('email')
            user.save()    
            return super().save(*args, **kwargs)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User = get_user_model()
        self.fields['user'].queryset = User.objects.exclude(Q(pk__in=Member.objects.all().values('user')) 
                                                            | Q(pk__in=Librarian.objects.all().values('user')))
    
class MemberForm(CustomUserForm):
    class Meta():
        model = Member
        fields = CustomUserForm.Meta.fields
        fields += ['phone_number', 'aadhaar_card_id', 'date_of_birth', 'address', 'pin_code', 
                  'currently_borrowed_books_count', 'pending_charge']
        
class LibrarianForm(CustomUserForm):
    class Meta():
        model = Librarian    
        fields = CustomUserForm.Meta.fields
        fields += ['phone_number', 'address'] 
