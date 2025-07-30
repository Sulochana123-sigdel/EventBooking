from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.home, name='event_list'),  # Use home for event list
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('api/events/', views.api_events, name='api_events'),
    path('create-event/', views.create_event, name='create_event'),
    path('profile/', views.profile, name='profile'),
    path('my-events/', views.my_events, name='my_events'),

    # Password reset URLs using Django's built-in auth views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)