from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, LeaveRequest


class CustomSignupForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[('employee', 'Employee'), ('manager', 'Manager'), ('admin', 'Admin')],
        required=True
    )
    manager = forms.ModelChoiceField(
        queryset=User.objects.filter(role='manager'),
        required=False,
        empty_label='Select your manager (for employees)',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    by_passkey = False  # Required by newer allauth versions
    
    class Meta:
        model = User
        fields = ('email', 'full_name', 'role', 'manager', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update manager queryset to get latest managers
        self.fields['manager'].queryset = User.objects.filter(role='manager')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.role = self.cleaned_data['role']
        
        # Set manager for employees
        if user.role == 'employee' and self.cleaned_data.get('manager'):
            user.manager = self.cleaned_data['manager']
        
        if user.role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        if commit:
            user.save()
        return user
    
    def try_save(self, request):
        """Required by allauth for custom signup - returns (user, response)"""
        user = self.save(commit=True)
        return user, None


class LeaveRequestForm(forms.ModelForm):
    manager = forms.ModelChoiceField(
        queryset=User.objects.filter(role='manager'),
        required=True,
        empty_label='Choose your manager',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'total_days', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'total_days': forms.HiddenInput(),
            'reason': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Please provide a detailed reason for your leave request...'}),
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'department', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'accept': 'image/*'}),
        }
