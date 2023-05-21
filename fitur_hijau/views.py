from time import strftime
from venv import logger
from django.shortcuts import redirect, render
from django.http import HttpResponse
import uuid
import psycopg2.extras
import psycopg2
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from fitur_putih.auth import *
import ast
from datetime import datetime


conn = psycopg2.connect(
    database = settings.DATABASE_NAME,
    user = settings.DATABASE_USER,
    password = settings.DATABASE_PASSWORD,
    host = settings.DATABASE_HOST,
    port = settings.DATABASE_PORT,
)
curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)



# @login_required("ATLET")
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

@login_required(role="ATLET")
def ujian_kualifikasi_atlet(request):
    # tested = '34847a13-05b0-42fa-a5e8-293203691bcf'
    # queryzz = f'SELECT ANU.id_atlet into id_atlet_sekarang FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI AS ANU WHERE id_atlet = \'{tested}\''

    query = f'SELECT * FROM UJIAN_KUALIFIKASI'
    curr.execute(query)
    lst = curr.fetchall()
    list_data = []
    for x in lst:
        context = {}
        context["tahun"] = x[0]
        context["batch"] = x[1]
        context["tempat"] = x[2]
        context["tanggal"] =  x[3].strftime("%Y-%m-%d")
        list_data.append(context)

    if request.method =="POST":
        value = request.POST.get('pilihan')
        test = ast.literal_eval(value)

        id_atlet = request.COOKIES['id']
        tahun = test['tahun']
        batch = test['batch']
        tempat = test['tempat']
        tanggal = test['tanggal']
        datetime_object = datetime.strptime(tanggal, "%Y-%m-%d")
        try:
            query = f'INSERT INTO ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI VALUES (\'{id_atlet}\', \'{tahun}\', \'{batch}\', \'{tempat}\', \'{tanggal}\')'
            curr.execute(query)
            return render(request, 'ujian_kualifikasi_question.html')
        except Exception as e:
             messages.error(request, generate_error_message(e))
             conn.rollback()


    return render(request, 'ujian_kualifikasi_atlet.html', {'data' : list_data})

def generate_error_message(exception):
    msg = str(exception)
    msg = msg[:msg.index('CONTEXT')-1]
    return msg

def check_ujian_kualifikasi(request):
    id_atlet = request.COOKIES['id']
    query = f'SELECT * FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI WHERE id_atlet = \'{id_atlet}\''
    curr.execute(query)
    lst = curr.fetchall()

    return render(request, 'ujian_kualifikasi_question.html')


def riwayat_kualifikasi_atlet(request):
    id_atlet = request.COOKIES['id']
    query = f'SELECT * FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI WHERE id_atlet = \'{id_atlet}\''
    print(id_atlet)
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