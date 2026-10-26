from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import (
    Aprendiz,
    CentroFormacion,
    Contrato,
    Dependencia,
    Entrenador,
    Especialidad,
    Ficha,
    Funcionario,
    Jornada,
    Modalidad,
    NivelFormacion,
    Programa,
    TipoContrato,
    TipoDocumento,
    TipoUsuario,
    Usuario,
)

# Register your models here.


# ---------------------------------------------------------------------------
# Usuario (modelo personalizado)
# Se hereda de UserAdmin para que la contraseña se guarde con hash
# y no en texto plano. Con un ModelAdmin normal quedaría sin cifrar.
# ---------------------------------------------------------------------------
class UsuarioCreationForm(UserCreationForm):    #UserCreationForm es el formulario que Django usa para crear usuarios y que viene con las contraseñas y con model se le esta indicando que use el modelo que se creo para usuarios y con con fields los campos adiciones a password que debe incluir
    class Meta:
        model = Usuario
        fields = ("correo_institucional", "nombre", "apellidos")


class UsuarioChangeForm(UserChangeForm):     #UserChangeForm es el formulario para editar un usuario existente. Muestra la contraseña como un hash de solo lectura, con un enlace para cambiarla, en lugar de mostrarla en un campo editable. fields = "__all__" incluye todos los campos del model
    class Meta:
        model = Usuario
        fields = "__all__"


class UsuarioAdmin(BaseUserAdmin):      #BaseUserAdmin es el UserAdmin de Django, que ya sabe manejar contraseñas con hash. Por eso se hereda de él y no de ModelAdmin
    form = UsuarioChangeForm            #UsuarioChangeForm es el formulario que se usa al editar un usuario.
    add_form = UsuarioCreationForm      #UsuarioCreationForm es el formulario que se usa al crear uno nuevo.

    readonly_fields = ("last_login",)      #readonly_fields hace que last_login, la fecha del último inicio de sesión, se vea pero no se pueda modificar.
    ordering = ("correo_institucional",)   #ordena la lista de usuarios por correo
    list_display = (
        "correo_institucional",
        "nombre",
        "apellidos",
        "tipo_usuario",
        "is_active",
        "is_staff",
    )     #son las columnas que se van a mostrar.
    list_filter = ("tipo_usuario", "is_active", "is_staff")    #son los filtros del panel derecho.
    search_fields = (
        "correo_institucional",
        "nombre",
        "apellidos",
        "numero_documento",
    )      #son los campos que se usan para buscar a un usuario en la barra de busqueda

    # Formulario de edición
    fieldsets = (
        (None, {"fields": ("correo_institucional", "password")}),
        (
            "Datos personales",
            {
                "fields": (
                    "nombre",
                    "apellidos",
                    "telefono",
                    "tipo_documento",
                    "numero_documento",
                    "fecha_nacimiento",
                    "tipo_usuario",
                )
            },
        ),
        ("Datos físicos", {"fields": ("peso", "altura", "grasa_corporal")}),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Fechas importantes", {"fields": ("last_login",)}),
    )

    # Formulario de creación
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "correo_institucional",
                    "nombre",
                    "apellidos",
                    "tipo_usuario",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


# ---------------------------------------------------------------------------
# Catálogos
# ---------------------------------------------------------------------------
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


class TipoContratoAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


class NivelFormacionAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


class ModalidadAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


class JornadaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre", "descripcion")


# ---------------------------------------------------------------------------
# Estructura institucional
# ---------------------------------------------------------------------------
class CentroFormacionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ubicacion")
    search_fields = ("nombre", "ubicacion")


class DependenciaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "centro")
    search_fields = ("nombre", "centro__nombre")
    list_filter = ("centro",)


# ---------------------------------------------------------------------------
# Formación académica
# ---------------------------------------------------------------------------
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "nivel", "duracion", "centro")
    search_fields = ("codigo", "nombre")
    list_filter = ("nivel", "centro")


class FichaAdmin(admin.ModelAdmin):
    list_display = (
        "numero",
        "programa",
        "modalidad",
        "jornada",
        "fecha_inicio",
        "fecha_fin",
    )
    search_fields = ("numero", "programa__nombre")
    list_filter = ("modalidad", "jornada", "programa")


# ---------------------------------------------------------------------------
# Perfiles
# ---------------------------------------------------------------------------
class AprendizAdmin(admin.ModelAdmin):
    list_display = ("usuario", "ficha")
    search_fields = (
        "usuario__nombre",
        "usuario__apellidos",
        "usuario__correo_institucional",
        "ficha__numero",
    )
    list_filter = ("ficha",)


class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "dependencia", "centro", "tipo_contrato")
    search_fields = (
        "usuario__nombre",
        "usuario__apellidos",
        "usuario__correo_institucional",
    )
    list_filter = ("centro", "dependencia", "tipo_contrato")


class ContratoAdmin(admin.ModelAdmin):
    list_display = ("numero", "usuario", "fecha_inicio", "fecha_fin")
    search_fields = ("numero", "usuario__nombre", "usuario__apellidos")
    list_filter = ("fecha_inicio", "fecha_fin")


class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ("usuario", "especialidad")
    search_fields = (
        "usuario__nombre",
        "usuario__apellidos",
        "usuario__correo_institucional",
        "especialidad__nombre",
    )
    list_filter = ("especialidad",)


# ---------------------------------------------------------------------------
# Registro
# ---------------------------------------------------------------------------
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(TipoUsuario, TipoUsuarioAdmin)
admin.site.register(TipoContrato, TipoContratoAdmin)
admin.site.register(NivelFormacion, NivelFormacionAdmin)
admin.site.register(Modalidad, ModalidadAdmin)
admin.site.register(Jornada, JornadaAdmin)
admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(CentroFormacion, CentroFormacionAdmin)
admin.site.register(Dependencia, DependenciaAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Ficha, FichaAdmin)
admin.site.register(Aprendiz, AprendizAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Entrenador, EntrenadorAdmin)