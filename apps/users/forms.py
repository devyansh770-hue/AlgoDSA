from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Registration form with preferred language selection."""
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'Email (optional)',
        'autocomplete': 'email',
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'preferred_language')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Username',
                'autocomplete': 'username',
            }),
            'preferred_language': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm Password',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email


class UserProfileForm(forms.ModelForm):
    """Profile edit form."""

    class Meta:
        model = User
        fields = ('bio', 'preferred_language', 'leetcode_username', 'gfg_username')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Tell us about yourself...',
                'rows': 4,
            }),
            'preferred_language': forms.Select(attrs={
                'class': 'form-select',
            }),
            'leetcode_username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. leetcode_user123',
            }),
            'gfg_username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. gfg_handle_123',
            }),
        }
