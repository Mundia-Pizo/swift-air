
from ssl import ALERT_DESCRIPTION_RECORD_OVERFLOW
from  django.urls import path 
from .views import  (
    HomeView, 
    AirTicketView, 
    CarRentalView,
    CarDetailView,
    FlightDetailView,
    OrderSummaryView,
    SearchView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart
    )



urlpatterns =[
    path('', HomeView.as_view(), name = 'home'),
    # path('<str:slug>/city/detail',CityDetailView.as_view(), name='city-details' ),
    # path('<str:slug>/place/detail', PlaceDetailView.as_view(), name='place-detail'),
    # path('iata/', iata, name='iata'),
    path('results/', SearchView.as_view(), name='search'),
    path('ticket/', AirTicketView.as_view(), name="tickets"),
    path('car-rental/', CarRentalView.as_view(), name='car-rental'),
    path('<str:slug>/car-detail', CarDetailView.as_view(), name='car-detail'),
    path('<str:slug>/flight-detail',FlightDetailView.as_view(), name='flight-detail' ),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<str:slug>/',add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<str:slug>/',remove_from_cart, name='remove-from-cart'),
    path('remove-from-single-ticket/<str:slug>/',remove_single_item_from_cart, name='remove-single-item-from-cart'),
]



