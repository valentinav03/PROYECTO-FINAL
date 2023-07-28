from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import AreaTrabajo, Trabajador, User, AreaEjerce
from .forms import NewUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request, area_id=None):
    areas_trabajo = AreaTrabajo.objects.all()
    trabajadores = Trabajador.objects.all()

    if area_id :
        trabajadores = trabajadores.filter(areaejerce__id_area=area_id)
    else:
        trabajadores = None
        return render(request, 'Index.html',{'areas_trabajo': areas_trabajo})

    # Crear una lista para almacenar la información de los trabajadores
    trabajadores_info = []
    for trabajador in trabajadores:
        # Obtener el objeto de autenticación del trabajador
        try:
            user = User.objects.get(id=trabajador.id_cuenta)
            trabajador_info = {
                'username': user.username,
                'email': user.email,
                'precio': trabajador.precio,
                'experiencia': trabajador.experiencia,
                'descripcion': trabajador.descripcion,
            }
            trabajadores_info.append(trabajador_info)
        except User.DoesNotExist:
            pass

    return render(request, 'Index.html', {'areas_trabajo': areas_trabajo, 'trabajadores': trabajadores_info})


def login_page(request):
    # Código para la vista login_page aquí
    return render(request, 'login.html')

def registro_page(request):
    data = {
        'form': NewUserForm()
    }

    if request.method == 'POST':
        formulario= NewUserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            login(request, user)
            return redirect(to="index")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

def edit_page(request):

    try:
        trabajador = Trabajador.objects.get(id_cuenta=request.user.id)
        es_trabajador = True
    except Trabajador.DoesNotExist:
        es_trabajador = False

    if request.method == 'POST':
        user = request.user

        nuevo_nombre = request.POST.get('username')
        nuevo_email = request.POST.get('email')
        nuevo_telefono = request.POST.get('telefono')
        nueva_direccion = request.POST.get('direccion')
        nuevo_precio = request.POST.get('precio')
        nueva_exp = request.POST.get('Exp')
        nueva_descripcion = request.POST.get('descripcion')

        if nuevo_nombre.strip() and nuevo_nombre != user.username:
            if not User.objects.filter(username=nuevo_nombre).exclude(id=user.id).exists():
                user.username = nuevo_nombre
                user.save()
            
        if nuevo_email.strip():
            user.email = nuevo_email
            user.save()

        if nueva_descripcion and nueva_descripcion.strip():
            trabajador.descripcion = nueva_descripcion
            trabajador.save()

        if nuevo_telefono and nuevo_telefono.strip():
            user.last_name = nuevo_telefono.strip()
            user.save()

        if nueva_direccion and nueva_direccion.strip():
            user.first_name = nueva_direccion.strip()
            user.save()

        if nuevo_precio and nuevo_precio.strip():
            trabajador.precio = nuevo_precio.strip()
            trabajador.save()

        if nueva_exp and nueva_exp.strip():
            trabajador.experiencia = nueva_exp.strip()
            trabajador.save()

        if es_trabajador:
            return render(request, 'editar_perfil.html', {'es_trabajador': es_trabajador, 'trabajador': trabajador})
    
    return render(request, 'editar_perfil.html', {'es_trabajador': es_trabajador})

def trabajador(request):
    areas_trabajo = AreaTrabajo.objects.all()
        
    if request.method == 'POST':
        user = request.user

        nuevo_telefono = request.POST.get('telefono')
        nueva_direccion = request.POST.get('direccion')
        nuevo_trabajo = request.POST.get('area_id')

        if nuevo_telefono and nuevo_telefono.strip():
            user.last_name = nuevo_telefono.strip()
            user.save()

        if nueva_direccion and nueva_direccion.strip():
            user.first_name = nueva_direccion.strip()
            user.save()

        if nuevo_trabajo and nuevo_trabajo.strip():
            trabajador = Trabajador.objects.create(
                id_cuenta=request.user.id,
                precio=0,
                experiencia=0,
                descripcion="",
                calificacion_promedio=3.0
            )
            
            AreaTrabajador= AreaEjerce.objects.create(
                id_area= AreaTrabajo.objects.get(id=nuevo_trabajo),
                id_trabajador= trabajador
            )
            user.save()


        return redirect('editarPerfil')

    return render(request, 'trabajador.html', {'areas_trabajo': areas_trabajo})