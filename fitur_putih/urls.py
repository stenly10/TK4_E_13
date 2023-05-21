from django.urls import path
from fitur_putih.views import *

app_name = 'fitur_putih'

urlpatterns = [
    path('login', login_member, name='login'),
    path('register/atlet', register_atlet, name='register_atlet'),
    path('register/pelatih', register_pelatih, name='register_pelatih'),
    path('register/umpire', register_umpire, name='register_umpire'),
    path('register', register, name='register'),
    path('logout', logout_user, name='logout'),
    path('', landing_page, name='landing_page'),
]