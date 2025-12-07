from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .forms import LeaveRequestForm, ProfileUpdateForm
from .models import User, LeaveRequest, LeaveBalance, LeaveType, ChatMessage


def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'manager':
            return redirect('manager_dashboard')
        else:
            return redirect('employee_dashboard')
    return redirect('account_login')





@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('account_login')
    
    total_users = User.objects.count()
    total_employees = User.objects.filter(role='employee').count()
    total_managers = User.objects.filter(role='manager').count()
    pending_leaves = LeaveRequest.objects.filter(status='pending').count()
    
    recent_leaves = LeaveRequest.objects.all()[:10]
    recent_users = User.objects.all()[:5]
    
    context = {
        'total_users': total_users,
        'total_employees': total_employees,
        'total_managers': total_managers,
        'pending_leaves': pending_leaves,
        'recent_leaves': recent_leaves,
        'recent_users': recent_users,
    }
    return render(request, 'dashboards/admin_dashboard.html', context)


@login_required
def manager_dashboard(request):
    if request.user.role != 'manager':
        messages.error(request, 'Access denied. Manager only.')
        return redirect('account_login')
    
    team_members = User.objects.filter(manager=request.user)
    pending_leaves = LeaveRequest.objects.filter(
        employee__manager=request.user,
        status='pending'
    )
    
    team_leaves = LeaveRequest.objects.filter(
        employee__manager=request.user
    )[:10]
    
    context = {
        'team_members': team_members,
        'pending_leaves': pending_leaves,
        'team_leaves': team_leaves,
        'pending_count': pending_leaves.count(),
        'team_count': team_members.count(),
    }
    return render(request, 'dashboards/manager_dashboard.html', context)


@login_required
def employee_dashboard(request):
    if request.user.role != 'employee':
        messages.error(request, 'Access denied. Employee only.')
        return redirect('home')
    
    my_leaves = LeaveRequest.objects.filter(employee=request.user)
    leave_balances = LeaveBalance.objects.filter(
        employee=request.user,
        year=timezone.now().year
    )
    
    for balance in leave_balances:
        if balance.total_days > 0:
            balance.percentage = int((balance.remaining_days / balance.total_days) * 100)
        else:
            balance.percentage = 0
    
    pending_count = my_leaves.filter(status='pending').count()
    approved_count = my_leaves.filter(status='approved').count()
    
    context = {
        'my_leaves': my_leaves[:10],
        'leave_balances': leave_balances,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'total_requests': my_leaves.count(),
    }
    return render(request, 'dashboards/employee_dashboard.html', context)


@login_required
def request_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            
            manager = form.cleaned_data.get('manager')
            if manager:
                request.user.manager = manager
                request.user.save()
            
            leave_request.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('employee_dashboard')
    else:
        form = LeaveRequestForm()
    
    return render(request, 'leaves/request_leave.html', {'form': form})


@login_required
def my_leaves(request):
    leaves = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'leaves/my_leaves.html', {'leaves': leaves})


@login_required
def all_leaves(request):
    if request.user.role not in ['admin', 'manager']:
        messages.error(request, 'Access denied.')
        return redirect('account_login')
    
    status_filter = request.GET.get('status', '')
    
    if request.user.role == 'admin':
        leaves = LeaveRequest.objects.all()
    else:
        leaves = LeaveRequest.objects.filter(employee__manager=request.user)
    
    if status_filter:
        leaves = leaves.filter(status=status_filter)
    
    leaves = leaves.order_by('-created_at')
    
    context = {
        'leaves': leaves,
        'status_filter': status_filter,
    }
    return render(request, 'leaves/all_leaves.html', context)


@login_required
def approve_leave(request, leave_id):
    # Only managers can approve/reject leaves, not admin
    if request.user.role != 'manager':
        messages.error(request, 'Only managers can approve or reject leave requests.')
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        return redirect('account_login')
    
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    
    # Verify the leave request is from manager's team
    if leave_request.employee.manager != request.user:
        messages.error(request, 'You can only approve leaves from your team members.')
        return redirect('manager_dashboard')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            leave_request.status = 'approved'
            leave_request.approved_by = request.user
            leave_request.save()
            messages.success(request, f'Leave request approved for {leave_request.employee.full_name}')
            
            try:
                balance = LeaveBalance.objects.get(
                    employee=leave_request.employee,
                    leave_type=leave_request.leave_type,
                    year=timezone.now().year
                )
                balance.used_days += leave_request.total_days
                balance.save()
            except LeaveBalance.DoesNotExist:
                pass
        
        elif action == 'reject':
            leave_request.status = 'rejected'
            leave_request.approved_by = request.user
            leave_request.save()
            messages.success(request, f'Leave request rejected for {leave_request.employee.full_name}')
        
        return redirect('manager_dashboard')
    
    return redirect('manager_dashboard')


