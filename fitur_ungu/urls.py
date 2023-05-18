from django.urls import path
from fitur_ungu.views import *

app_name = 'fitur_ungu'

urlpatterns = [
    path('enrolled-event', enrolled_event, name='enrolled_event'),
]