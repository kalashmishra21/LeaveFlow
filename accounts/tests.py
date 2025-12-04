"""
LeaveFlow Test Suite
====================
This file contains all test cases for the LeaveFlow application.
Run tests with: python manage.py test accounts
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import LeaveType, LeaveRequest, LeaveBalance, ChatMessage
from datetime import date, timedelta

User = get_user_model()


class UserModelTests(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        """Set up test data"""
        self.admin = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            full_name='Test Admin',
            role='admin'
        )
        self.manager = User.objects.create_user(
            email='manager@test.com',
            password='testpass123',
            full_name='Test Manager',
            role='manager'
        )
        self.employee = User.objects.create_user(
            email='employee@test.com',
            password='testpass123',
            full_name='Test Employee',
            role='employee',
            manager=self.manager
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.employee.email, 'employee@test.com')
        self.assertEqual(self.employee.role, 'employee')
        self.assertTrue(self.employee.check_password('testpass123'))
    
    def test_user_str_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.employee), 'employee@test.com')
    
    def test_superuser_creation(self):
        """Test superuser creation"""
        superuser = User.objects.create_superuser(
            email='super@test.com',
            password='superpass123'
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.role, 'admin')
    
    def test_manager_assignment(self):
        """Test manager is assigned to employee"""
        self.assertEqual(self.employee.manager, self.manager)
    
    def test_user_roles(self):
        """Test different user roles"""
        self.assertEqual(self.admin.role, 'admin')
        self.assertEqual(self.manager.role, 'manager')
        self.assertEqual(self.employee.role, 'employee')


class LeaveTypeModelTests(TestCase):
    """Test cases for LeaveType model"""
    
    def setUp(self):
        self.leave_type = LeaveType.objects.create(
            name='Casual Leave',
            description='Short-term personal leave',
            default_days=12
        )
    
    def test_leave_type_creation(self):
        """Test leave type is created correctly"""
        self.assertEqual(self.leave_type.name, 'Casual Leave')
        self.assertEqual(self.leave_type.default_days, 12)
    
    def test_leave_type_str(self):
        """Test leave type string representation"""
        self.assertEqual(str(self.leave_type), 'Casual Leave')


class LeaveRequestModelTests(TestCase):
    """Test cases for LeaveRequest model"""
    
    def setUp(self):
        self.manager = User.objects.create_user(
            email='manager@test.com',
            password='testpass123',
            role='manager'
        )
        self.employee = User.objects.create_user(
            email='employee@test.com',
            password='testpass123',
            role='employee',
            manager=self.manager
        )
        self.leave_type = LeaveType.objects.create(
            name='Sick Leave',
            default_days=10
        )
        self.leave_request = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type=self.leave_type,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            total_days=3,
            reason='Not feeling well',
            status='pending'
        )
    
    def test_leave_request_creation(self):
        """Test leave request is created correctly"""
        self.assertEqual(self.leave_request.employee, self.employee)
        self.assertEqual(self.leave_request.status, 'pending')
        self.assertEqual(self.leave_request.total_days, 3)
    
    def test_leave_request_approval(self):
        """Test leave request approval"""
        self.leave_request.status = 'approved'
        self.leave_request.approved_by = self.manager
        self.leave_request.save()
        self.assertEqual(self.leave_request.status, 'approved')
        self.assertEqual(self.leave_request.approved_by, self.manager)
    
    def test_leave_request_rejection(self):
        """Test leave request rejection"""
        self.leave_request.status = 'rejected'
        self.leave_request.save()
        self.assertEqual(self.leave_request.status, 'rejected')


class LeaveBalanceModelTests(TestCase):
    """Test cases for LeaveBalance model"""
    
    def setUp(self):
        self.employee = User.objects.create_user(
            email='employee@test.com',
            password='testpass123',
            role='employee'
        )
        self.leave_type = LeaveType.objects.create(
            name='Casual Leave',
            default_days=12
        )
        self.balance = LeaveBalance.objects.create(
            employee=self.employee,
            leave_type=self.leave_type,
            year=2025,
            total_days=12,
            used_days=3
        )
    
    def test_remaining_days_calculation(self):
        """Test remaining days property"""
        self.assertEqual(self.balance.remaining_days, 9)
    
    def test_balance_update(self):
        """Test balance update after leave approval"""
        self.balance.used_days = 5
        self.balance.save()
        self.assertEqual(self.balance.remaining_days, 7)


class ChatMessageModelTests(TestCase):
    """Test cases for ChatMessage model"""
    
    def setUp(self):
        self.manager = User.objects.create_user(
            email='manager@test.com',
            password='testpass123',
            role='manager'
        )
        self.employee = User.objects.create_user(
            email='employee@test.com',
            password='testpass123',
            role='employee'
        )
        self.message = ChatMessage.objects.create(
            sender=self.employee,
            receiver=self.manager,
            message='Hello, I need to discuss my leave request.'
        )
    
    def test_message_creation(self):
        """Test chat message is created correctly"""
        self.assertEqual(self.message.sender, self.employee)
        self.assertEqual(self.message.receiver, self.manager)
        self.assertFalse(self.message.is_read)
    
    def test_message_read_status(self):
        """Test message read status update"""
        self.message.is_read = True
        self.message.save()
        self.assertTrue(self.message.is_read)


class AuthenticationViewTests(TestCase):
    """Test cases for authentication views"""
    
    def setUp(self):
        self.client = Client()
        self.employee = User.objects.create_user(
            email='employee@test.com',
            password='testpass123',
            full_name='Test Employee',
            role='employee'
        )
    
    def test_login_page_loads(self):
        """Test login page loads correctly"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_signup_page_loads(self):
        """Test signup page loads correctly"""
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
    
    def test_employee_login_redirect(self):
        """Test employee login redirects to employee dashboard"""
        self.client.login(username='employee@test.com', password='testpass123')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)


