from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('help/', views.help, name='help'),
    path('quotes/', views.quotes, name='quotes'),
    path('booknow/', views.booknow, name='booknow'),
    path("submit/", views.submit_booking, name="submit_form"),
]
