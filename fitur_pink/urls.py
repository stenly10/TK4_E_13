from django.urls import path
from . import views

urlpatterns = [
    path('daftar_atlet/', views.daftar_atlet, name='daftar_atlet'),
    path('latih_atlet/', views.latih_atlet, name='latih_atlet'),
    path('list_atlet/', views.list_atlet, name='list_atlet'),
    path('list_partai_kompetisi/', views.list_partai_kompetisi, name='list_partai_kompetisi'),
    path('list_hasil_pertandingan/<str:jenis_partai>/<str:nama_event>/<int:tahun>/', views.list_hasil_pertandingan, name='list_hasil_pertandingan'),
]
