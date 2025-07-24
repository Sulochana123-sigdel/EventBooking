from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Booking

def home(request):
    events = Event.objects.all()
    return render(request, 'events/home.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Booking.objects.create(user=request.user, event=event)
    messages.success(request, 'Successfully booked event!')
    return redirect('my_bookings')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'events/my_bookings.html', {'bookings': bookings})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'events/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'events/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

from django.http import JsonResponse
from .models import Event

def api_events(request):
    events = Event.objects.all()
    data = [
        {
            "id": event.id,
            "title": event.title,
            "location": event.location,
            "date": str(event.date),
            "time": str(event.time),
        }
        for event in events
    ]
    return JsonResponse(data, safe=False)