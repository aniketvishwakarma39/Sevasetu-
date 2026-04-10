from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-event/', views.create_event, name='create_event'),
    path('join/<int:event_id>/', views.join_event, name='join_event'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('sponsor/<int:event_id>/', views.sponsor_event, name='sponsor_event'),
    path('dashboard/', views.creator_dashboard, name='dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('my-dashboard/', views.my_dashboard, name='my_dashboard'),
    path('certificate/', views.generate_certificate, name='certificate'),
    path('approve-part/<int:id>/', views.approve_participation),
path('reject-part/<int:id>/', views.reject_participation),

path('approve-spon/<int:id>/', views.approve_sponsorship),
path('reject-spon/<int:id>/', views.reject_sponsorship),
]