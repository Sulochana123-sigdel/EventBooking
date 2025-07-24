from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    path('api/events/', views.api_events, name='api_events'),
]
