from django.urls import path
from fitur_hijau.views import *

app_name = 'fitur_hijau'

urlpatterns = [
    path('ujiankualifikasi/umpire', ujian_kualifikasi_umpire, name='ujian_kualifikasi_umpire'),
    path('ujiankualifikasi/question', ujian_kualifikasi_question, name='ujian_kualifikasi_question'),
    path('ujiankualifikasi/atlet', ujian_kualifikasi_atlet, name='ujian_kualifikasi_atlet'),
    path('ujiankualifikasi/riwayat', riwayat_kualifikasi, name='riwayat_kualifikasi'),

]