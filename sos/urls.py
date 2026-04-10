from django.urls import path
from . import views

urlpatterns = [
    path('', views.sos_list, name='sos_list'),
    path('create/', views.create_sos, name='create_sos'),
    path('join/<int:sos_id>/', views.join_sos, name='join_sos'),
    path('approve/<int:id>/', views.approve_sos),
    path('reject/<int:id>/', views.reject_sos),
    
]