from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import psycopg2
import psycopg2.extras
import json
from datetime import date

conn = psycopg2.connect(
    database = settings.DATABASE_NAME,
    user = settings.DATABASE_USER,
    password = settings.DATABASE_PASSWORD,
    host = settings.DATABASE_HOST,
    port = settings.DATABASE_PORT,
)

curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Create your views here.

def read_enrolled_event(request):
    query = ("SELECT * "
            + "FROM PESERTA_MENDAFTAR_EVENT AS PME, EVENT AS E "
            + "WHERE PME.nama_event=E.nama_event " 
            + "AND PME.tahun=E.tahun")
    curr.execute(query)
    lst = curr.fetchall()
    json_format(lst)
    return HttpResponse(json.dumps(lst), content_type = "application/json")

def json_format(lst):
    for i in range(len(lst)):
        lst[i] = dict(lst[i])
        change_date_format(lst[i])

def change_date_format(param):
    for key in param:
        if(isinstance(param[key], date)):
            param[key] = param[key].strftime('%d-%m-%Y')
