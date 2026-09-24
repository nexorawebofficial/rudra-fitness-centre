from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email', 'autocomplete': 'email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your phone (optional)', 'autocomplete': 'tel'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your message', 'rows': 5}),
        }
