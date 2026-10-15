from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.issue_list, name='issue_list'),
    path('issue/<int:id>/', views.issue_detail, name='issue_detail'),
    path('new/', views.issue_create, name='issue_create'),
    path('map/', views.map_view, name='map_view'),
    path('update/<int:issue_id>/', views.update_status, name='update_status'),
    path('register/', views.register, name='register'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('citizen-dashboard/', views.citizen_dashboard, name='citizen_dashboard'),
    path('issue/<int:issue_id>/send-email/', views.send_issue_email, name='send_issue_email'),

]
