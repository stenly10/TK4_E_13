from django.shortcuts import render
import psycopg2
from django.conf import settings
from django.http import HttpResponse
import json

conn = psycopg2.connect(
    database = settings.DATABASE_NAME,
    user = settings.DATABASE_USER,
    password = settings.DATABASE_PASSWORD,
    host = settings.DATABASE_HOST,
    port = settings.DATABASE_PORT,
)

curr = conn.cursor()

def index(request):
    return render(request, 'index.html')

def test(request):
    try:
        curr.execute("DELETE FROM PESERTA_MENDAFTAR_EVENT WHERE nomor_peserta = 63")
    except Exception as e:
        print(e)
        curr.execute("ROLLBACK")
    
    return HttpResponse()
