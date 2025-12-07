  # LeaveFlow - Project Documentation

## 📋 Project Overview
**LeaveFlow** is an Employee Leave Management System built with Django that allows employees to request leaves, managers to approve/reject them, and provides real-time chat functionality.

---

## 🛠 Technologies & Tools Used

### 1. **Backend Framework**
- **Django 4.2** - Python web framework
- **Why**: Rapid development, built-in admin panel, ORM, security features
- **Location**: `config/settings.py` (Line 1-120)

### 2. **Database**
- **SQLite** (Development) - File-based database
- **PostgreSQL** (Production) - Relational database
- **Tool Used**: `dj-database-url` - Database URL parser
- **Location**: `config/settings.py` (Line 58-68)
- **Code**:
```python
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
```

### 3. **Authentication System**
- **django-allauth** - Email-based authentication
- **Why**: No username required, social auth support, customizable
- **Location**: 
  - Settings: `config/settings.py` (Line 90-105)
  - Custom Adapter: `accounts/adapters.py` (Line 1-20)
  - Custom Form: `accounts/forms.py` (Line 6-40)
- **Features**:
  - Email login (no username)
  - Role-based access (Admin, Manager, Employee)
  - Password visibility toggle

### 4. **Static Files Management**
- **WhiteNoise** - Serves static files in production
- **Why**: No need for separate CDN or server for static files
- **Location**: `config/settings.py` (Line 35-40)
- **Code**:
```python
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Line 36
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 5. **Environment Variables**
- **python-decouple** - Manages .env file
- **Why**: Keep secrets out of code, different configs for dev/prod
- **Location**: `config/settings.py` (Line 8-11)
- **Code**:
```python
from decouple import config
SECRET_KEY = config('SECRET_KEY', default='...')
DEBUG = config('DEBUG', default=True, cast=bool)
```

### 6. **Image Processing**
- **Pillow** - Python Imaging Library
- **Why**: Handle profile pictures and chat image uploads
- **Location**: 
  - Profile Picture: `accounts/models.py` (Line 35)
  - Chat Attachments: `accounts/models.py` (Line 110)
- **Code**:
```python
profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)
```

### 7. **Frontend Framework**
- **Bootstrap 5.3** - CSS framework
- **Why**: Responsive design, pre-built components
- **Location**: `templates/base.html` (Line 8)
- **Custom CSS**: `static/css/global-styles.css` (1000+ lines)

### 8. **Deployment**
- **Gunicorn** - WSGI HTTP Server
- **Render** - Cloud platform
- **Location**: `build.sh` (Line 1-7)

---

## 🎯 Key Features Implementation

### 1. **Chat Feature** 💬

#### Tools & Technologies:
- **AJAX Polling** - Check for new messages every 2 seconds
- **JSON API** - Send/receive messages
- **FileField** - Upload images and PDFs
- **JavaScript** - Real-time UI updates

#### Implementation Files:
1. **Backend API** - `accounts/views.py` (Line 380-520)
   - `get_chat_users()` - Line 380
   - `get_messages()` - Line 400
   - `send_message()` - Line 430
   - `check_new_messages()` - Line 480

2. **Database Model** - `accounts/models.py` (Line 105-135)
```python
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField(blank=True)
    attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)
    attachment_name = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

3. **Frontend** - `templates/chat/chat.html` (Line 1-500)
   - User list with unread badges - Line 50-100
   - Message bubbles - Line 150-250
   - File upload - Line 300-350
   - Polling logic - Line 400-450

#### How It Works:
1. Employee/Manager opens chat
2. JavaScript calls `/chat/users/` API to get contact list
3. Click on user → calls `/chat/messages/<user_id>/` to load history
4. Send message → AJAX POST to `/chat/send/`
5. Every 2 seconds → calls `/chat/check/<user_id>/` for new messages
6. New messages appear automatically without refresh

---

### 2. **File Upload (Images & PDFs)** 📎

#### For Chat Attachments:
**Location**: `accounts/views.py` (Line 430-475)

**Code**:
```python
def send_message(request):
    if request.content_type and 'multipart/form-data' in request.content_type:
        attachment = request.FILES.get('attachment')
        
    msg = ChatMessage.objects.create(
        sender=request.user,
        receiver=receiver,
        message=message_text,
        attachment=attachment,
        attachment_name=attachment.name if attachment else ''
    )
```

**Frontend**: `templates/chat/chat.html` (Line 300-350)
```javascript
const formData = new FormData();
formData.append('receiver_id', currentUserId);
formData.append('message', messageText);
formData.append('attachment', fileInput.files[0]);

fetch('/chat/send/', {
    method: 'POST',
    body: formData
})
```

