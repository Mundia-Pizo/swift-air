

from json import tool
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView, ListView, DeleteView
import os
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from blog.models import Blog
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import  FlightAgent,Flight, OrderFlight, Order, Car, CarRental
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class HomeView(View):
    template_name = 'core/Home.html'

    def get(self, request, *args, **kwargs):
        latest_posts  = Blog.objects.all().order_by('-timestamp')[0:4]
        flights = Flight.objects.all().order_by('-date')[0:4]

        context = {
            'latest_posts':latest_posts,
            'flights':flights
        }
        return render (request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
    #     flights = FlightAgent.objects.all()
    #     context={
    #         'flights':flights
    #     }
    #     return render(request, 'core/air-search-results.html', context)

class FlightDetailView(DetailView):
    model = FlightAgent
    template_name='core/flight-detail.html'


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Flight, slug=slug)
    order_flight, created = OrderFlight.objects.get_or_create(
        flight=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.tickets.filter(flight__slug=item.slug).exists():
            order_flight.quantity += 1
            order_flight.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.tickets.add(order_flight)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.tickets.add(order_flight)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")


@login_required
def remove_from_cart(request, slug):
    flight = get_object_or_404(Flight, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.tickets.filter(flight__slug=flight.slug).exists():
            order_ticket = OrderFlight.objects.filter(
                flight=flight,
                user=request.user,
                ordered=False
            )[0]
            order.tickets.remove(order_ticket)
            order_ticket.delete()
            messages.info(request, "This ticket is removed from the saved tickets")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("order-summary", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("order-summary", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Flight, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.tickets.filter(flight__slug=item.slug).exists():
            order_item = OrderFlight.objects.filter(
                flight=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.tickets.remove(order_item)
                order_item.delete()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("order-summary", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("order-summary", slug=slug)

class OrderSummaryView(LoginRequiredMixin,View):
    model = OrderFlight
    template_name = 'core/order-summary.html'


    def get(self,request, *args, **kwargs):
        order_Item= OrderFlight.objects.filter(user=request.user, ordered=False)
        order = Order.objects.filter(user=request.user, ordered=False)

        total_price = 0
        for order_total in order_Item:
            total_price +=order_total.get_total_price()
           
        context={
           'orders':order_Item,
           'order':order,
           'total_price':total_price
        }
        return render(request, self.template_name, context)




class AirTicketView(View):
    template_name = 'core/air-ticket.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name )


"""this is the car rental view with all the 
funtionalities for posting and 
get inforamation to the server"""

class CarRentalView(View):
    template_name ='core/car-rental.html'

    def get(self,request,*args, **kwargs):
        cars = Car.objects.all()
        context={
            'cars':cars
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, 'core/car-search.html')


class CarDetailView(DeleteView):
    model = Car
    template_name = 'core/car-detail.html'



class SearchView(ListView):
    template_name = 'core/air-search-results.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            return FlightAgent.objects.search(query=query)
        return FlightAgent.objects.none()


