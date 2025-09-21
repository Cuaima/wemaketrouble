from django.contrib import admin
from .models import (
    User,
    StylistProfile,
    CustomerProfile,
    Service,
    Location,
    Booking,
    BookingService,
)

# Custom User admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_stylist", "is_customer", "is_staff")
    list_filter = ("is_stylist", "is_customer", "is_staff", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


# Profile admins
@admin.register(StylistProfile)
class StylistProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "address")
    search_fields = ("user__username", "user__email", "phone_number")


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "address")
    search_fields = ("user__username", "user__email", "phone_number")


# Service admin
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "stylist", "price", "duration")
    list_filter = ("stylist",)
    search_fields = ("name", "stylist__username")
    ordering = ("name",)


# Location admin
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "zip_code")
    search_fields = ("name", "city", "state", "zip_code")
    ordering = ("city", "name")


# Inline for BookingService
class BookingServiceInline(admin.TabularInline):
    model = BookingService
    extra = 1  # one empty row by default
    autocomplete_fields = ["service"]


# Booking admin
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "stylist",
        "customer",
        "appointment_date",
        "location",
        "total_price_display",
        "published_date",
    )
    list_filter = ("stylist", "customer", "appointment_date", "location")
    search_fields = ("stylist__username", "customer__username", "notes")
    ordering = ("-appointment_date",)
    date_hierarchy = "appointment_date"
    inlines = [BookingServiceInline]

    def total_price_display(self, obj):
        return obj.total_price()
    total_price_display.short_description = "Total Price"
