from django.db import models
from django.contrib.auth.models import User
import datetime

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    timezone = models.CharField(max_length=50, default='EST')
    location = models.CharField(max_length=255)
    venue_address = models.CharField(max_length=300, blank=True)
    venue_parking_info = models.CharField(max_length=300, blank=True)
    venue_accessibility = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seats = models.PositiveIntegerField()
    total_seats = models.PositiveIntegerField(default=100)
    max_tickets_per_user = models.PositiveIntegerField(default=5)
    refund_policy = models.TextField(blank=True)
    is_free = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[('draft', 'Draft'), ('published', 'Published')],
        default='draft'
    )
    publish_date = models.DateTimeField(null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

class Speaker(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='speakers')
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='speakers/', blank=True, null=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ScheduleItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedule_items')
    time = models.TimeField()
    title = models.CharField(max_length=200)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    speaker = models.ForeignKey(Speaker, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField()

    def __str__(self):
        return self.question

class Booking(models.Model):
    CATEGORY_CHOICES = [
        ('Festival', 'Festival'),
        ('Party', 'Party'),
        ('Seminar', 'Seminar'),
        ('Competition', 'Competition'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, default="")
    description = models.TextField(default="")
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Festival')
    date = models.DateField(default=datetime.date.today)
    time = models.TimeField(default=datetime.time(0, 0))
    location = models.CharField(max_length=255, default="Unknown Location")
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} booked {self.event.title}"