from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Event, Booking, Category
from datetime import date
from django.db.models import Q

# Home Page - Event Listing with Filters
def home(request):
    today = date.today()

    # Get filters from request
    category = request.GET.get("category", "")
    start_date = request.GET.get("from", "")
    end_date = request.GET.get("to", "")
    search_query = request.GET.get("search", "")

    # Start with published, future events
    events = Event.objects.filter(status='published', date__gte=today)

    # Filter by category name from ForeignKey category__name
    if category and category.lower() != "all":
        events = events.filter(category__name__iexact=category)

    # Filter by date range
    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)

    # Search by event title
    if search_query:
        events = events.filter(title__icontains=search_query)

    # Calculate available seats for each event
    for event in events:
        bookings_count = Booking.objects.filter(event=event).count()
        event.available_seats = event.total_seats - bookings_count

    # Get all categories from DB
    categories = Category.objects.all()

    context = {
        'events': events,
        'categories': categories,
        'selected_category': category,
        'start_date': start_date,
        'end_date': end_date,
        'search_query': search_query,
    }

    return render(request, 'events/home.html', context)

# View Single Event Details
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    bookings_count = Booking.objects.filter(event=event).count()
    available_seats = event.total_seats - bookings_count
    
    context = {
        'event': event,
        'available_seats': available_seats,
        'total_seats': event.total_seats,
        'is_available': available_seats > 0
    }
    return render(request, 'events/event_detail.html', context)

# Book an Event
@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check available seats
    bookings_count = Booking.objects.filter(event=event).count()
    available_seats = event.total_seats - bookings_count
    
    if available_seats <= 0:
        messages.error(request, "No available seats for this event.")
        return redirect('event_detail', event_id=event.id)

    # Prevent double booking
    if Booking.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, "You already booked this event.")
        return redirect('event_detail', event_id=event.id)

    Booking.objects.create(user=request.user, event=event)
    messages.success(request, 'Successfully booked event!')
    return redirect('my_bookings')

# Show Logged-in User's Bookings
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('event')
    
    # Add seat information to each booking
    for booking in bookings:
        bookings_count = Booking.objects.filter(event=booking.event).count()
        booking.available_seats = booking.event.total_seats - bookings_count
    
    return render(request, 'events/my_bookings.html', {'bookings': bookings})

# User Registration
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                User.objects.create_user(username=username, email=email, password=password1)
                messages.success(request, 'Registration successful!')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'events/register.html')

# Login
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

# Logout
def logout_view(request):
    logout(request)
    return redirect('home')

# Create Event Page (Admin only or anyone)
@login_required
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        date_val = request.POST.get('date')
        time_val = request.POST.get('time')
        total_seats = int(request.POST.get('total_seats', 0))
        category_name = request.POST.get('category')
        
        # Get or create category
        category, created = Category.objects.get_or_create(name=category_name)
        
        # Create event
        event = Event.objects.create(
            title=title,
            description=description,
            location=location,
            date=date_val,
            time=time_val,
            total_seats=total_seats,
            seats=total_seats,  # <-- Add this line
            category=category,
            organizer=request.user,
            status='published'
    )
        messages.success(request, 'Event created successfully!')
        return redirect('event_detail', event_id=event.id)
    
    categories = Category.objects.all()
    return render(request, 'events/create_event.html', {'categories': categories})

# User Profile Page
@login_required
def profile(request):
    return render(request, 'events/profile.html')

# Admin's Created Events (Optional View)
@login_required
def my_events(request):
    events = Event.objects.filter(organizer=request.user)
    
    # Add seat information for each event
    for event in events:
        bookings_count = Booking.objects.filter(event=event).count()
        event.bookings_count = bookings_count
        event.available_seats = event.total_seats - bookings_count
    
    return render(request, 'events/my_events.html', {'events': events})

# REST API for JSON
def api_events(request):
    events = Event.objects.filter(status='published')
    data = [
        {
            "id": event.id,
            "title": event.title,
            "location": event.location,
            "date": str(event.date),
            "time": str(event.time),
            "total_seats": event.total_seats,
            "available_seats": event.total_seats - Booking.objects.filter(event=event).count()
        }
        for event in events
    ]
    return JsonResponse(data, safe=False)