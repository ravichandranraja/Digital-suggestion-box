from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('suggestion/<int:suggestion_id>/', views.suggestion_detail, name='suggestion_detail'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('add-category/', views.add_category, name='add_category'),
    path('update-status/<int:suggestion_id>/', views.update_suggestion_status, name='update_suggestion_status'),
] 