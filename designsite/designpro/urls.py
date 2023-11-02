from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name = 'login'),
    path('registration/', views.registration, name='registration'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('create_design_request/', views.create_design_request, name='create_design_request'),
    path('my_design_requests/', views.my_design_requests, name='my_design_requests'),
    path('my_design_requests/<int:request_id>/', views.request_detail, name='request_detail'),
    path('delete_request/<int:pk>/', views.delete_request, name='delete_request'),
]
