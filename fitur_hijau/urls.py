from django.urls import path
from fitur_hijau.views import *

app_name = 'fitur_hijau'

urlpatterns = [
    path('ujiankualifikasi/umpire/create', ujian_kualifikasi_umpire_create, name='ujian_kualifikasi_umpire_create'),
    path('ujiankualifikasi/umpire/read', ujian_kualifikasi_umpire_read, name='ujian_kualifikasi_umpire_read'),
    path('ujiankualifikasi/question', ujian_kualifikasi_question, name='ujian_kualifikasi_question'),
    path('ujiankualifikasi/atlet', ujian_kualifikasi_atlet, name='ujian_kualifikasi_atlet'),
    path('ujiankualifikasi/riwayat/atlet', riwayat_kualifikasi_atlet, name='riwayat_kualifikasi_atlet'),
    path('ujiankualifikasi/riwayat/umpire', riwayat_kualifikasi_umpire, name='riwayat_kualifikasi_umpire'),
     path('ujiankualifikasi/question/kualifikasi', atlet_kualifikasi_question, name='atlet_kualifikasi_question'),

]