from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils import timezone
from decimal import Decimal

class User(AbstractUser):
    is_stylist = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)


class BaseProfile(models.Model):
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    class Meta:
        abstract = True

class StylistProfile(BaseProfile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} (Stylist)"

class CustomerProfile(BaseProfile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} (Customer)"
    
class Service(models.Model):
    stylist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="services"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.DurationField()  # e.g., timedelta(hours=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        f"{self.name} ({self.price} USD)"
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    

class Booking(models.Model):
    # Django creates an "id" automatically, no need to declare it unless you want a custom PK.
    stylist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings_as_stylist"
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings_as_customer"
    )
    appointment_date = models.DateTimeField()
    duration = models.DurationField()  # e.g., timedelta(hours=1)
    notes = models.TextField(blank=True)
    def total_price(self):
        return sum(service.price for service in self.services.all())
    published_date = models.DateTimeField(blank=True, null=True)
    services = models.ManyToManyField(Service, through="BookingService", related_name="bookings")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return f"Booking {self.id} for {self.customer} with {self.stylist} on {self.appointment_date:%Y-%m-%d %H:%M}"
    
class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def line_total(self):
        return self.quantity * self.service.price
