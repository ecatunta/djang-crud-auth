from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import MenuInsert
from .models import Plato
from django.contrib import messages
from django.http import HttpResponse

import datetime

# Create your views here.


def home(request):
    # return HttpResponse('<h1>Hello world</h1>')
    return render(request, 'home.html')


def signup(request):
    # ingresar a la pagina signup
    if request.method == 'GET':
        print('enviando formulario')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        # obtener datos del formulario, metodo POST
        print(request.POST)
        print('obteniendo datos')
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)  # para crear cookies
                # return HttpResponse('User created successfully')
                return redirect('tasks')
            except:
                # return HttpResponse ('Username already exists')
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        # return HttpResponse('Password do not match')
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })


def tasks(request):
    return render(request, 'tasks.html')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        print(request.POST)
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')


def insert_record(request):

    if request.method == 'GET':
        return render(request, 'menu.html')
    else:
        # print (request.POST)
        save_record = MenuInsert()
        save_record.plato = request.POST['plato']
        save_record.tipo = request.POST['tipo']
        save_record.save()
        messages.success(request, 'Record Saved Successfully...')
        return render(request, 'menu.html')


def listar_platos(request):
    platos = Plato.objects.all()
    return render(request, 'listaPlatos.html', {"platos": platos})


def list_menu(request):
    # se debe usar el simbolo '-' para filtrar de forma descendente
    list_menu = Plato.objects.order_by('-fecha_registro')
    return render(request, 'listaPlatos.html', {"platos": list_menu})


def menu2(request):
    cadena_contenido_princ = ''
    hora_actual = datetime.datetime.now()  # 2023-09-22 15:14:56.241033

    if request.method == 'GET':
        return render(request, 'menu2.html')
    else:
        try:
            # obtener los valores del formulario
            tipo_producto = request.POST['tipo']
            nombre_platillo = request.POST['plato']
            contenido_principal = request.POST.getlist('contenido[]')
            categoria = request.POST['clase']
            nivel_mp = request.POST['costo']
            estado = request.POST['activo']

            # validaciones del lado servidor
            if (nombre_platillo == ''):
                return render(request, 'menu2.html', {
                    'Error': 'Debe registrar el nombre del producto/platillo'
                })

            if (len(contenido_principal) == 0):
                return render(request, 'menu2.html', {
                    'Error': 'Debe eligir al menos un contenido'
                })

        except:
            return render(request, 'menu2.html', {
                'Error': 'Por favor elija el tipo de producto',
                'producto':''
            })

        print(request.POST)
        savePlato = Plato()

        savePlato.tipo = tipo_producto
        savePlato.plato = nombre_platillo        
        savePlato.clase = categoria
        savePlato.costo = nivel_mp
        savePlato.estado = estado
        # savePlato.fecha_registro = '2023-09-22 15:02:25'
        savePlato.fecha_registro = hora_actual        

        for item in contenido_principal:
            cadena_contenido_princ = cadena_contenido_princ+item+','
        savePlato.contenido = cadena_contenido_princ[:-1]

        savePlato.save()
        return redirect('listar')
