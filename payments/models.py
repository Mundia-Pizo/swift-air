from django.db import models
from core.models import Flight
from django.contrib.auth.models import User 



# Create your models here.
class FlightPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # flight = models.ForeignKey(Flight, on_delete=models.CASCADE, null=True, blank=True)
    date_booked = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.user.username}'s Tickets"

