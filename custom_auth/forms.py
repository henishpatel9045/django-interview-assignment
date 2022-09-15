from django import forms
from .models import Member, Librarian

class CustomUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField()
        
            
class MemberForm(CustomUserForm):
    class Meta():
        model = Member
        fields = ['user', 'first_name', 'last_name', 'email']        
        fields += ['phone_number', 'aadhaar_card_id', 'date_of_birth', 'address', 'pin_code', 
                  'currently_borrowed_books_count', 'pending_charge']
        
class LibrarianForm(CustomUserForm):
    class Meta():
        model = Librarian    
        fields = ['user', 'first_name', 'last_name', 'email']        
        fields += ['phone_number', 'address'] 
