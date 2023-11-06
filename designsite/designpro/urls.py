from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static



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
    path('all_user_requests/', views.all_user_requests, name='all_user_requests'),
    path('request_detail/<int:request_id>/', views.request_detail, name='request_detail'),
    path('change_request_status/<int:request_id>/', views.change_request_status, name='change_request_status'),
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)