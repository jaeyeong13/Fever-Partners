from django import forms
from .models import MemberAuthentication

class MemberAuthenticationForm(forms.ModelForm):
    class Meta:
        model = MemberAuthentication
        fields = ['content', 'image']
