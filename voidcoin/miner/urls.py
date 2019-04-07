from django.urls import path
from miner.views import *
urlpatterns = [
    path('',mine),
    path('show_blockchain/',show_blockchain),
]
