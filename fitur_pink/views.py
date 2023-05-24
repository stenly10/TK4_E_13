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

@login_required("UMPIRE")
def daftar_atlet(request):
    id_umpire = request.COOKIES['id']

    query_kualifikasi = f"SELECT M.nama, MAX(A.tgl_lahir) AS tgl_lahir, A.negara_asal, A.height, MAX(AK.world_rank) AS world_rank, MAX(AK.world_tour_rank) AS world_tour_rank, A.jenis_kelamin, SUM(PH.total_point) AS total_point FROM ATLET_KUALIFIKASI AS AK, ATLET AS A, MEMBER AS M, POINT_HISTORY AS PH WHERE AK.id_atlet = A.id AND A.id = M.id AND PH.id_atlet = AK.id_atlet GROUP BY M.nama, A.negara_asal, A.height, A.jenis_kelamin"

    curr.execute(query_kualifikasi)
    lst_kualifikasi = curr.fetchall()
    change_format(lst_kualifikasi)

    query_non_kualifikasi = f"SELECT M.nama, A.tgl_lahir, A.negara_asal, A.height, A.play_right, A.jenis_kelamin FROM ATLET_NON_KUALIFIKASI AS ANK, ATLET AS A, MEMBER AS M WHERE ANK.id_atlet = A.id AND A.id = M.id"
    
    curr.execute(query_non_kualifikasi )
    lst_non_kualifikasi = curr.fetchall()
    change_format(lst_non_kualifikasi)

    query_ganda = """
    SELECT
      AG.id_atlet_ganda,
      M1.nama AS nama_atlet_kualifikasi,
      M2.nama AS nama_atlet_kualifikasi_2,
      SUM(PH.total_point) AS total_point
    FROM
      ATLET_GANDA AS AG
      JOIN POINT_HISTORY AS PH ON PH.id_atlet = AG.id_atlet_kualifikasi OR PH.id_atlet = AG.id_atlet_kualifikasi_2
      JOIN MEMBER AS M1 ON AG.id_atlet_kualifikasi = M1.id
      JOIN MEMBER AS M2 ON AG.id_atlet_kualifikasi_2 = M2.id
    GROUP BY
      AG.id_atlet_ganda,
      M1.nama,
      M2.nama
    """

    curr.execute(query_ganda)
    lst_ganda = curr.fetchall()
    change_format(lst_ganda)

    context = {
        'atlet_kualifikasi':lst_kualifikasi,
        'atlet_non_kualifikasi':lst_non_kualifikasi,
        'atlet_ganda':lst_ganda,
    }
    return render(request, 'daftar_atlet.html', context)

@login_required("PELATIH")
def latih_atlet(request):
    id_pelatih = request.COOKIES['id']

    if request.method == "POST":
        latih_atlet_post(request, id_pelatih)

    # ini blm

    query = f"SELECT A.id, A.email, A.world_rank, M.email FROM ATLET AS A, MEMBER AS M, ATLET_PELATIH AS AP WHERE AP.id_pelatih = \'{id_pelatih}\' AND AP.id_atlet = A.id AND A.id = M.id"
    
    curr.execute(query)
    lst = curr.fetchall()
    change_format(lst)
    context = {
        'atlet':lst
    }

    # return render(request, 'list_atlet.html', context)

def latih_atlet_post(request, id_pelatih):
    id_atlet = request.POST.get('id_atlet')
    if id_atlet is None:
        messages.error(request, "Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu")
        return
    
    try:
        dml = f"INSERT INTO ATLET_PELATIH VALUES(\'{id_pelatih}\', \'{id_atlet}\')"
        curr.execute(dml)
        conn.commit()
        messages.success(request, "Berhasil mendaftarkan atlet baru")
    except Exception as e:
        conn.rollback()
        messages.error(request, generate_error_message(e))
    return

# read
@login_required("PELATIH")
def list_atlet(request):
    id_pelatih = request.COOKIES['id']

    query = """
    SELECT A.id, M.email, A.world_rank
    FROM ATLET AS A, MEMBER AS M, ATLET_PELATIH AS AP
    WHERE AP.id_pelatih = '73db521c-e781-4924-aa6b-3ae5ffcbe9b0'
    AND AP.id_atlet = A.id
    AND A.id = M.id
    """

    curr.execute(query)
    lst = curr.fetchall()
    change_format(lst)
    context = {
        'atlet':lst
    }
    return render(request, 'list_atlet.html', context)

@login_required("UMPIRE")
def list_partai_kompetisi(request):

    query = """
    SELECT 
    E.nama_event,PK.tahun_event AS tahun_event, E.nama_stadium, PK.jenis_partai, E.kategori_superseries, E.tgl_mulai, E.tgl_selesai, S.kapasitas,
    COUNT(PME.nomor_peserta) AS jumlah_pendaftar,
    COUNT(PME.nomor_peserta) = S.kapasitas AS is_full

    FROM 
    PARTAI_KOMPETISI AS PK
    JOIN EVENT AS E ON PK.nama_event = E.nama_event AND PK.tahun_event = E.tahun
    JOIN STADIUM AS S ON E.nama_stadium = S.nama AND E.negara = S.negara
    JOIN PESERTA_MENDAFTAR_EVENT AS PME ON E.nama_event = PME.nama_event AND E.tahun = PME.tahun

    GROUP BY 
    E.nama_event, PK.tahun_event, E.nama_stadium, PK.jenis_partai, E.kategori_superseries, E.tgl_mulai, E.tgl_selesai, S.kapasitas
    """
    
    curr.execute(query)
    lst = curr.fetchall()
    change_format(lst)
    context = {
        'partai_kompetisi':lst
    }
    return render(request, 'list_partai_kompetisi.html', context)

@login_required("UMPIRE")
def list_hasil_pertandingan(request, jenis_partai, nama_event, tahun):
    
    query ="""
    SELECT 
    E.nama_event, PK.tahun_event AS tahun_event, E.nama_stadium, PK.jenis_partai, E.kategori_superseries, E.tgl_mulai, E.tgl_selesai, S.kapasitas,

    FROM 
    PARTAI_KOMPETISI AS PK
    JOIN EVENT AS E ON PK.nama_event = E.nama_event AND PK.tahun_event = E.tahun
    JOIN STADIUM AS S ON E.nama_stadium = S.nama AND E.negara = S.negara

    WHERE
    PK.jenis_partai = '{jenis_partai}' AND
    E.nama_event = '{nama_event}' AND
    PK.tahun_event = {tahun}

    GROUP BY 
    E.nama_event, PK.tahun_event, E.nama_stadium, PK.jenis_partai, E.kategori_superseries, E.tgl_mulai, E.tgl_selesai, S.kapasitas
    """.format(jenis_partai=jenis_partai, nama_event=nama_event, tahun=tahun)

    
    curr.execute(query)
    lst = curr.fetchall()
    change_format(lst)
    context = {
        'hasil_pertandingan':lst
    }
    return render(request, 'list_hasil_pertandingan.html', context)