class DashboardViewTests(TestCase):
    """Test cases for dashboard views"""
    
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            role='admin',
            is_staff=True
        )
        self.manager = User.objects.create_user(
            email='manager@test.com',
            password='testpass123',
            role='manager'
        )
        self.employee = User.objects.create_user(
            email='employee@test.com',
            password='testpass123',
            role='employee',
            manager=self.manager
        )
    
    def test_admin_dashboard_access(self):
        """Test admin can access admin dashboard"""
        self.client.login(username='admin@test.com', password='testpass123')
        response = self.client.get('/dashboard/admin/')
        self.assertEqual(response.status_code, 200)
    
    def test_manager_dashboard_access(self):
        """Test manager can access manager dashboard"""
        self.client.login(username='manager@test.com', password='testpass123')
        response = self.client.get('/dashboard/manager/')
        self.assertEqual(response.status_code, 200)
    
    def test_employee_dashboard_access(self):
        """Test employee can access employee dashboard"""
        self.client.login(username='employee@test.com', password='testpass123')
        response = self.client.get('/dashboard/employee/')
        self.assertEqual(response.status_code, 200)
    
    def test_unauthorized_dashboard_access(self):
        """Test unauthorized access is denied"""
        self.client.login(username='employee@test.com', password='testpass123')
        response = self.client.get('/dashboard/admin/')
        self.assertEqual(response.status_code, 302)  # Redirect


class LeaveRequestViewTests(TestCase):
    """Test cases for leave request views"""
    
    def setUp(self):
        self.client = Client()
        self.manager = User.objects.create_user(
            email='manager@test.com',
            password='testpass123',
            role='manager'
        )
        self.employee = User.objects.create_user(
            email='employee@test.com',
            password='testpass123',
            role='employee',
            manager=self.manager
        )
        self.leave_type = LeaveType.objects.create(
            name='Casual Leave',
            default_days=12
        )
    
    def test_request_leave_page_loads(self):
        """Test request leave page loads for employee"""
        self.client.login(username='employee@test.com', password='testpass123')
        response = self.client.get('/leaves/request/')
        self.assertEqual(response.status_code, 200)
    
    def test_my_leaves_page_loads(self):
        """Test my leaves page loads"""
        self.client.login(username='employee@test.com', password='testpass123')
        response = self.client.get('/leaves/my-leaves/')
        self.assertEqual(response.status_code, 200)


class ChatViewTests(TestCase):
    """Test cases for chat views"""
    
    def setUp(self):
        self.client = Client()
        self.manager = User.objects.create_user(
            email='manager@test.com',
            password='testpass123',
            role='manager'
        )
        self.employee = User.objects.create_user(
            email='employee@test.com',
            password='testpass123',
            role='employee',
            manager=self.manager
        )
    
    def test_chat_page_loads(self):
        """Test chat page loads"""
        self.client.login(username='employee@test.com', password='testpass123')
        response = self.client.get('/chat/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_chat_users(self):
        """Test get chat users API"""
        self.client.login(username='employee@test.com', password='testpass123')
        response = self.client.get('/chat/users/')
        self.assertEqual(response.status_code, 200)


class DatabaseIntegrityTests(TestCase):
    """Test cases for database integrity"""
    
    def test_cascade_delete_user_leaves(self):
        """Test leave requests are deleted when user is deleted"""
        manager = User.objects.create_user(
            email='manager@test.com',
            password='testpass123',
            role='manager'
        )
        employee = User.objects.create_user(
            email='employee@test.com',
            password='testpass123',
            role='employee'
        )
        leave_type = LeaveType.objects.create(name='Test Leave', default_days=5)
        LeaveRequest.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date=date.today(),
            end_date=date.today(),
            total_days=1,
            reason='Test'
        )
        
        employee_id = employee.id
        employee.delete()
        
        # Verify leave requests are deleted
        self.assertEqual(LeaveRequest.objects.filter(employee_id=employee_id).count(), 0)
    
    def test_unique_email_constraint(self):
        """Test unique email constraint"""
        User.objects.create_user(
            email='unique@test.com',
            password='testpass123'
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='unique@test.com',
                password='testpass456'
            )
    
    def test_leave_balance_unique_constraint(self):
        """Test unique constraint on leave balance"""
        employee = User.objects.create_user(
            email='employee@test.com',
            password='testpass123',
            role='employee'
        )
        leave_type = LeaveType.objects.create(name='Test Leave', default_days=5)
        
        LeaveBalance.objects.create(
            employee=employee,
            leave_type=leave_type,
            year=2025,
            total_days=10,
            used_days=0
        )
        
        with self.assertRaises(Exception):
            LeaveBalance.objects.create(
                employee=employee,
                leave_type=leave_type,
                year=2025,
                total_days=10,
                used_days=0
            )
