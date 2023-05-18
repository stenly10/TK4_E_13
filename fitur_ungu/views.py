from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import psycopg2
import psycopg2.extras
import json
from datetime import date
from fitur_putih.auth import login_required

conn = psycopg2.connect(
    database = settings.DATABASE_NAME,
    user = settings.DATABASE_USER,
    password = settings.DATABASE_PASSWORD,
    host = settings.DATABASE_HOST,
    port = settings.DATABASE_PORT,
)

curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Create your views here.

@login_required(role="ATLET")
def read_enrolled_event(request):
    
    query = ("SELECT E.nama_event, E.tahun, E.nama_stadium, PAR.jenis_partai, E.kategori_superseries, E.tgl_mulai, E.tgl_selesai "
            + "FROM PARTAI_PESERTA_KOMPETISI AS PAR, EVENT AS E, PESERTA_KOMPETISI AS PK "
            + "WHERE PAR.nama_event=E.nama_event " 
            + "AND PAR.tahun_event=E.tahun "
            + "AND PAR.nomor_peserta = PK.nomor_peserta "
            + "AND (PK.id_atlet_kualifikasi = " + f"\'{request.COOKIES['id']}\')")
    curr.execute(query)
    lst = curr.fetchall()
    change_format(lst)
    context = {
        "data":lst
    }
    return HttpResponse(json.dumps(lst), content_type = "application/json")

def change_format(lst):
    for i in range(len(lst)):
        lst[i] = dict(lst[i])
        change_date_format(lst[i])

def change_date_format(param):
    for key in param:
        if(isinstance(param[key], date)):
            param[key] = param[key].strftime('%d-%m-%Y')
