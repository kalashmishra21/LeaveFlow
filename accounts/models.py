from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    CUSTOM USER MODEL - Email-based authentication (no username)
    Extends Django's AbstractBaseUser for custom fields
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    
    email = models.EmailField(unique=True)  # Used for login instead of username
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    
    # SELF-REFERENCING FOREIGN KEY: User can be manager of other users
    # Complex relationship: One user (manager) can have many users (employees)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members')
    
    # PROFILE PICTURE UPLOAD: Uses Pillow library, saves to media/profiles/
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'  # Login with email instead of username
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'users'


class LeaveType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    default_days = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'leave_types'


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.email} - {self.leave_type.name}"
    
    class Meta:
        db_table = 'leave_requests'
        ordering = ['-created_at']


class LeaveBalance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    year = models.IntegerField()
    total_days = models.IntegerField()
    used_days = models.IntegerField(default=0)
    
    @property
    def remaining_days(self):
        return self.total_days - self.used_days
    
    def __str__(self):
        return f"{self.employee.email} - {self.leave_type.name} ({self.year})"
    
    class Meta:
        db_table = 'leave_balances'
        unique_together = ['employee', 'leave_type', 'year']


class ChatMessage(models.Model):
    """
    CHAT MESSAGE MODEL - Stores messages with file attachments
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField(blank=True)  # Text message (optional if file attached)
    
    # FILE UPLOAD: Stores images and PDFs in media/chat_attachments/
    # Uses Pillow library for image processing
    attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)
    attachment_name = models.CharField(max_length=255, blank=True)
    
    is_read = models.BooleanField(default=False)  # For unread badge
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.email} -> {self.receiver.email}"
    
    @property
    def is_image(self):
        """
        FILE TYPE DETECTION: Check if attachment is an image
        Used in template to show image preview vs download link
        """
        if self.attachment:
            ext = self.attachment.name.lower().split('.')[-1]
            return ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']
        return False
    
    @property
    def is_pdf(self):
        """
        FILE TYPE DETECTION: Check if attachment is a PDF
        Used in template to show PDF icon and download link
        """
        if self.attachment:
            return self.attachment.name.lower().endswith('.pdf')
        return False
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']
