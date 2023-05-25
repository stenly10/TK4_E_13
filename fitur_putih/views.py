from django.shortcuts import render
from django.http import HttpResponse
from fitur_putih.auth import authenticate, login, logout
import uuid
import psycopg2.extras
import psycopg2
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from fitur_putih.auth import login_required
from fitur_putih.auth import get_role_with_id
from datetime import date
from datetime import datetime


conn = psycopg2.connect(
    database = settings.DATABASE_NAME,
    user = settings.DATABASE_USER,
    password = settings.DATABASE_PASSWORD,
    host = settings.DATABASE_HOST,
    port = settings.DATABASE_PORT,
)
curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Create your views here.


def generate_error_message(exception):
    msg = str(exception)
    msg = msg[:msg.index('CONTEXT')-1]
    return msg

def login_member(request):
    if request.method == "GET":
        return render(request, "login.html")
    nama = request.POST["nama"]
    email = request.POST["email"]
    member = authenticate(nama = nama, email = email)
    if member == None:
        messages.error(request, "Email atau nama salah")
        return render(request, "login.html")
    return login(member['id'])
    

def register(request):
    return render(request, 'register.html')

def register_atlet(request):
    if request.method == "GET":
        return render(request, "register_atlet.html")
    
    id = generate_id()
    nama = request.POST['nama']
    email = request.POST['email']
    tgl_lahir = change_date_format(request.POST['tgl_lahir'])
    negara_asal = request.POST['negara']
    play_right = request.POST.get('kanan', None) != None
    height = request.POST['tinggi_badan']
    jenis_kelamin = request.POST.get('laki_laki', None) != None
        
    try:
        register_member(id, nama, email)
        insert_atlet = f"INSERT INTO ATLET VALUES(\'{id}\', \'{tgl_lahir}\', \'{negara_asal}\', \'{play_right}\', {height}, null, \'{jenis_kelamin}\')"
        curr.execute(insert_atlet)
        conn.commit()
    except Exception as e:
        error_msg = generate_error_message(e)
        messages.error(request, generate_error_message(e))
        conn.rollback()
        return render(request, "register_atlet.html")
    return HttpResponseRedirect(reverse("fitur_putih:login"))



def register_pelatih(request):
    if request.method == "GET":
        return render(request, "register_pelatih.html")
    
    id = generate_id()
    nama = request.POST['nama']
    email = request.POST['email']
    tgl_mulai = request.POST['tgl_mulai']
    tunggal_putra = request.POST.get('tunggal_putra', None)
    tunggal_putri = request.POST.get('tunggal_putri', None)
    ganda_putra = request.POST.get('ganda_putra', None)
    ganda_putri = request.POST.get('ganda_putri', None)
    ganda_campuran = request.POST.get('ganda_campuran', None)

    try:
        register_member(id, nama, email)
        insert_pelatih = f"INSERT INTO PELATIH VALUES(\'{id}\', \'{tgl_mulai}\')"
        curr.execute(insert_pelatih)
        if tunggal_putra != None:
            insert_pelatih_spesialisasi(id, "Tunggal Putra")
        if tunggal_putri != None:
            insert_pelatih_spesialisasi(id, "Tunggal Putri")
        if ganda_putra != None:
            insert_pelatih_spesialisasi(id, "Ganda Putra")
        if ganda_putri != None:
            insert_pelatih_spesialisasi(id, "Ganda Putri")
        if ganda_campuran != None:
            insert_pelatih_spesialisasi(id, "Ganda Campuran")
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        return render(request, "register_pelatih.html")
    
    return HttpResponseRedirect(reverse("fitur_putih:login"))

def register_umpire(request):
    if request.method == "GET":
        return render(request, "register_umpire.html")
    id = generate_id()
    nama = request.POST['nama']
    email = request.POST['email']
    negara = request.POST['negara']
    
    try:
        register_member(id, nama, email)
        insert_umpire = f"INSERT INTO UMPIRE VALUES(\'{id}\', \'{negara}\')"
        curr.execute(insert_umpire)
        conn.commit()
    except Exception as e:
        conn.rollback()
        return render(request, "register_umpire.html")
    
    return HttpResponseRedirect(reverse("fitur_putih:login"))
    
def generate_id():
    id = str(uuid.uuid4())
    while is_exist_id(id):
        id = str(uuid.uuid4())
    return id
        
