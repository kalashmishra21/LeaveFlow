from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/employee/', views.employee_dashboard, name='employee_dashboard'),
    path('dashboard/users/', views.all_users, name='all_users'),
    path('leaves/request/', views.request_leave, name='request_leave'),
    path('leaves/my-leaves/', views.my_leaves, name='my_leaves'),
    path('leaves/all/', views.all_leaves, name='all_leaves'),
    path('leaves/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('leaves/cancel/<int:leave_id>/', views.cancel_leave, name='cancel_leave'),
    path('leaves/history/', views.team_history, name='team_history'),
    # Chat URLs
    path('chat/', views.chat_page, name='chat_page'),
    path('chat/users/', views.get_chat_users, name='get_chat_users'),
    path('chat/messages/<int:user_id>/', views.get_messages, name='get_messages'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/check/<int:user_id>/', views.check_new_messages, name='check_new_messages'),
    # User management
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]
