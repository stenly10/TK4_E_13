from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import psycopg2
import psycopg2.extras
import json
from datetime import date
from fitur_putih.auth import login_required
from django.contrib import messages

conn = psycopg2.connect(
    database = settings.DATABASE_NAME,
    user = settings.DATABASE_USER,
    password = settings.DATABASE_PASSWORD,
    host = settings.DATABASE_HOST,
    port = settings.DATABASE_PORT,
)

curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Create your views here.

@login_required(role="ATLET_KUALIFIKASI")
def enrolled_event(request):
    if request.method == "POST":
        unenroll_event(request)
    query = ("SELECT E.nama_event, E.total_hadiah, E.tahun, E.nama_stadium, PAR.jenis_partai, E.kategori_superseries, E.tgl_mulai, E.tgl_selesai "
            + "FROM PARTAI_PESERTA_KOMPETISI AS PAR, EVENT AS E, PESERTA_KOMPETISI AS PK "
            + "WHERE PAR.nama_event=E.nama_event " 
            + "AND PAR.tahun_event=E.tahun "
            + "AND PAR.nomor_peserta = PK.nomor_peserta "
            + "AND (PK.id_atlet_kualifikasi = " + f"\'{request.COOKIES['id']}\')")
    curr.execute(query)
    lst = curr.fetchall()
    change_format(lst)
    context = {
        "events": lst
    }
    return render(request, "enrolled_event.html", context=context)

def unenroll_event(request):
    id_atlet = request.COOKIES['id']
    nama_event = request.POST['nama_event']
    tahun = int(request.POST['tahun'])
    query = ("SELECT PME.nomor_peserta FROM PESERTA_MENDAFTAR_EVENT AS PME, PESERTA_KOMPETISI AS PK "
             + f"WHERE PME.nama_event = \'{nama_event}\' AND PME.tahun = {tahun} "
             + f"AND PME.nomor_peserta = PK.nomor_peserta AND PK.id_atlet_kualifikasi = \'{id_atlet}\'")
    curr.execute(query)
    lst = curr.fetchall()
    no_peserta = dict(lst[0])['nomor_peserta']
    dml = f"DELETE FROM PESERTA_MENDAFTAR_EVENT AS PME WHERE PME.nomor_peserta = {no_peserta} AND PME.tahun = {tahun} AND PME.nama_event = \'{nama_event}\'"
    try:
        curr.execute(dml)
        conn.commit()
        messages.success(request, f"Berhasil unenroll event {nama_event} tahun {tahun}")
    except Exception as e:
        messages.error(request, generate_error_message(e))
        conn.rollback()

def generate_error_message(exception):
    msg = str(exception)
    msg = msg[:msg.index('CONTEXT')-1]
    return msg


def change_format(lst):
    for i in range(len(lst)):
        lst[i] = dict(lst[i])
        change_date_format(lst[i])

def change_date_format(param):
    for key in param:
        if(isinstance(param[key], date)):
            param[key] = param[key].strftime('%d-%m-%Y')



@login_required(role="ATLET_KUALIFIKASI")
def daftar_sponsor(request):
    id_user = request.COOKIES['id']
    if request.method == "POST":
        daftar_sponsor_post(request, id_user)
    query = ("SELECT S.id, S.nama_brand FROM SPONSOR S WHERE NOT EXISTS "
             + f"(SELECT * FROM ATLET_SPONSOR AS ASP WHERE S.id = ASP.id_sponsor AND ASP.id_atlet = \'{id_user}\')")
    curr.execute(query)
    lst = curr.fetchall()
    change_format(lst)
    context = {
        'sponsors':lst
    }
    return render(request, 'daftar_sponsor.html', context)

def daftar_sponsor_post(request, id_user):
    id_sponsor = request.POST['id_sponsor']
    tgl_mulai = request.POST.get('tgl_mulai', None)
    tgl_selesai = request.POST.get('tgl_selesai', None)
    if not tgl_mulai or not tgl_selesai:
        messages.error(request, "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu")
        return
    try:
        dml = f"INSERT INTO ATLET_SPONSOR VALUES(\'{id_user}\', \'{id_sponsor}\', \'{tgl_mulai}\', \'{tgl_selesai}\')"
        curr.execute(dml)
        conn.commit()
        messages.success(request, "Berhasil mendaftarkan sponsor baru")
    except Exception as e:
        conn.rollback()
        messages.error(request, generate_error_message(e))
    return 

@login_required("ATLET_KUALIFIKASI")
def list_sponsor(request):
    id_user = request.COOKIES['id']
    query = f"SELECT ASP.tgl_mulai, ASP.tgl_selesai, S.nama_brand FROM ATLET_SPONSOR AS ASP, SPONSOR AS S WHERE ASP.id_atlet = \'{id_user}\' AND ASP.id_sponsor = S.id"
    curr.execute(query)
    lst = curr.fetchall()
    change_format(lst)
    context = {
        'list_atlet_sponsor':lst
    }
    return render(request, "list_sponsor.html", context)


