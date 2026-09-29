from django import forms
from allauth.account.forms import SignupForm

from .models import User, LeaveRequest


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=255, required=True)
    role = forms.ChoiceField(choices=[('employee', 'Employee'), ('manager', 'Manager')])
    manager = forms.ModelChoiceField(
        queryset=User.objects.none(), required=False,
        empty_label='Select your manager',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_manager'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager'].queryset = User.objects.filter(role='manager', is_active=True)

    def clean(self):
        data = super().clean()
        if data.get('role') != 'employee':
            data['manager'] = None
        return data


class LeaveRequestForm(forms.ModelForm):
    total_days = forms.IntegerField(widget=forms.HiddenInput(), required=False)
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

    def clean(self):
        data = super().clean()
        start, end = data.get('start_date'), data.get('end_date')
        if start and end:
            if end < start:
                self.add_error('end_date', 'End date must be on or after start date.')
            else:
                data['total_days'] = (end - start).days + 1
        return data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'department', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'accept': 'image/*'}),
        }