@login_required
def cancel_leave(request, leave_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_id, employee=request.user)
    
    if leave_request.status == 'pending':
        leave_request.delete()
        messages.success(request, 'Leave request cancelled and removed!')
    else:
        messages.error(request, 'Only pending requests can be cancelled.')
    
    return redirect('my_leaves')


@login_required
def team_history(request):
    if request.user.role != 'manager':
        messages.error(request, 'Access denied. Manager only.')
        return redirect('account_login')
    
    status_filter = request.GET.get('status', '')
    
    team_leaves = LeaveRequest.objects.filter(
        employee__manager=request.user
    ).order_by('-created_at')
    
    if status_filter:
        team_leaves = team_leaves.filter(status=status_filter)
    
    context = {
        'team_leaves': team_leaves,
        'status_filter': status_filter,
    }
    return render(request, 'leaves/team_history.html', context)


@login_required
def all_users(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('account_login')
    
    users = User.objects.all()
    return render(request, 'admin/all_users.html', {'users': users})


@login_required
def custom_logout(request):
    logout(request)
    return redirect('account_login')


@login_required
def profile(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        # Check if any password field is filled (password change attempt)
        password_fields_filled = current_password or new_password or confirm_password
        
        if password_fields_filled:
            # This is a password change request - validate all fields
            if not current_password:
                messages.error(request, 'Please enter your current password!')
            elif not new_password:
                messages.error(request, 'Please enter a new password!')
            elif not confirm_password:
                messages.error(request, 'Please confirm your new password!')
            elif not request.user.check_password(current_password):
                messages.error(request, 'Current password is incorrect!')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match!')
            elif request.user.check_password(new_password):
                messages.error(request, 'Do not use your old password! Please choose a different password.')
            else:
                # All validations passed, update password
                request.user.set_password(new_password)
                request.user.save()
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully!')
        else:
            # Profile update (no password fields filled)
            user = request.user
            user.full_name = request.POST.get('full_name', user.full_name)
            user.email = request.POST.get('email', user.email)
            user.department = request.POST.get('department', user.department)
            
            # Phone validation - must be exactly 10 digits
            phone = request.POST.get('phone', '').strip()
            if phone:
                # Remove any spaces or dashes
                phone_clean = ''.join(filter(str.isdigit, phone))
                if len(phone_clean) != 10:
                    messages.error(request, 'Phone number must be exactly 10 digits!')
                    if request.user.role == 'employee':
                        return redirect('employee_dashboard')
                    elif request.user.role == 'manager':
                        return redirect('manager_dashboard')
                    else:
                        return redirect('admin_dashboard')
                user.phone = phone_clean
            
            # PROFILE PICTURE UPLOAD - Uses Pillow library to handle image files
            # request.FILES contains uploaded files from form
            # Saves to media/profiles/ folder (defined in models.py)
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            
            user.save()
            messages.success(request, 'Profile updated successfully!')
        
        # Redirect based on role
        if request.user.role == 'employee':
            return redirect('employee_dashboard')
        elif request.user.role == 'manager':
            return redirect('manager_dashboard')
        else:
            return redirect('admin_dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'account/profile.html', context)


# ============================================
# CHAT FEATURE - Real-time messaging with AJAX
# ============================================

@login_required
def get_chat_users(request):
    """
    CHAT API 1: Get list of users available for chat
    Returns JSON with user list and unread message count
    """
    # Role-based chat access: Employees see managers, Managers see their team
    if request.user.role == 'employee':
        users = User.objects.filter(role='manager')
    else:
        users = User.objects.filter(manager=request.user)
    
    user_list = []
    for user in users:
        # Count unread messages for badge display
        unread = ChatMessage.objects.filter(sender=user, receiver=request.user, is_read=False).count()
        user_list.append({
            'id': user.id,
            'name': user.full_name or user.email,
            'email': user.email,
            'role': user.role,
            'unread': unread
        })
    
    return JsonResponse({'users': user_list})


@login_required
def get_messages(request, user_id):
    """
    CHAT API 2: Load chat history between two users
    Returns all messages with attachment info (images/PDFs)
    """
    other_user = get_object_or_404(User, id=user_id)
    
    # Complex query: Get messages where BOTH users are sender OR receiver
    # This gets the full conversation between two people
    messages_qs = ChatMessage.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('created_at')
    
    # Mark all received messages as read (removes unread badge)
    ChatMessage.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    message_list = []
    for msg in messages_qs:
        msg_data = {
            'id': msg.id,
            'sender_id': msg.sender.id,
            'sender_name': msg.sender.full_name or msg.sender.email,
            'message': msg.message,
            'is_mine': msg.sender == request.user,
            'time': msg.created_at.strftime('%I:%M %p'),
            'date': msg.created_at.strftime('%b %d, %Y'),
            'has_attachment': bool(msg.attachment),
            'attachment_url': msg.attachment.url if msg.attachment else None,
            'attachment_name': msg.attachment_name or '',
            'is_image': msg.is_image,
            'is_pdf': msg.is_pdf,
        }
        message_list.append(msg_data)
    
    return JsonResponse({'messages': message_list})


@login_required
def send_message(request):
    """
    CHAT API 3: Send message with optional file attachment (IMAGE/PDF UPLOAD)
    Handles both text messages and file uploads using multipart/form-data
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # FILE UPLOAD DETECTION: Check if request contains files
        # multipart/form-data = file upload, application/json = text only
        if request.content_type and 'multipart/form-data' in request.content_type:
            receiver_id = request.POST.get('receiver_id')
            message_text = request.POST.get('message', '').strip()
            attachment = request.FILES.get('attachment')  # Get uploaded file
        else:
            data = json.loads(request.body)
            receiver_id = data.get('receiver_id')
            message_text = data.get('message', '').strip()
            attachment = None
        
        if not receiver_id:
            return JsonResponse({'error': 'Receiver ID required'}, status=400)
        
        if not message_text and not attachment:
            return JsonResponse({'error': 'Message or attachment required'}, status=400)
        
        receiver = get_object_or_404(User, id=receiver_id)
        
        # SAVE MESSAGE WITH ATTACHMENT: Pillow handles image processing
        # Files saved to media/chat_attachments/ folder
        msg = ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            message=message_text,
            attachment=attachment,  # FileField handles upload
            attachment_name=attachment.name if attachment else ''
        )
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': msg.id,
                'sender_id': msg.sender.id,
                'sender_name': msg.sender.full_name or msg.sender.email,
                'message': msg.message,
                'is_mine': True,
                'time': msg.created_at.strftime('%I:%M %p'),
                'date': msg.created_at.strftime('%b %d, %Y'),
                'has_attachment': bool(msg.attachment),
                'attachment_url': msg.attachment.url if msg.attachment else None,
                'attachment_name': msg.attachment_name or '',
                'is_image': msg.is_image,
                'is_pdf': msg.is_pdf,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def check_new_messages(request, user_id):
    """
    CHAT API 4: AJAX POLLING - Check for new messages every 2 seconds
    This is called repeatedly by JavaScript to get real-time updates
    """
    last_id = request.GET.get('last_id', 0)  # Track last message ID to avoid duplicates
    other_user = get_object_or_404(User, id=user_id)
    
    # Get only NEW messages (id greater than last_id)
    # This prevents re-fetching old messages
    new_messages = ChatMessage.objects.filter(
        sender=other_user,
        receiver=request.user,
        id__gt=last_id  # Only messages after last_id
    ).order_by('created_at')
    
    # Mark new messages as read
    new_messages.update(is_read=True)
    
    message_list = []
    for msg in new_messages:
        message_list.append({
            'id': msg.id,
            'sender_id': msg.sender.id,
            'sender_name': msg.sender.full_name or msg.sender.email,
            'message': msg.message,
            'is_mine': False,
            'time': msg.created_at.strftime('%I:%M %p'),
            'date': msg.created_at.strftime('%b %d, %Y'),
            'has_attachment': bool(msg.attachment),
            'attachment_url': msg.attachment.url if msg.attachment else None,
            'attachment_name': msg.attachment_name or '',
            'is_image': msg.is_image,
            'is_pdf': msg.is_pdf,
        })
    
    return JsonResponse({'messages': message_list})


@login_required
def chat_page(request):
    """Dedicated chat page"""
    return render(request, 'chat/chat.html')


@login_required
def delete_user(request, user_id):
    """Delete a user (admin only)"""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        user_to_delete = get_object_or_404(User, id=user_id)
        if user_to_delete == request.user:
            messages.error(request, 'You cannot delete yourself!')
        else:
            user_to_delete.delete()
            messages.success(request, f'User {user_to_delete.email} deleted successfully!')
    
    return redirect('all_users')
