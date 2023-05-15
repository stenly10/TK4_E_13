from django.urls import path
from example_app.views import index, test

app_name = 'example_app'

urlpatterns = [
    path('', index, name='index'),
    path('test', test, name='test'),
]