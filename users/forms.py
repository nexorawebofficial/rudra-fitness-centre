from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone

from members.models import MemberProfile
from memberships.models import MembershipPlan

User = get_user_model()


class MemberRegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=150, label='Full Name')
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(max_length=15, label='Phone Number')
    date_of_birth = forms.DateField(
        label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}),
    )
    gender = forms.ChoiceField(choices=MemberProfile.GENDER_CHOICES)
    emergency_contact_name = forms.CharField(max_length=100, label='Emergency Contact Name')
    emergency_contact_phone = forms.CharField(max_length=15, label='Emergency Contact Phone')
    membership_plan = forms.ModelChoiceField(
        queryset=MembershipPlan.objects.filter(is_active=True),
        label='Selected Membership', empty_label='Select a plan',
    )
    preferred_training_time = forms.ChoiceField(choices=MemberProfile.TRAINING_TIME_CHOICES, required=False)
    fitness_goal = forms.CharField(max_length=200, required=False, label='Fitness Goal (optional)')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email already exists. Try logging in instead.')
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number'].strip()
        digits = ''.join(ch for ch in phone if ch.isdigit())
        if len(digits) < 10:
            raise ValidationError('Enter a valid phone number (at least 10 digits).')
        return phone

    def clean_emergency_contact_phone(self):
        phone = self.cleaned_data['emergency_contact_phone'].strip()
        digits = ''.join(ch for ch in phone if ch.isdigit())
        if len(digits) < 10:
            raise ValidationError('Enter a valid emergency contact phone number (at least 10 digits).')
        return phone

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = timezone.localdate()
        if dob >= today:
            raise ValidationError('Enter a valid date of birth.')
        age_years = (today - dob).days / 365.25
        if age_years < 14:
            raise ValidationError('Members must be at least 14 years old. Please contact us about junior programs.')
        if age_years > 100:
            raise ValidationError('Enter a valid date of birth.')
        return dob

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            validate_password(password)
        return password

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
