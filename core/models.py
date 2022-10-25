from email.mime import image
from django.db import models
from tinymce.models import HTMLField
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import reverse

from django.db.models import Q
from django.contrib.postgres.search import(
    SearchVector,
    SearchQuery,
    SearchRank)


class FlightQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            vector = SearchVector('origin', weight='A') \
                + SearchVector('destination', weight='B')\
                + SearchVector('date', weight='C')
            query = SearchQuery(query)
            result = Flight.objects.annotate(rank=SearchRank(vector,
                                                              query)).filter(rank__gte=0.3).order_by('rank').order_by('-rank')
        return result


class FlightManager(models.Manager):
    def get_queryset(self):
        return FlightQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

# Create your models here.
class Subscribe(models.Model):
    email=models.EmailField()
    date=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email 

class Flight(models.Model):
    origin = models.CharField(max_length=200, blank=True, null=True)
    destination = models.CharField(max_length=200, blank=True, null=True)
    flight_charge = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField()
    date_of_return = models.DateTimeField()
    # image = models.ImageField()
    slug = models.SlugField(blank=True, null=True)
    # date_listed = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.origin} to {self.destination} flight"


    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_book_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_book_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })
    def get_remove_single_book_url(self):
        return reverse("remove-single-item-from-cart", kwargs={
            'slug': self.slug
        })


class FlightAgent(models.Model):
    title = models.CharField(max_length=200)
    flights = models.ManyToManyField(Flight)
    date =models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    objects=FlightManager()

    def __str__(self) -> str:
        return self.title

    

    # @property
    # def flights(self):
    #     return self.flight_set.all()


class OrderFlight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, null=True, blank=True)
    date_booked = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.flight.origin} booked by {self.user.username}"


    def get_total_price(self):
        return self.quantity * self.flight.flight_charge

    # def get_complete_cost(self):
    #     total = 0


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(OrderFlight)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ordered Tickets"

    def get_total(self):
        total = 0
        for order_item in self.tickets.all():
            total += order_item.get_total_price()
        return  total

    # def get_total_quantity_cost(self):
    #     quantity_cost = 0
    #     for order_item in self.tickets.all():
    #         quantity_cost = 


class Car(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField()
    price_perday = models.PositiveIntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title


class CarRental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_rented =  models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField()
    duration  = models.CharField(max_length=200)


    def __str__(self) -> str:
        return super().__str__(self.title)
    

class Apartment(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField()
    date_booked = models.DateTimeField(auto_now_add=True)
    date_expired = models.DateTimeField()


    def __str__(self) -> str:
        return super().__str__(self.title)


