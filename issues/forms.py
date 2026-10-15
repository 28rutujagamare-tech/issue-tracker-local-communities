from django import forms
from .models import Issue
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Form for Issues
class IssueForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('light', 'Broken Streetlight'),
        ('garbage', 'Garbage'),
        ('road', 'Road Damage'),
        ('water', 'Water Supply'),
    ]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Issue
        fields = ['title', 'description', 'category', 'location', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }


# Form for User Registration
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
