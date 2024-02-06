from django import forms
from .models import Authentication, MemberAuthentication

class AuthenticationForm(forms.ModelForm):
    class Meta:
        model = Authentication
        fields =['start', 'end']

class MemberAuthenticationForm(forms.ModelForm):
    class Meta:
        model = MemberAuthentication
        fields = ['content', 'image']