**File Type Detection**: `accounts/models.py` (Line 125-135)
```python
@property
def is_image(self):
    if self.attachment:
        ext = self.attachment.name.lower().split('.')[-1]
        return ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']
    return False

@property
def is_pdf(self):
    if self.attachment:
        return self.attachment.name.lower().endswith('.pdf')
    return False
```

#### For Profile Pictures:
**Location**: `accounts/views.py` (Line 280-320)

**Code**:
```python
def profile(request):
    if 'profile_picture' in request.FILES:
        user.profile_picture = request.FILES['profile_picture']
    user.save()
```

**Model**: `accounts/models.py` (Line 35)
```python
profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
```

**Settings**: `config/settings.py` (Line 85-87)
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

### 3. **Leave Management** 📝

#### Auto-Calculate Days:
**Location**: `templates/leaves/request_leave.html` (Line 180-210)

**JavaScript Code**:
```javascript
function calculateDuration() {
    const start = new Date(startDate.value);
    const end = new Date(endDate.value);
    const diffTime = end - start;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
    totalDaysInput.value = diffDays;
}
```

#### Approval Workflow:
**Location**: `accounts/views.py` (Line 160-200)

**Code**:
```python
def approve_leave(request, leave_id):
    if request.user.role != 'manager':
        messages.error(request, 'Only managers can approve')
        return redirect('manager_dashboard')
    
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    
    if action == 'approve':
        leave_request.status = 'approved'
        leave_request.approved_by = request.user
        leave_request.save()
        
        # Update leave balance
        balance = LeaveBalance.objects.get(
            employee=leave_request.employee,
            leave_type=leave_request.leave_type
        )
        balance.used_days += leave_request.total_days
        balance.save()
```

---

### 4. **Role-Based Access Control** 🔐

**Location**: `accounts/views.py` (Line 20-80)

**Decorator Pattern**:
```python
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('account_login')
    # Admin-only code
```

**Database Model**: `accounts/models.py` (Line 23-28)
```python
ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('employee', 'Employee'),
]
role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
```

---

## 🔧 Complex Code Implementations

### 1. **Custom User Model**
**Location**: `accounts/models.py` (Line 8-50)

**Why Complex**: Extends Django's AbstractBaseUser, custom authentication

**Code**:
```python
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    
    USERNAME_FIELD = 'email'  # Login with email instead of username
    
    objects = UserManager()  # Custom manager
```

### 2. **Self-Referencing Foreign Key**
**Location**: `accounts/models.py` (Line 34)

**Why Complex**: User can be manager of other users

**Code**:
```python
manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members')
```

### 3. **Chat Polling with AJAX**
**Location**: `templates/chat/chat.html` (Line 400-450)

**Why Complex**: Real-time updates without WebSockets

**Code**:
```javascript
let pollingInterval;
let lastMessageId = 0;

function startPolling() {
    pollingInterval = setInterval(() => {
        fetch(`/chat/check/${currentUserId}/?last_id=${lastMessageId}`)
            .then(response => response.json())
            .then(data => {
                if (data.messages.length > 0) {
                    data.messages.forEach(msg => {
                        appendMessage(msg);
                        lastMessageId = msg.id;
                    });
                }
            });
    }, 2000);  // Check every 2 seconds
}
```

### 4. **Dynamic Form Field (Manager Selection)**
**Location**: `templates/account/signup.html` (Line 410-430)

**Why Complex**: Show/hide field based on role selection

**Code**:
```javascript
function toggleManagerField() {
    const role = document.getElementById('signupRole').value;
    const managerField = document.getElementById('managerField');
    
    if (role === 'employee') {
        managerField.style.display = 'block';
        managerSelect.required = true;
    } else {
        managerField.style.display = 'none';
        managerSelect.required = false;
    }
}
```

### 5. **Management Commands**
**Location**: `accounts/management/commands/create_leave_types.py`

**Why Complex**: Custom Django commands for automation

**Code**:
```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create default leave types'
    
    def handle(self, *args, **kwargs):
        leave_types = [
            {'name': 'Casual Leave', 'default_days': 12},
            {'name': 'Sick Leave', 'default_days': 10},
        ]
        
        for lt in leave_types:
            LeaveType.objects.get_or_create(name=lt['name'], defaults=lt)
```

**Run**: `python manage.py create_leave_types`

### 6. **Database Query Optimization**
**Location**: `accounts/views.py` (Line 400-420)

