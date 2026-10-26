from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
 
 
# ---------------------------------------------------------------------------
# Catálogos básicos
# ---------------------------------------------------------------------------
class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=50)
 
    class Meta:
        verbose_name = "tipo de documento"
        verbose_name_plural = "tipos de documento"
 
    def __str__(self):
        return self.nombre
 
 
class TipoUsuario(models.Model):
    """Aprendiz, Funcionario, Entrenador."""
    nombre = models.CharField(max_length=50)
 
    class Meta:
        verbose_name = "tipo de usuario"
        verbose_name_plural = "tipos de usuario"
 
    def __str__(self):
        return self.nombre
 
 
class UsuarioManager(BaseUserManager):
    use_in_migrations = True
 
    def _crear(self, correo_institucional, password, **extra):
        if not correo_institucional:
            raise ValueError("El correo institucional es obligatorio")
        correo_institucional = self.normalize_email(correo_institucional)
        usuario = self.model(correo_institucional=correo_institucional, **extra)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario
 
    def create_user(self, correo_institucional, password=None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        return self._crear(correo_institucional, password, **extra)
 
    def create_superuser(self, correo_institucional, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self._crear(correo_institucional, password, **extra)
 
 
class Usuario(AbstractBaseUser, PermissionsMixin):

    is_active = models.BooleanField(default=True)     #Indica si la cuenta está habilitada. Si se pone en False, el usuario no puede iniciar sesión, pero sus datos y su historial se conservan
    is_staff = models.BooleanField(default=False)     #Indica si el usuario puede entrar al panel de administración

    objects = UsuarioManager()

    # Campo que se usará para iniciar sesión
    USERNAME_FIELD = "correo_institucional"
    
    # Campos obligatorios adicionales que se pedirán al crear un superusuario por consola
    REQUIRED_FIELDS = ["nombre", "apellidos"]

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    correo_institucional = models.EmailField(max_length=50, unique=True)
    tipo_documento = models.ForeignKey(
        TipoDocumento, on_delete=models.PROTECT, related_name="usuarios", null=True, blank=True)
    numero_documento = models.CharField(max_length=50, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
 
    # Datos físicos actuales (el historial va en rutinas.SeguimientoProgreso)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    grasa_corporal = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, default=0
    )
 
    tipo_usuario = models.ForeignKey(
        TipoUsuario, on_delete=models.PROTECT, related_name="usuarios", null=True, blank=True
    )
 
    
 
    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        constraints = [
            models.UniqueConstraint(
                fields=["tipo_documento", "numero_documento"],
                name="uq_usuario_documento",
            )
        ]
 
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
 
   
 
 
# ---------------------------------------------------------------------------
# Estructura institucional (centros, dependencias)
# ---------------------------------------------------------------------------
class CentroFormacion(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
 
    class Meta:
        verbose_name = "centro de formación"
        verbose_name_plural = "centros de formación"
 
    def __str__(self):
        return self.nombre
 
 
class Dependencia(models.Model):
    nombre = models.CharField(max_length=100)
    centro = models.ForeignKey(
        CentroFormacion, on_delete=models.CASCADE, related_name="dependencias"
    )
 
    def __str__(self):
        return f"{self.nombre} ({self.centro})"
 
 
# ---------------------------------------------------------------------------
# Formación académica (programas, fichas)
# ---------------------------------------------------------------------------
class NivelFormacion(models.Model):
    """Técnico, tecnólogo, operario."""
    nombre = models.CharField(max_length=50)
 
    class Meta:
        verbose_name = "nivel de formación"
        verbose_name_plural = "niveles de formación"
 
    def __str__(self):
        return self.nombre
 
 
class Modalidad(models.Model):
    nombre = models.CharField(max_length=100)
 
    class Meta:
        verbose_name_plural = "modalidades"
 
    def __str__(self):
        return self.nombre
 
 
class Jornada(models.Model):
    nombre = models.CharField(max_length=50)
 
    def __str__(self):
        return self.nombre
 
 
class Programa(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=200)
    nivel = models.ForeignKey(
        NivelFormacion, on_delete=models.CASCADE, related_name="programas"
    )
    duracion = models.IntegerField(help_text="Duración en meses")
    centro = models.ForeignKey(
        CentroFormacion, on_delete=models.CASCADE, related_name="programas"
    )
 
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
 
 
class Ficha(models.Model):
    numero = models.IntegerField(unique=True)
    programa = models.ForeignKey(
        Programa, on_delete=models.CASCADE, related_name="fichas"
    )
    modalidad = models.ForeignKey(
        Modalidad, on_delete=models.CASCADE, related_name="fichas"
    )
    jornada = models.ForeignKey(
        Jornada, on_delete=models.CASCADE, related_name="fichas"
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
 
    def __str__(self):
        return str(self.numero)
 
 
# ---------------------------------------------------------------------------
# Perfiles según tipo de usuario
# ---------------------------------------------------------------------------
class Aprendiz(models.Model):
    usuario = models.OneToOneField( Usuario, on_delete=models.CASCADE, related_name="perfil_aprendiz")      #Con OneToOneField, se le dice a la base de datos que un Usuario tiene exactamente un Perfil, y ese Perfil pertenece a un único Usuario.
    ficha = models.ForeignKey(
        Ficha, on_delete=models.CASCADE, related_name="aprendices"
    )
 
    class Meta:
        verbose_name_plural = "aprendices"
 
    def __str__(self):
        return f"{self.usuario} - Ficha {self.ficha}"
 
 
class TipoContrato(models.Model):
    """Contrato, Planta."""
    nombre = models.CharField(max_length=100)
 
    class Meta:
        verbose_name = "tipo de contrato"
        verbose_name_plural = "tipos de contrato"
 
    def __str__(self):
        return self.nombre
 
 
class Funcionario(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_funcionario"
    )
    dependencia = models.ForeignKey(
        Dependencia, on_delete=models.CASCADE, related_name="funcionarios"
    )
    centro = models.ForeignKey(
        CentroFormacion, on_delete=models.CASCADE, related_name="funcionarios"
    )
    tipo_contrato = models.ForeignKey(
        TipoContrato, on_delete=models.PROTECT, related_name="funcionarios"
    )
 
    class Meta:
        verbose_name_plural = "funcionarios"
 
    def __str__(self):
        return str(self.usuario)
 
 
class Contrato(models.Model):
    numero = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    usuario = models.ForeignKey(
        Usuario, on_delete=models.PROTECT, related_name="contratos"
    )
 
    def __str__(self):
        return f"Contrato {self.numero}"
 
 
class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
 
    class Meta:
        verbose_name_plural = "especialidades"
 
    def __str__(self):
        return self.nombre
 
 
class Entrenador(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.PROTECT, related_name="perfil_entrenador"
    )
    especialidad = models.ForeignKey(
        Especialidad, on_delete=models.CASCADE, related_name="entrenadores"
    )
 
    class Meta:
        verbose_name_plural = "entrenadores"
 
    def __str__(self):
        return str(self.usuario)
 