from time import timezone
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import CsrfExemptMixin
from core.models import Order, OrderFlight
from .models import FlightPayment
# Create your views here.


class PaymentSuccess(CsrfExemptMixin,LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)    
    def get(self,request, *args, **kwargs):
        order_flight = OrderFlight.objects.filter(user=request.user, ordered=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        try:
            r = request.GET.get('response')
            print("this is the response", r)
            import json
            r_dict=json.loads(r)
            status = r_dict['status']
            amount = r_dict['amount']
            print(status)
            print(amount)
            if status == 'successful':
                """Adding some logic for updating the user paid tickets"""

                for flight in order_flight:
                    flight.ordered = True
                    flight.save()
                for order in orders:
                    order.ordered = True
                    order.save()
                messages.info(request,'Payment successful for the ticket(s)')
                return redirect('dashboard')
            else:
                return redirect('order-summary')
        except:
            messages.info(request, "Oopps !!!! Some error occured!!! please try again.")
            return redirect('summary')





