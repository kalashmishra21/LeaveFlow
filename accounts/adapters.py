from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.full_name = form.cleaned_data.get('full_name', '')
        user.role = form.cleaned_data.get('role', 'employee')
        if user.role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        if commit:
            user.save()
        return user
    
    def populate_username(self, request, user):
        """No username field needed"""
        pass
    
    def get_login_redirect_url(self, request):
        """Redirect to role-specific dashboard"""
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                return '/dashboard/admin/'
            elif request.user.role == 'manager':
                return '/dashboard/manager/'
            else:
                return '/dashboard/employee/'
        return '/'
    
    def add_message(self, request, level, message_template, message_context=None, extra_tags=''):
        """Disable only success messages, show errors"""
        from django.contrib import messages
        # Only disable success messages (level 25), show errors (level 40)
        if level != messages.SUCCESS:
            super().add_message(request, level, message_template, message_context, extra_tags)
