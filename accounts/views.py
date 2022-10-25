from django.shortcuts import render
from django.views.generic import FormView, View

from core.models import OrderFlight
from .forms import UserRegistrationsForm


class RegistrationView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationsForm
    success_url = '/accounts/login'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super().form_valid(form)


class DashBoardView(View):
    template_name = 'accounts/dashboard.html'
    def get(self,request, *args, **kwargs):
        my_tickets = OrderFlight.objects.filter(user=request.user, ordered=True)
        context={
            'tickets':my_tickets
        }
        return render(request,self.template_name,context )
