from django.contrib import admin
from .models import Event, Speaker, ScheduleItem, FAQ, Category, Booking

class SpeakerInline(admin.TabularInline):
    model = Speaker
    extra = 1

class ScheduleItemInline(admin.TabularInline):
    model = ScheduleItem
    extra = 1

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [SpeakerInline, ScheduleItemInline, FAQInline]
    list_display = ('title', 'date', 'location', 'status', 'publish_date')
    list_filter = ('status', 'date')

admin.site.register(Category)
admin.site.register(Booking)