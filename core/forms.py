from django import forms 
from .forms import SubscriptionForm
from django.forms.widgets import DateInput
from core.models import CarRental


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionForm
        fields = ('email',)

class CarForm(forms.MidelForm):
    class Meta:
        model = CarRental
        fields = "__all__"
    