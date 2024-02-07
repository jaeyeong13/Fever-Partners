from django import forms
from .models import Authentication, MemberAuthentication

class AuthenticationForm(forms.ModelForm):
    class Meta:
        model = Authentication
        fields =['start', 'end']
        start = forms.CharField(widget=forms.TimeInput(format='%H:%M'))
        end = forms.CharField(widget=forms.TimeInput(format='%H:%M'))

class MemberAuthenticationForm(forms.ModelForm):
    class Meta:
        model = MemberAuthentication
        fields = ['content', 'image']