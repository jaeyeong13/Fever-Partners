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

        widgets = {
            'content': forms.Textarea(attrs={'class': 'auth-input', 'label': '내용'}),
            'image': forms.ClearableFileInput(attrs={'class': 'auth-input', 'label': '사진'}),
        }
        