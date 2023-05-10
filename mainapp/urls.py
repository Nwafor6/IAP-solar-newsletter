from django.urls import path
from .import views

urlpatterns = [
    path('subscribe/', views.Subscribe),
    path("subscriber_list/", views.SubscribersList.as_view())
]