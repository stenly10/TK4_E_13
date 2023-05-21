from django.shortcuts import render
from django.http import HttpResponse
import uuid
import psycopg2.extras
import psycopg2
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

conn = psycopg2.connect(
    database = settings.DATABASE_NAME,
    user = settings.DATABASE_USER,
    password = settings.DATABASE_PASSWORD,
    host = settings.DATABASE_HOST,
    port = settings.DATABASE_PORT,
)
curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def ujian_kualifikasi_question(request):
    return render(request, 'ujian_kualifikasi_question.html')

# @login_required("UMPIRE")
def ujian_kualifikasi_umpire_create(request):
    if request.method == "POST":
        tahun = request.POST.get('tahun')
        nomor_batch = request.POST.get('nomorbatch')
        tempat = request.POST.get('tempat')
        tanggal = request.POST.get('date')
    
        # query = f'INSERT INTO UJIAN_KUALIFIKASI VALUES (\'{tahun}\', \'{nomor_batch}\', \'{tempat}\, \'{tanggal}\)'
        # curr.execute(query)
    
    return render(request, 'ujian_kualifikasi_umpire_create.html')

def ujian_kualifikasi_umpire_read(request):
    query = f'SELECT * FROM UJIAN_KUALIFIKASI'
    curr.execute(query)
    lst = curr.fetchall()
    list_data = []
    for x in lst:
        context = {}
        context["tahun"] = x[0]
        context["batch"] = x[1]
        context["tempat"] = x[2]
        context["tanggal"] = x[3]
        print(context)
        list_data.append(context)

    return render(request, 'ujian_kualifikasi_umpire_read.html', {'data' : list_data})

# @login_required(role="ATLET")
def ujian_kualifikasi_atlet(request):
    query = f'SELECT * FROM UJIAN_KUALIFIKASI'
    curr.execute(query)
    lst = curr.fetchall()
    list_data = []
    for x in lst:
        context = {}
        context["tahun"] = x[0]
        context["batch"] = x[1]
        context["tempat"] = x[2]
        context["tanggal"] = x[3]
        print(context)
        list_data.append(context)

    return render(request, 'ujian_kualifikasi_atlet.html', {'data' : list_data})


def riwayat_kualifikasi_atlet(request):
    sp = '34847a13-05b0-42fa-a5e8-293203691bcf'
    query = f'SELECT * FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI WHERE id_atlet = \'{sp}\''
    curr.execute(query)
    lst = curr.fetchall()
    list_data = []
    for x in lst:
        context = {}
        context["tahun"] = x[1]
        context["batch"] = x[2]
        context["tempat"] = x[3]
        context["tanggal"] = x[4]
        context["hasil"] = x[5]
        print(context)
        list_data.append(context)

    return render(request, 'riwayat_kualifikasi_atlet.html', {'data' : list_data})


def riwayat_kualifikasi_umpire(request):
    query = f'SELECT * FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI'
    curr.execute(query)
    lst = curr.fetchall()
    list_data = []
    for x in lst:
        context = {}
        context["id"] = x[0]
        context["tahun"] = x[1]
        context["batch"] = x[2]
        context["tempat"] = x[3]
        context["tanggal"] = x[4]
        context["hasil"] = x[5]
        print(context)
        list_data.append(context)

    return render(request, 'riwayat_kualifikasi_umpire.html', {'data' : list_data})