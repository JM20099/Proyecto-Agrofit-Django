from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render

from .models import (
    Aprendiz, CentroFormacion, Contrato, Dependencia, Entrenador,
    Especialidad, Ficha, Funcionario, TipoContrato, TipoDocumento,
    TipoUsuario, Usuario,
)


# Create your views here.
def inicio(request):

    return render(request, 'inicio_de_sesion.html', {
    }) 

def registro(request):

    return render(request, 'registro.html', {
    }) 

def registro(request):

    if request.method == 'POST':

        nombre = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        telefono = request.POST.get('telefono')
        tipo_documento = request.POST.get('tipo_documento')
        numero_documento = request.POST.get('numero_documento')
        correo = request.POST.get('correo')
        rol = request.POST.get('rol')
        telefono = request.POST.get('telefono')
        fecha_nacimiento = request.POST.get('fechaNacimiento')
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        grasa_corporal = request.POST.get('grasaCorporal')
        password = request.POST.get('password')

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

        usuarios = Usuario(
                correo_institucional=correo,
                password=password,
                nombre=nombre,
                apellidos=apellidos,
                telefono=telefono,
                tipo_documento_id=tipo_documento,
                numero_documento=numero_documento,
                peso=peso,
                altura=altura,
                grasa_corporal=grasa_corporal,
                tipo_usuario=TipoUsuario.objects.get(nombre__iexact=rol),
                fecha_nacimiento=fecha_nacimiento
            )

        messages.success(request, 'Te has registrado correctamente')
        return redirect('inicio')

    return render(request, 'registro.html', {
        'title': 'Registro',
        'tipos_documento': TipoDocumento.objects.all(),
        'centros': CentroFormacion.objects.all(),
        'dependencias': Dependencia.objects.select_related('centro'),
        'tipos_usuario': TipoUsuario.objects.all(),
        'tipos_contrato': TipoContrato.objects.all(),
    })