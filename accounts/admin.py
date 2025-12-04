from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, LeaveType, LeaveRequest, LeaveBalance

# Unregister unnecessary models
admin.site.unregister(Group)

try:
    from django.contrib.sites.models import Site
    admin.site.unregister(Site)
except:
    pass

try:
    from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
    admin.site.unregister(SocialApp)
    admin.site.unregister(SocialAccount)
    admin.site.unregister(SocialToken)
except:
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'department', 'profile_picture')}),
        ('Permissions', {'fields': ('role', 'manager', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'full_name', 'role'),
        }),
    )


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_days')
    search_fields = ('name',)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'total_days', 'status', 'created_at')
    list_filter = ('status', 'leave_type', 'created_at')
    search_fields = ('employee__email', 'employee__full_name')
    date_hierarchy = 'created_at'


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'year', 'total_days', 'used_days', 'remaining_days')
    list_filter = ('year', 'leave_type')
    search_fields = ('employee__email', 'employee__full_name')