**Why Complex**: Efficient queries with filters and ordering

**Code**:
```python
messages = ChatMessage.objects.filter(
    sender__in=[request.user, other_user],
    receiver__in=[request.user, other_user]
).order_by('created_at')

# Mark as read in single query
ChatMessage.objects.filter(
    sender=other_user, 
    receiver=request.user, 
    is_read=False
).update(is_read=True)
```

---

## 📂 Project Structure

```
LeaveFlow/
├── accounts/                    # Main app
│   ├── models.py               # Database models (Line 1-135)
│   ├── views.py                # Business logic (Line 1-520)
│   ├── forms.py                # Form handling (Line 1-70)
│   ├── urls.py                 # URL routing (Line 1-30)
│   ├── adapters.py             # Custom allauth adapter (Line 1-20)
│   └── management/commands/    # Custom commands
│       ├── create_leave_types.py
│       └── create_admin.py
│
├── config/                      # Project settings
│   ├── settings.py             # Main configuration (Line 1-120)
│   ├── urls.py                 # Root URLs (Line 1-15)
│   └── wsgi.py                 # WSGI config (Line 1-16)
│
├── templates/                   # HTML templates
│   ├── base.html               # Base template with sidebar (Line 1-300)
│   ├── account/
│   │   ├── login.html          # Login page (Line 1-250)
│   │   └── signup.html         # Signup page (Line 1-400)
│   ├── dashboards/
│   │   ├── admin_dashboard.html
│   │   ├── manager_dashboard.html
│   │   └── employee_dashboard.html
│   ├── leaves/
│   │   ├── request_leave.html  # Leave form (Line 1-220)
│   │   └── my_leaves.html
│   └── chat/
│       └── chat.html           # Chat interface (Line 1-500)
│
├── static/css/
│   └── global-styles.css       # Custom styles (Line 1-1000+)
│
├── media/                       # Uploaded files
│   ├── profiles/               # Profile pictures
│   └── chat_attachments/       # Chat files
│
├── requirements.txt            # Python dependencies
├── build.sh                    # Deployment script
├── .env                        # Environment variables
└── manage.py                   # Django CLI
```

---

## 🔑 Key Concepts

### 1. **ORM (Object-Relational Mapping)**
- Django ORM converts Python code to SQL
- Example: `User.objects.filter(role='manager')` → `SELECT * FROM users WHERE role='manager'`

### 2. **MVC Pattern (Model-View-Template)**
- **Model**: Database structure (`models.py`)
- **View**: Business logic (`views.py`)
- **Template**: HTML presentation (`templates/`)

### 3. **CSRF Protection**
- `{% csrf_token %}` in all forms
- Prevents Cross-Site Request Forgery attacks

### 4. **Middleware**
- Code that runs before/after each request
- Example: WhiteNoise, Authentication, CSRF

### 5. **Migrations**
- Track database schema changes
- Files in `accounts/migrations/`

---

## 🚀 Deployment Process

1. **Build Script** (`build.sh`):
```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_leave_types
python manage.py create_admin
```

2. **Environment Variables** (Render):
- `SECRET_KEY` - Django secret
- `DEBUG=False` - Production mode
- `DATABASE_URL` - PostgreSQL connection
- `ALLOWED_HOSTS` - Domain whitelist

3. **Static Files**:
- Collected to `staticfiles/` folder
- Served by WhiteNoise in production

---

## 📊 Database Schema

### Users Table
- email (unique)
- full_name
- role (admin/manager/employee)
- manager_id (foreign key to self)
- profile_picture

### Leave Types Table
- name
- description
- default_days

### Leave Requests Table
- employee_id (foreign key)
- leave_type_id (foreign key)
- start_date
- end_date
- total_days
- reason
- status (pending/approved/rejected)
- approved_by_id (foreign key)

### Chat Messages Table
- sender_id (foreign key)
- receiver_id (foreign key)
- message (text)
- attachment (file)
- is_read (boolean)
- created_at (timestamp)

---

## 🎓 Learning Points

1. **Django Framework** - Full-stack web development
2. **Database Design** - Relationships, foreign keys
3. **REST APIs** - JSON endpoints for AJAX
4. **File Handling** - Upload, storage, validation
5. **Authentication** - Custom user model, permissions
6. **Frontend** - Bootstrap, JavaScript, AJAX
7. **Deployment** - Production configuration, environment variables
8. **Version Control** - Git, GitHub

---

**Project Completion Date**: December 2025
**Total Lines of Code**: ~5000+
**Development Time**: 2-3 weeks