def is_exist_id(id):
    query = f'SELECT id FROM MEMBER WHERE MEMBER.id = \'{id}\''
    curr.execute(query)
    lst = curr.fetchall()
    return len(lst) > 0
    
def change_date_format(tgl):
    """
    Change date format to YYYY-mm-dd
    return date in string
    """
    return f'{tgl[6:]}-{tgl[3:5]}-{tgl[0:2]}'

def register_member(id, nama, email):
    insert_member = f"INSERT INTO MEMBER VALUES(\'{id}\', \'{nama}\', \'{email}\')"
    curr.execute(insert_member)

def insert_pelatih_spesialisasi(id, sp):
    query = f'SELECT id FROM SPESIALISASI WHERE spesialisasi = \'{sp}\''
    curr.execute(query)
    lst = curr.fetchall()
    id_sp = dict(lst[0])['id']
    query = f'INSERT INTO PELATIH_SPESIALISASI VALUES(\'{id}\', \'{id_sp}\')'
    curr.execute(query)

def logout_user(request):
    return logout()

def landing_page(request):
    return render(request, 'landing_page.html')


@login_required(role="PELATIH")
def dashboard_pelatih(request):
    id = request.COOKIES['id']
    query = ("SELECT M.nama, M.email, P.tanggal_mulai, STRING_AGG(S.spesialisasi, \', \') AS spesialisasi "
            + "FROM MEMBER M "
            + f"JOIN PELATIH P ON P.id = \'{id}\' AND P.id = M.id "
            + "JOIN PELATIH_SPESIALISASI PS ON PS.id_pelatih = P.id "
            + "JOIN SPESIALISASI S ON PS.id_spesialisasi = S.id "
            + "GROUP BY P.id, M.id")
    curr.execute(query)
    lst = curr.fetchall()
    pelatih = dict(lst[0])
    context = {
        'pelatih':pelatih
    }
    return render(request, 'dashboard_pelatih.html', context)

@login_required(role="ATLET")
def dashboard_atlet(request):
    id = request.COOKIES['id']
    query = ("SELECT M.nama, M.email, A.negara_asal, A.tgl_lahir, A.play_right, A.height, A.world_rank, A.jenis_kelamin, STRING_AGG(P.nama, \', \') AS pelatih "
            + "FROM MEMBER M "
            + f"JOIN ATLET A ON A.id = \'{id}\' AND A.id = M.id "
            + "JOIN ATLET_PELATIH AP ON AP.id_atlet = A.id "
            + "JOIN (SELECT PEL.id, MEM.nama FROM PELATIH PEL JOIN MEMBER MEM ON PEL.id = MEM.id) P ON AP.id_pelatih = P.id "
            + "GROUP BY M.id, A.id")
    curr.execute(query)
    lst = curr.fetchall()
    atlet = dict(lst[0])
    atlet['total_point'] = get_total_point_atlet(id)
    context = {
        'atlet':atlet
    }
    return render(request, "dashboard_atlet.html", context)

def get_total_point_atlet(id):
    query = f"SELECT * FROM POINT_HISTORY WHERE id_atlet = \'{id}\'"
    curr.execute(query)
    lst = curr.fetchall()
    if len(lst) == 0:
        return 0
    change_format(lst)
    return create_total_point(lst)

def create_total_point(lst):
    lst = sorted(lst, key= lambda x: (x['tahun'], x['bulan'], x['minggu_ke']), reverse=True)
    total_point = 0
    for elm in lst[:52]:
        total_point += elm['total_point']
    return total_point

@login_required(role="UMPIRE")
def dashboard_umpire(request):
    id = request.COOKIES['id']
    query = f"SELECT M.nama, M.email, U.negara FROM MEMBER AS M, UMPIRE AS U WHERE U.id = \'{id}\' AND U.id = M.id"
    curr.execute(query)
    lst = curr.fetchall()
    umpire = dict(lst[0])
    context = {
        'umpire':umpire
    }
    return render(request, 'dashboard_umpire.html', context)

def change_format(lst):
    for i in range(len(lst)):
        lst[i] = dict(lst[i])
        change_month(lst[i])

def change_month(param):
    param['bulan'] = datetime.strptime(param['bulan'], '%B').month
        
        

