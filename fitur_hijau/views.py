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



@login_required("ATLET")
def ujian_kualifikasi_question(request):
    if request.method =="POST":
        question_1  = request.POST.get('q1')
        question_2  = request.POST.get('q2')
        question_3  = request.POST.get('q3')
        question_4  = request.POST.get('q4')
        question_5  = request.POST.get('q5')

        correct_answers = 0
        if question_1 == "21":
            correct_answers += 1
        if question_2 == "poin":
            correct_answers += 1
        if question_3 == "1":
            correct_answers += 1    
        if question_4 == "england":
            correct_answers += 1
        if question_5 == "kanan":
            correct_answers += 1
        # print("jumlah benar : " + str(correct_answers)) 

        id_atlet = request.COOKIES['id']
        dict_info = request.COOKIES['dict_info']
        dict = ast.literal_eval(dict_info)

        tahun = dict['tahun']
        batch = dict['batch']
        tempat = dict['tempat']
        tanggal = dict['tanggal']
        if correct_answers > 3:
            query = f'UPDATE ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI SET hasil_lulus = true WHERE id_atlet = \'{id_atlet}\' AND tahun = \'{tahun}\' AND batch = \'{batch}\' AND tempat = \'{tempat}\' AND tanggal = \'{tanggal}\' AND hasil_lulus = false'
            print(query)
            curr.execute(query)
            conn.commit()
            return redirect('fitur_hijau:riwayat_kualifikasi_atlet')
    return render(request, 'ujian_kualifikasi_question.html')

@login_required("ATLET")
def atlet_kualifikasi_question(request):
    
    if request.method =="POST":
        return redirect('fitur_hijau:riwayat_kualifikasi_atlet')
    
    return render(request, 'atlet_kualifikasi_question.html')


@login_required("UMPIRE")
def ujian_kualifikasi_umpire_create(request):
    if request.method == "POST":
        tahun = request.POST.get('tahun')
        nomor_batch = request.POST.get('nomorbatch')
        tempat = request.POST.get('tempat')
        tanggal = request.POST.get('date')
    
        query = f'INSERT INTO UJIAN_KUALIFIKASI VALUES(\'{tahun}\', \'{nomor_batch}\', \'{tempat}\', \'{tanggal}\')'
        curr.execute(query)
        conn.commit()
        return redirect('fitur_hijau:ujian_kualifikasi_umpire_read')
    
    return render(request, 'ujian_kualifikasi_umpire_create.html')

@login_required("UMPIRE")
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

        try:
            query = f'INSERT INTO ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI VALUES(\'{id_atlet}\', \'{tahun}\', \'{batch}\', \'{tempat}\', \'{tanggal}\', false)'
            print(query)
            curr.execute(query)
            conn.commit()
            response = HttpResponseRedirect(reverse('fitur_hijau:ujian_kualifikasi_question'))
            response.set_cookie('dict_info', value)
            return response
        except Exception as e:
            error_msg = generate_error_message(e)
            print(error_msg)
                
            if error_msg == 'Ujian Kualifikasi sudah pernah diikuti':
                messages.error(request, generate_error_message(e))
                conn.rollback()
            elif error_msg == 'atlet_kualifikasi_ujian':
                conn.rollback()
                return redirect('fitur_hijau:atlet_kualifikasi_question')
                

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

@login_required(role="ATLET")
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

@login_required(role="UMPIRE")
def riwayat_kualifikasi_umpire(request):
    query = f'SELECT M.nama, ANU.tahun, ANU.batch, ANU.tempat, ANU.tanggal, ANU.hasil_lulus FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI AS ANU, MEMBER AS M WHERE M.id = ANU.id_atlet'
    curr.execute(query)
    lst = curr.fetchall()
    list_data = []
    for x in lst:
        context = {}
        context["nama"] = x[0]
        context["tahun"] = x[1]
        context["batch"] = x[2]
        context["tempat"] = x[3]
        context["tanggal"] = x[4]
        context["hasil"] = x[5]
        print(context)
        list_data.append(context)

    return render(request, 'riwayat_kualifikasi_umpire.html', {'data' : list_data})



