from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.decorators import login_required


 
from .models import (
    Aprendiz, CentroFormacion, Contrato, Dependencia, Entrenador,
    Especialidad, Ficha, Funcionario, TipoContrato, TipoDocumento,
    TipoUsuario, Usuario,
)
 
 
# Create your views here.
def inicio(request):
    
    #if request.user.is_authenticated:
        #return redirect('inicio')

    if request.method == 'POST':
        correo = (request.POST.get('correo') or '').strip().lower()
        password = request.POST.get('password')

        # authenticate usa el campo correo_institucional como "username"
        usuario = authenticate(request, username=correo, password=password)

        if usuario is not None:
            login(request, usuario)

            siguiente = request.GET.get('next')
            if siguiente and url_has_allowed_host_and_scheme(siguiente, allowed_hosts={request.get_host()}):    #url_has_allowed_host_and_scheme verifica que la URL de redirección sea segura y esté permitida para evitar ataques de redirección abierta. allowed_hosts={request.get_host()} asegura que la URL de redirección pertenezca al mismo dominio que la aplicación.
                return redirect(siguiente)
            return redirect('home')

        messages.error(request, 'Correo o contraseña incorrectos')
        return redirect('inicio')

    return render(request, 'inicio_de_sesion.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')

def registro_correcto(request):
 
    return render(request, 'registro_correcto.html', {
    })


@login_required
def home(request):
 
    return render(request, 'home.html', {
    })

 
 
 
def registro(request):
 
    if request.method == 'POST':
 
        nombre = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        telefono = request.POST.get('telefono')
        tipo_documento = request.POST.get('tipo_documento')
        numero_documento = request.POST.get('numero_documento')
        correo = (request.POST.get('correo') or '').strip().lower()    #strip() quita los espacios al inicio y al final de un texto y lower() convierte todo el texto a minúsculas
        rol = request.POST.get('rol')
        fecha_nacimiento = request.POST.get('fechaNacimiento')
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        grasa_corporal = request.POST.get('grasaCorporal')
        password = request.POST.get('password')
 
        # Campos según el rol
        numero_ficha = request.POST.get('numeroFicha')
        especialidad = request.POST.get('especialidad')
        dependencia = request.POST.get('dependencia')
        centro = request.POST.get('centro')
        tipo_contrato = request.POST.get('tipoContrato')
        numero_contrato = request.POST.get('numeroContrato')
        fecha_inicio = request.POST.get('fechaInicio')
        fecha_fin = request.POST.get('fechaFin')
 
        # --- Validaciones generales ---
        if rol not in ('Aprendiz', 'Funcionario', 'Entrenador'):
            messages.error(request, 'Selecciona un tipo de rol')
            return redirect('registro')
 
        if Usuario.objects.filter(correo_institucional=correo).exists():
            messages.error(request, 'Este correo ya está registrado')
            return redirect('registro')
 
        if Usuario.objects.filter(tipo_documento_id=tipo_documento,
                                  numero_documento=numero_documento).exists():
            messages.error(request, 'Este documento ya está registrado')
            return redirect('registro')
 
        if rol == 'Aprendiz':
            try:
                ficha = Ficha.objects.get(numero=numero_ficha)
            except (Ficha.DoesNotExist, ValueError):
                messages.error(request, 'El número de ficha ingresado no existe en el sistema')
                return redirect('registro')

        if rol == 'Entrenador' and not (especialidad or '').strip():
                messages.error(request, 'Ingresa la especialidad')
                return redirect('registro')

        if rol == 'Aprendiz' and not correo.endswith('@soy.sena.edu.co'):
                messages.error(request, 'El correo del aprendiz debe terminar en @soy.sena.edu.co')
                return redirect('registro')

        elif rol == 'Entrenador' and not correo.endswith('@sena.edu.co'):
                messages.error(request, 'El correo del entrenador debe terminar en @sena.edu.co')
                return redirect('registro')

        elif rol == 'Funcionario':
                try:
                    validate_email(correo)
                except ValidationError:
                    messages.error(request, 'Ingresa un correo válido')
                    return redirect('registro')
        
        try:
            with transaction.atomic():       #with transaction.atomic() se asegura de que todas las operaciones dentro del bloque se realicen como una sola transacción. Si ocurre un error, se deshacen todos los cambios realizados en la base de datos durante esa transacción.
 
                # create_user guarda el usuario y encripta la contraseña
                usuario = Usuario.objects.create_user(
                    correo_institucional=correo,
                    password=password,
                    nombre=nombre,
                    apellidos=apellidos,
                    telefono=telefono,
                    tipo_documento_id=tipo_documento,
                    numero_documento=numero_documento,
                    peso=peso or None,
                    altura=altura or None,
                    grasa_corporal=grasa_corporal or 0,
                    tipo_usuario=TipoUsuario.objects.get(nombre__iexact=rol),
                    fecha_nacimiento=fecha_nacimiento or None
                )
 
                # --- Perfil según el rol ---
                if rol == 'Aprendiz':
                    Aprendiz.objects.create(
                        usuario=usuario,
                        ficha=ficha
                    )
 
                elif rol == 'Entrenador':
                    especialidad_obj, _ = Especialidad.objects.get_or_create(
                        nombre=especialidad.strip()
                    )

                    Entrenador.objects.create(
                        usuario=usuario,
                        especialidad=especialidad_obj
                    )
 
                elif rol == 'Funcionario':
                    dependencia_obj = Dependencia.objects.get(pk=dependencia)
                    tipo_contrato_obj = TipoContrato.objects.get(nombre__iexact=tipo_contrato)

                    Funcionario.objects.create(
                        usuario=usuario,
                        dependencia=dependencia_obj,
                        centro_id=centro,
                        tipo_contrato=tipo_contrato_obj
                    )
 
                    if tipo_contrato_obj.nombre.lower() == 'contrato':
                        Contrato.objects.create(
                            usuario=usuario,
                            numero=numero_contrato,
                            fecha_inicio=fecha_inicio or None,
                            fecha_fin=fecha_fin or None
                        )
 
        except Exception as e:
            print('--- ERROR EN REGISTRO ---', e)
            messages.error(request, f'Ocurrió un error al registrar: {e}')
            return redirect('registro')
 
        messages.success(request, 'Te has registrado correctamente')
        return redirect('registro_correcto')
 
    return render(request, 'registro.html', {
        'title': 'Registro',
        'tipos_documento': TipoDocumento.objects.all(),
        'centros': CentroFormacion.objects.all(),
        'dependencias': Dependencia.objects.all(),
        'tipos_usuario': TipoUsuario.objects.all(),
        'tipos_contrato': TipoContrato.objects.all(),
        'especialidades': Especialidad.objects.all(),
    })