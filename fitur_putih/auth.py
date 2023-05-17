from django.contrib.auth.backends import BaseBackend
import psycopg2.extras
import psycopg2
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

conn = psycopg2.connect(
    database = settings.DATABASE_NAME,
    user = settings.DATABASE_USER,
    password = settings.DATABASE_PASSWORD,
    host = settings.DATABASE_HOST,
    port = settings.DATABASE_PORT,
)

curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def authenticate(nama, email):
    query = f'SELECT * FROM MEMBER AS M WHERE M.email = \'{email}\' AND M.nama = \'{nama}\''
    curr.execute(query)
    lst = curr.fetchall()
    if len(lst) == 0:
        return None
    return dict(lst[0])

def login(id):
    response = HttpResponseRedirect(reverse("example_app:index"))
    response.set_cookie('id', id)
    return response

def authenticateWithId(id):
    query = f'SELECT * FROM MEMBER AS M WHERE M.id = \'{id}\''
    curr.execute(query)
    lst = curr.fetchall()
    if len(lst) == 0:
        return None
    return dict(lst[0])

def login_required(func):
    def inner1(*args, **kwargs):
        id = args[0].COOKIES.get('id', None)
        if(id == None or authenticateWithId(id) == None):
            return HttpResponseRedirect(reverse("fitur_putih:login"))
        return func(*args, **kwargs)

    return inner1

def logout():
    response = HttpResponseRedirect(reverse('fitur_putih:login'))
    response.set_cookie('id', 'id', expires='Thu, 01-Jan-1970 00:00:00 GMT')
    return response
    
    
    