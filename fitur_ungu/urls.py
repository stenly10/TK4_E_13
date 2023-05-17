from django.urls import path
from fitur_ungu.views import *

app_name = 'fitur_ungu'

urlpatterns = [
    path('read-enrolled-event', read_enrolled_event, name='read_enrolled_event'),
]