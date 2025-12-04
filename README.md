# 📋 LeaveFlow - Employee Leave Management System

A comprehensive, modern leave management system built with Django for efficient leave tracking, approval workflows, and real-time communication between employees and managers.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📑 Table of Contents

1. [Features](#-features)
2. [Tech Stack](#-tech-stack)
3. [Project Structure](#-project-structure)
4. [Installation & Setup](#-installation--setup)
5. [Running the Application](#-running-the-application)
6. [Testing](#-testing)
7. [Database Testing](#-database-testing)
8. [Deployment](#-deployment)
9. [File Descriptions](#-file-descriptions)
10. [API Endpoints](#-api-endpoints)
11. [User Roles](#-user-roles)
12. [Screenshots](#-screenshots)

---

## ✨ Features

### 🔐 Authentication & Authorization
- **Email-based Authentication**: No username required, login with email
- **Role-based Access Control**: Admin, Manager, Employee roles
- **Secure Password Management**: Django's PBKDF2 hashing
- **Session Management**: Remember me functionality
- **Password Visibility Toggle**: Show/hide password on login, signup, and profile pages
- **Advanced Password Validation**: 
  - Current password verification
  - New password confirmation matching
  - Old password reuse prevention

### 👥 User Management
- **Admin Panel**: Full system access, manage all users
- **User Profiles**: Update personal info, profile picture
- **Password Change**: Secure password update with multi-level verification
- **Phone Validation**: 10-digit phone number validation
- **Profile Picture Upload**: Image upload with preview

### 📝 Leave Management
- **4 Leave Types**: Casual (12 days), Sick (10 days), Earned (15 days), Emergency (5 days)
- **Leave Request**: Submit with date range, reason, manager selection
- **Auto-calculate Duration**: Automatic day calculation
- **Approval Workflow**: Manager approve/reject with one click
- **Leave Balance Tracking**: Real-time balance updates
- **Team Leave History**: Dedicated history page for managers with filtering

### 💬 Real-Time Chat
- **Employee-Manager Communication**: Direct messaging
- **Real-time Updates**: 2-second polling for new messages
- **Message History**: Persistent chat history with date separators
- **Unread Indicators**: Badge for unread messages
- **File Attachments**: Send images and PDF files
- **Image Preview**: View images directly in chat
- **PDF Support**: Download and view PDF documents
- **User Search**: Search contacts by name or email
- **Read Receipts**: Double tick for sent messages

### 🎨 Modern UI/UX
- **Sidebar Navigation**: Clean, organized menu with clickable logo
- **Dark/Light Theme**: Toggle with localStorage persistence
- **Responsive Design**: Mobile, tablet, desktop support
- **Bootstrap 5**: Modern component library
- **Glassmorphism Design**: Modern blur effects and gradients
- **Smooth Animations**: Slide-up, fade-in, shake effects
- **Advanced Form Styling**: Focus states with glow effects
- **Custom Scrollbars**: Styled scrollbars for chat and lists

---

## 🛠 Tech Stack

### Backend
| Technology | Description |
|------------|-------------|
| **Python 3.8+** | Programming language |
| **Django 4.2** | Web framework for rapid development |
| **django-allauth** | Authentication library for email login |
| **SQLite** | Lightweight database (development) |
| **python-decouple** | Environment variable management |

### Frontend
| Technology | Description |
|------------|-------------|
| **HTML5** | Markup language |
| **CSS3** | Styling with custom properties |
| **JavaScript** | Client-side interactivity |
| **Bootstrap 5.3** | CSS framework for responsive design |

### Key Libraries
| Library | Purpose |
|---------|---------|
| `django-allauth` | Handles authentication, signup, login |
| `python-decouple` | Manages environment variables from .env |
| `Pillow` | Image processing for profile pictures and chat attachments |

### Design Features
| Feature | Description |
|---------|-------------|
| Glassmorphism | Modern blur effects with semi-transparent backgrounds |
| CSS Variables | Custom properties for theming |
| Flexbox/Grid | Modern layout techniques |
| CSS Animations | Smooth transitions and keyframe animations |
| Gradient Backgrounds | Linear gradients for buttons and cards |

---

## 📁 Project Structure

```
LeaveFlow/
├── accounts/                    # Main application
│   ├── migrations/              # Database migrations
│   │   ├── 0001_initial.py     # Initial migration (User, LeaveType, etc.)
│   │   └── 0002_chatmessage.py # Chat message migration
│   ├── __init__.py             # Package initializer
│   ├── admin.py                # Django admin configuration
│   ├── adapters.py             # Custom allauth adapter
│   ├── apps.py                 # App configuration
│   ├── forms.py                # Form definitions
│   ├── models.py               # Database models
│   ├── tests.py                # Test cases
│   ├── urls.py                 # URL routing
│   └── views.py                # View functions
│
├── config/                      # Project configuration
│   ├── __init__.py             # Package initializer
│   ├── asgi.py                 # ASGI configuration
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Root URL configuration
│   └── wsgi.py                 # WSGI configuration
│
├── static/                      # Static files
│   └── css/
│       └── global-styles.css   # Custom CSS styles
│
├── templates/                   # HTML templates
│   ├── account/                # Authentication templates
│   │   ├── login.html          # Login page
│   │   └── signup.html         # Registration page
│   ├── admin/                  # Admin templates
│   │   └── all_users.html      # User management page
│   ├── chat/                   # Chat templates
│   │   └── chat.html           # Chat page
│   ├── dashboards/             # Dashboard templates
│   │   ├── admin_dashboard.html
│   │   ├── manager_dashboard.html
│   │   └── employee_dashboard.html
│   ├── leaves/                 # Leave management templates
│   │   ├── all_leaves.html     # All leaves list
│   │   ├── my_leaves.html      # User's leaves
│   │   ├── request_leave.html  # Leave request form
│   │   └── team_history.html   # Manager's team leave history
│   └── base.html               # Base template with sidebar
│
├── .env                        # Environment variables
├── .gitignore                  # Git ignore rules
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management script
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone/Download Project
```bash
# Clone repository
git clone <repository-url>
cd LeaveFlow

# OR download and extract ZIP
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment (Optional)
Create `.env` file in project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 5: Run Migrations
```bash
python manage.py migrate
```

### Step 6: Create Leave Types
```bash
python manage.py shell -c "
from accounts.models import LeaveType
LeaveType.objects.get_or_create(name='Casual Leave', defaults={'description': 'Short-term personal leave', 'default_days': 12})
LeaveType.objects.get_or_create(name='Sick Leave', defaults={'description': 'Medical or health-related leave', 'default_days': 10})
LeaveType.objects.get_or_create(name='Earned Leave', defaults={'description': 'Annual vacation leave', 'default_days': 15})
LeaveType.objects.get_or_create(name='Emergency Leave', defaults={'description': 'Urgent unforeseen circumstances', 'default_days': 5})
print('Leave types created!')
"
```

### Step 7: Create Site Object
```bash
python manage.py shell -c "
from django.contrib.sites.models import Site
Site.objects.get_or_create(id=1, defaults={'domain': 'localhost:8000', 'name': 'LeaveFlow'})
print('Site created!')
"
```

### Step 8: Create Admin User
```bash
python manage.py createsuperuser
# Enter email, password when prompted
```

---

## ▶️ Running the Application

### Development Server
```bash
python manage.py runserver
```
Visit: http://127.0.0.1:8000/

### Create Test Users
```bash
python manage.py shell -c "
from accounts.models import User

# Create Manager
manager = User.objects.create_user(
    email='manager@company.com',
    password='manager123',
    full_name='John Manager',
    role='manager'
)

# Create Employee
User.objects.create_user(
    email='employee@company.com',
    password='employee123',
    full_name='Jane Employee',
    role='employee',
    manager=manager
)
print('Test users created!')
"
```

### Test Credentials
| Role | Email | Password |
|------|-------|----------|
| Admin | (your email) | (your password) |
| Manager | manager@company.com | manager123 |
| Employee | employee@company.com | employee123 |

---

## 🧪 Testing

### Run All Tests
```bash
python manage.py test accounts
```

### Run Specific Test Class
```bash
# Test User Model
python manage.py test accounts.tests.UserModelTests

# Test Leave Request Model
python manage.py test accounts.tests.LeaveRequestModelTests

# Test Authentication Views
python manage.py test accounts.tests.AuthenticationViewTests

# Test Dashboard Views
python manage.py test accounts.tests.DashboardViewTests

# Test Chat Views
python manage.py test accounts.tests.ChatViewTests
```

### Run with Verbosity
```bash
python manage.py test accounts -v 2
```

### Test Coverage (Optional)
```bash
pip install coverage
coverage run manage.py test accounts
coverage report
coverage html  # Generate HTML report
```

### Test Categories

| Test Class | Description |
|------------|-------------|
| `UserModelTests` | User creation, roles, manager assignment |
| `LeaveTypeModelTests` | Leave type creation and properties |
| `LeaveRequestModelTests` | Leave request CRUD, approval/rejection |
| `LeaveBalanceModelTests` | Balance calculation, updates |
| `ChatMessageModelTests` | Message creation, read status |
| `AuthenticationViewTests` | Login, signup page loading |
| `DashboardViewTests` | Dashboard access by role |
| `LeaveRequestViewTests` | Leave request pages |
| `ChatViewTests` | Chat functionality |
| `DatabaseIntegrityTests` | Cascade delete, unique constraints |

---

## 🗄️ Database Testing

### Access Django Shell
```bash
python manage.py shell
```

### Test User Operations
```python
from accounts.models import User

# Create user
user = User.objects.create_user(
    email='test@example.com',
    password='testpass123',
    full_name='Test User',
    role='employee'
)

# Query users
all_users = User.objects.all()
employees = User.objects.filter(role='employee')
managers = User.objects.filter(role='manager')

# Check password
user.check_password('testpass123')  # Returns True

# Update user
user.full_name = 'Updated Name'
user.save()

# Delete user
user.delete()
```

### Test Leave Operations
```python
from accounts.models import User, LeaveType, LeaveRequest, LeaveBalance
from datetime import date, timedelta

# Get leave types
leave_types = LeaveType.objects.all()

# Create leave request
employee = User.objects.get(email='employee@company.com')
leave_type = LeaveType.objects.get(name='Casual Leave')

leave = LeaveRequest.objects.create(
    employee=employee,
    leave_type=leave_type,
    start_date=date.today(),
    end_date=date.today() + timedelta(days=2),
    total_days=3,
    reason='Personal work'
)

# Approve leave
leave.status = 'approved'
leave.save()

# Check leave balance
balance = LeaveBalance.objects.get(employee=employee, leave_type=leave_type)
print(f"Remaining: {balance.remaining_days}")
```

### Test Chat Operations
```python
from accounts.models import User, ChatMessage

sender = User.objects.get(email='employee@company.com')
receiver = User.objects.get(email='manager@company.com')

# Send message
msg = ChatMessage.objects.create(
    sender=sender,
    receiver=receiver,
    message='Hello, I need to discuss my leave.'
)

# Get conversation
messages = ChatMessage.objects.filter(
    sender__in=[sender, receiver],
    receiver__in=[sender, receiver]
).order_by('created_at')

# Mark as read
msg.is_read = True
msg.save()
```

### Database Queries
```python
# Count users by role
from django.db.models import Count
User.objects.values('role').annotate(count=Count('id'))

# Pending leave requests
LeaveRequest.objects.filter(status='pending').count()

# Leaves this month
from django.utils import timezone
LeaveRequest.objects.filter(
    created_at__month=timezone.now().month
).count()
```

---

## 🚀 Deployment

### Option 1: Railway (Recommended)

1. **Create Railway Account**: https://railway.app
2. **Connect GitHub Repository**
3. **Add Environment Variables**:
   ```
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app.railway.app
   ```
4. **Deploy**

### Option 2: Heroku

1. **Install Heroku CLI**
2. **Create Procfile**:
   ```
   web: gunicorn config.wsgi
   ```
3. **Add to requirements.txt**:
   ```
   gunicorn==21.2.0
   whitenoise==6.6.0
   ```
4. **Update settings.py**:
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware',
       ...
   ]
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   ```
5. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku run python manage.py migrate
   ```

### Option 3: VPS (DigitalOcean, AWS EC2)

1. **Install Dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

2. **Clone Project**:
   ```bash
   git clone <repository-url>
   cd LeaveFlow
   ```

3. **Setup Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

4. **Configure Gunicorn**:
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```

5. **Configure Nginx**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location /static/ {
           alias /path/to/LeaveFlow/staticfiles/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Setup PostgreSQL database
- [ ] Configure static files (WhiteNoise/S3)
- [ ] Enable HTTPS
- [ ] Setup email backend

---

## 📄 File Descriptions

### Core Files

| File | Description |
|------|-------------|
| `manage.py` | Django's command-line utility for administrative tasks |
| `requirements.txt` | List of Python packages required |
| `.env` | Environment variables (SECRET_KEY, DEBUG, etc.) |
| `db.sqlite3` | SQLite database file |

### Config Directory

| File | Description |
|------|-------------|
| `settings.py` | Django settings (database, apps, middleware, auth) |
| `urls.py` | Root URL configuration, includes app URLs |
| `wsgi.py` | WSGI entry point for production servers |
| `asgi.py` | ASGI entry point for async servers |

### Accounts App

| File | Description |
|------|-------------|
| `models.py` | Database models (User, LeaveType, LeaveRequest, LeaveBalance, ChatMessage) |
| `views.py` | View functions for all pages and API endpoints |
| `forms.py` | Form classes (CustomSignupForm, LeaveRequestForm, ProfileUpdateForm) |
| `urls.py` | App URL patterns |
| `admin.py` | Django admin customization |
| `adapters.py` | Custom allauth adapter for email login and redirects |
| `tests.py` | Test cases for models and views |

### Templates

| Template | Description |
|----------|-------------|
| `base.html` | Base template with sidebar, navbar, profile modal |
| `login.html` | Login page with password visibility toggle |
| `signup.html` | Registration page with role selection |
| `*_dashboard.html` | Role-specific dashboard pages |
| `request_leave.html` | Leave request form with auto-calculate |
| `chat.html` | Real-time chat interface |
| `all_users.html` | Admin user management with delete |

---

## 🔗 API Endpoints

### Authentication
| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | `/accounts/login/` | Login page |
| GET/POST | `/accounts/signup/` | Registration page |
| GET | `/logout/` | Logout user |

### Dashboards
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/dashboard/admin/` | Admin dashboard |
| GET | `/dashboard/manager/` | Manager dashboard |
| GET | `/dashboard/employee/` | Employee dashboard |

### Leave Management
| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | `/leaves/request/` | Request leave |
| GET | `/leaves/my-leaves/` | User's leaves |
| GET | `/leaves/all/` | All leaves (admin/manager) |
| POST | `/leaves/approve/<id>/` | Approve/reject leave |
| POST | `/leaves/cancel/<id>/` | Cancel leave request |

### Chat API
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/chat/` | Chat page |
| GET | `/chat/users/` | Get available chat users |
| GET | `/chat/messages/<user_id>/` | Get messages with user |
| POST | `/chat/send/` | Send message (text or file attachment) |
| GET | `/chat/check/<user_id>/` | Check new messages |

### Leave History
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/leaves/history/` | Team leave history (manager only) |

### User Management
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/dashboard/users/` | All users (admin) |
| POST | `/users/delete/<id>/` | Delete user |
| POST | `/profile/` | Update profile |

---

## 👥 User Roles

### Admin
- Full system access
- View all users and leaves
- Delete users
- Access Django admin panel

### Manager
- View team members
- Approve/reject leave requests
- Chat with team employees
- View team leave history

### Employee
- Request leaves
- View own leave balance
- Chat with managers
- Track leave status

---

## 📸 Screenshots

### Login Page
- Clean, modern design
- Password visibility toggle
- Error messages with auto-hide

### Dashboard
- Sidebar navigation
- Stats cards
- Recent activity

### Leave Request
- Date picker
- Auto-calculate days
- Manager selection

### Chat
- Real-time messaging
- User list with unread badges
- Message bubbles

---

## 🔒 Security Features

- CSRF protection on all forms
- Password hashing (PBKDF2)
- Session security (HttpOnly cookies)
- XSS protection headers
- SQL injection prevention (Django ORM)
- Role-based access control
- Password change validation (current password verification)
- Old password reuse prevention
- File upload validation for chat attachments

---

## 🆕 Recent Updates

### Chat Enhancements
- Added file attachment support (images and PDFs)
- Image preview in chat messages
- PDF download links
- User search functionality
- Date separators in message history
- Read receipts (double tick icons)
- Modern glassmorphism design

### Leave Management
- Added dedicated Team History page for managers
- History link in sidebar navigation
- Status filtering on history page

### Authentication & Profile
- Advanced password validation
- Password visibility toggle on all password fields
- Old password reuse prevention
- Improved error messages

### UI/UX Improvements
- Redesigned login and signup pages
- Centered button text with icons
- Smooth animations and transitions
- Better focus states on inputs
- Clickable logo redirects to dashboard
- Modern gradient backgrounds

---

## 📝 License

MIT License - feel free to use this project for learning or commercial purposes.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📧 Support

For issues or questions, please open a GitHub issue.

---

Built with ❤️ using Django and Bootstrap
