from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from movieclub.models import Movie, Person
import requests
import chardet
import datetime
from random import randint

# visit_count = 0

# Create your views here.


def account(request):
    return render(request, 'movieclub/index.html')


def index(request):
    if not request.user.is_authenticated:
        return redirect(account)
    else:
        url = 'http://api.themoviedb.org/3/discover/movie'

        for page in range(1, 3):
            params = {
                'api_key': '51aad3497f36ee29ca6359394cc828e4',
                'sort_by': 'popularity.desc',
                'page': page,
                'language': 'es-ES'
            }
            r = requests.get(url, params=params)
            movies = r.json()

            for movie in movies['results']:
                existe = Movie.objects.filter(codigo=movie['id']).count()
                if existe == 0:
                    director = Person()
                    director.save()
                    pelicula = Movie(name=movie['title'], desc=movie['overview'], release=movie['release_date'],
                                     poster=movie['poster_path'], rating=movie['vote_average'], director=director, codigo=movie['id'])
                    pelicula.save()

    peliculas_top = Movie.objects.raw('SELECT * FROM movieclub_movie ORDER BY rating DESC LIMIT 0,10;')
    context = {
        'peliculas': Movie.objects.all()[:10],
        'user_name': request.user.get_short_name(),
        'peliculas_top': peliculas_top
    }
    return render(request, 'movieclub/inicio.html', context)

# Para pasar de la pantalla de inicio a login (Cerrar sesión)


@login_required
def log_out(request):
    logout(request)
    return redirect(account)

# Para pasar de la pantalla de login a inicio (Iniciar sesión)
# Para entrar a la aplicación


