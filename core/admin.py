from django.contrib import admin

from .models import Car, CarRental,Flight, FlightAgent, Order, OrderFlight

admin.site.register(Car)
admin.site.register(CarRental)
admin.site.register(FlightAgent)
admin.site.register(Flight)
admin.site.register(OrderFlight)
admin.site.register(Order)


