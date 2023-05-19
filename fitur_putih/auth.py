from django.contrib.auth.backends import BaseBackend
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

def login_required(role):
    def inner(func):
        def inner1(*args, **kwargs):
            id = args[0].COOKIES.get('id', None)
            if id == None:
                messages.error(args[0],"Silahkan login terlebih dahulu")
                return HttpResponseRedirect(reverse("fitur_putih:login"))
            
            user = authenticateWithId(id)
            if user == None:
                messages.error(args[0],"Silahkan login terlebih dahulu")
                return HttpResponseRedirect(reverse("fitur_putih:login"))
            
            if not check_role(args[0], role, id):
                messages.error(args[0], "Silahkan login terlebih dahulu")
                return HttpResponseRedirect(reverse("fitur_putih:login"))
            
            return func(*args, **kwargs)
        return inner1
    return inner

def logout():
    response = HttpResponseRedirect(reverse('fitur_putih:login'))
    response.set_cookie('id', 'id', expires='Thu, 01-Jan-1970 00:00:00 GMT')
    return response

def get_role(request):
    id = request.COOKIES['id']
    if check_role(request, "ATLET", id):
        return "ATLET"
    elif check_role(request, "PELATIH", id):
        return "PELATIH"
    elif check_role(request, "UMPIRE", id):
        return "UMPIRE"

def check_role(request, role, id):
    query = f"SELECT * FROM {role} AS X WHERE X.id = \'{id}\'"
    curr.execute(query)
    lst = curr.fetchall()
    return len(lst) != 0
    
    