def inicio(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context = {
                'user_name': request.user.get_short_name()
            }
            return redirect(index)
        else:
            return redirect(account)


def movpage(request, pelicula):
    movie = Movie.objects.get(codigo=pelicula)
    if movie.video == '':
        url = 'http://api.themoviedb.org/3/movie/' + str(pelicula) + '/videos'
        params = {
            'api_key': '51aad3497f36ee29ca6359394cc828e4',
            'language': 'es-ES'
        }
        r = requests.get(url, params=params)
        videos = r.json()
        resultados = videos['results']
        if len(resultados) > 0:
            info = resultados[0]
            link = info['key']
            movie.video = link
    movie.save()

    url = 'http://api.themoviedb.org/3/movie/' + str(pelicula) + '/credits'
    params = {
            'api_key': '51aad3497f36ee29ca6359394cc828e4',
            'language': 'es-ES'
        }
    r = requests.get(url, params=params)
    result = r.json()
    if 'status_code' in result:
        context = {
            'movie': movie,
            'user_name': request.user.get_short_name()
        }
        return render(request, 'movieclub/movpage.html', context)
    reparto = result['cast'][:4]
    for persona in result['crew']:
        if persona['job'] == 'Director':
            movie.director.name = persona['name']
            break
    context = {
        'cast': reparto,
        'movie': movie,
        'user_name': request.user.get_short_name()
    }
    return render(request, 'movieclub/movpage.html', context)


def psearch(request):
    context = {}
    url = 'http://api.themoviedb.org/3/search/movie'
    query = request.POST['query']
    context['user_name'] = request.user.get_short_name()
    context['query'] = query
    params = {
        'api_key': '51aad3497f36ee29ca6359394cc828e4',
        'language': 'es-ES',
        'query': query
    }
    r = requests.get(url, params=params)
    ok = r.json()
    if ok['total_results'] > 0:
        peliculas = ok['results']
        context['resmovies'] = peliculas
        for movie in peliculas:
            existe = Movie.objects.filter(codigo=movie['id']).count()
            if existe == 0:
                director = Person()
                director.save()
                fecha = '1878-01-01' if movie['release_date'] == '' else movie['release_date']
                portada = '/404' if movie['poster_path'] == '' else movie['poster_path']
                pelicula = Movie(name=movie['title'], desc=movie['overview'], release=fecha,poster=portada, rating=movie['vote_average'], director=director, codigo=movie['id'])
                pelicula.save()

    url = 'http://api.themoviedb.org/3/search/person'
    r = requests.get(url, params=params)
    ok = r.json()
    if ok['total_results'] > 0:
        personas = ok['results']
        context['respeople'] = personas
        for persona in personas:
            existe = Person.objects.filter(name=persona['name']).count()
            if existe == 0:
                person = Person(name=persona['name'])
                person.save()

    context['user_name'] = request.user.get_short_name()
    return render(request, 'movieclub/sresults.html', context)




def manage(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request, 'movieclub/manage.html', {'user_name': request.user.get_short_name()})
        else:
            return redirect(index)
    else:
        return redirect(account)
            


def manmov(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            context = {
                'user_name': request.user.get_short_name(),
                'movies': Movie.objects.all()
            }
            return render(request, 'movieclub/filmmanage.html', context)
        else:
            return redirect(index)
    else:
        return redirect(account)




def delmov(request, pelicula):
    if request.user.is_authenticated:
        if request.user.is_staff:
            peli = Movie.objects.filter(codigo=pelicula)
            peli.delete()
            return redirect(manmov)
        else:
            return redirect(index)
    else:
        return redirect(account)



def filmform(request, pelicula):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if pelicula == 0:
                context = { 'user_name': request.user.get_short_name()}
                return render(request, 'movieclub/filmmanageform.html', context)
            else:
                peli = Movie.objects.get(codigo=pelicula)
                context = { 'user_name': request.user.get_short_name(),
                            'movie': peli,
                }
                return render(request, 'movieclub/filmmanageform.html', context)
        else:
            return redirect(index)
    else:
        return redirect(account)






def p_filmform(request, pelicula):
    if request.user.is_authenticated:
        if request.user.is_staff:

            nombre = request.POST['input_filmname']
            url = request.POST['input_filmvid']
            descrip = request.POST['input_filmdesc']
            #date = request.POST['input_filmdate']
            #date = request.POST.get('input_filmdate', '1878-01-01')
            date = request.POST.get('input_filmdate')
            print(date)
            rat = request.POST['input_filmrat']

            if pelicula != 0:
                

                peli = Movie.objects.get(codigo=pelicula)
                peli.video = peli.video if url is '' else url
                peli.desc = peli.desc if descrip is '' else descrip
                peli.release = peli.release if date is '' else date
                peli.rating = peli.rating if rat is '' else rat
                peli.save()
                
            else:
                urlb = 'http://api.themoviedb.org/3/search/movie'
                params = {
                    'language': 'es-ES',
                    'api_key': '51aad3497f36ee29ca6359394cc828e4',
                    'query': nombre
                }
                r = requests.get(urlb, params=params)
                ok = r.json()
                ok = ok['results']
                if len(ok) != 0:
                    ok = ok[0]
                    director = Person()
                    director.save()
                    peli = Movie(name=nombre, video=url, director=director)
                    peli.desc = ok['overview'] if descrip == '' else descrip
                    peli.release = ok['release_date'] if date == '' else date
                    peli.rating = ok['vote_average'] if rat == '' else rat
                    peli.codigo = ok['id']
                    peli.save()
                else:
                    director = Person()
                    director.save()
                    peli = Movie(name=nombre, video=url, director=director)
                    peli.desc = descrip
                    peli.release = '1878-01-01' if date is '' else date
                    peli.rating = 5 if rat is '' else rat
                    peli.codigo = randint(500000, 1000000)
                    peli.save()
            return redirect(manmov)
        else:
            return redirect(index)
    else:
        return redirect(account)





def manuser(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            context = {
                'user_name': request.user.get_short_name(),
                'users': User.objects.all()
            }
            return render(request, 'movieclub/usermanage.html', context)
        else:
            return redirect(index)
    else:
        return redirect(account)



def deluser(request, user):
    if request.user.is_authenticated:
        if request.user.is_staff:
            usuario = User.objects.get(id=user)
            usuario.delete()
            return redirect(manuser)
        else:
            return redirect(index)
    else:
        return redirect(account)



def userform(request, user):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if user == 0:
                context = { 'user_name': request.user.get_short_name()}
                return render(request, 'movieclub/usermanageform.html', context)
            else:
                usuario = User.objects.get(id=user)
                context = { 'user_name': request.user.get_short_name(),
                            'usuario': usuario,
                }
                return render(request, 'movieclub/usermanageform.html', context)
        else:
            return redirect(index)
    else:
        return redirect(account)



def p_userform(request, user):
    if request.user.is_authenticated:
        if request.user.is_staff:

            username = request.POST['input_username']
            if user == 0:
                password = request.POST['input_password']
            first = request.POST['input_name']
            last = request.POST['input_lastname']
            email = request.POST['input_email']
            staff = request.POST.getlist('staff')
            staff = False if len(staff) == 0 else True
            active = request.POST.getlist('active')
            active = False if len(active) == 0 else True
            #staff = request.POST.get('staff', True)
            #active = request.POST.get('active', True)
            #staff = True if request.POST.get('staff', False) == ' False ' else False
            #active = True if request.POST.get('active', False) == ' False ' else False

            print('---------------------------------' + active.__class__.__name__ + '--------------------------------')

            print('---------------------------------' + staff.__class__.__name__ + '--------------------------------')

            if user != 0:
                
                usuario = User.objects.get(id=user)
                usuario.username = usuario.username if username is '' else username
                usuario.first_name = usuario.first_name if first is '' else first
                usuario.last_name = usuario.last_name if last is '' else last
                usuario.email = usuario.email if email is '' else email
                usuario.is_staff = staff
                usuario.is_active = active
                usuario.save()
            else:
                usuario = User.objects.create_user(username, email, password, first_name=first, last_name=last, is_active=active, is_staff=staff)
                usuario.save()
            return redirect(manuser)
        else:
            return redirect(index)
    else:
        return redirect(account)