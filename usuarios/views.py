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

    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':

        nombre = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        tipo_documento = request.POST.get('tipo_documento')
        numero_documento = request.POST.get('numero_documento')
        correo = request.POST.get('correo')
        rol = request.POST.get('rol')
        telefono = request.POST.get('telefono')
        edad = request.POST.get('edad')
        peso = request.POST.get('peso')
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

        # --- Validaciones por rol ---
        ficha = centro = dependencia = tipo_contrato = especialidad = None
        tipo = request.POST.get('tipoContrato')

        if rol == 'Aprendiz':
            ficha = Ficha.objects.filter(numero=request.POST.get('ficha') or 0).first()
            if not ficha:
                messages.error(request, 'El número de ficha no existe')
                return redirect('registro')

        elif rol == 'Funcionario':
            centro = CentroFormacion.objects.filter(nombre=request.POST.get('centro')).first()
            dependencia = Dependencia.objects.filter(nombre=request.POST.get('dependencia')).first()
            tipo_contrato = TipoContrato.objects.filter(
                nombre__iexact='Planta' if tipo == 'planta' else 'Contrato').first()

            if not centro or not dependencia or not tipo_contrato:
                messages.error(request, 'Centro, dependencia o tipo de contrato no válidos')
                return redirect('registro')

            if tipo == 'contrato' and not (request.POST.get('fecha_inicio')
                                           and request.POST.get('fecha_fin')
                                           and request.POST.get('numero_contrato')):
                messages.error(request, 'Completa los datos del contrato')
                return redirect('registro')

        elif rol == 'Entrenador':
            especialidad = Especialidad.objects.first()
            if not especialidad:
                messages.error(request, 'No hay especialidades creadas')
                return redirect('registro')

        # --- Crear usuario y su perfil ---
        with transaction.atomic():
            usuario = Usuario.objects.create_user(
                correo_institucional=correo,
                password=password,
                nombre=nombre,
                apellidos=apellidos,
                telefono=telefono or None,
                tipo_documento_id=tipo_documento,
                numero_documento=numero_documento,
                peso=peso or None,
                tipo_usuario=TipoUsuario.objects.get(nombre__iexact=rol),
            )

            if rol == 'Aprendiz':
                Aprendiz.objects.create(usuario=usuario, ficha=ficha)

            elif rol == 'Entrenador':
                Entrenador.objects.create(usuario=usuario, especialidad=especialidad)

            elif rol == 'Funcionario':
                Funcionario.objects.create(usuario=usuario, dependencia=dependencia,
                                           centro=centro, tipo_contrato=tipo_contrato)
                if tipo == 'contrato':
                    Contrato.objects.create(
                        usuario=usuario,
                        numero=request.POST.get('numero_contrato'),
                        fecha_inicio=request.POST.get('fecha_inicio'),
                        fecha_fin=request.POST.get('fecha_fin'),
                    )

        messages.success(request, 'Te has registrado correctamente')
        return redirect('inicio')

    return render(request, 'registro.html', {
        'title': 'Registro',
        'tipos_documento': TipoDocumento.objects.all(),
        'centros': CentroFormacion.objects.all(),
        'dependencias': Dependencia.objects.select_related('centro'),
    })