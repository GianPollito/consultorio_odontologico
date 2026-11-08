from django.db import models

class Odontologo(models.Model):
    """
    Modelo 02: Odontólogo
    Registra al profesional odontólogo colegiado, su especialidad y estado de actividad.
    """
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    id = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    numero_colegiatura = models.CharField(max_length=30, unique=True, verbose_name="Número de Colegiatura")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    correo = models.EmailField(verbose_name="Correo Electrónico")
    especialidad = models.ForeignKey(
        'apps.Especialidad',
        on_delete=models.PROTECT,
        related_name='odontologos',
        verbose_name="Especialidad"
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', verbose_name="Estado")

    class Meta:
        db_table = 'odontologos'
        verbose_name = 'Odontólogo'
        verbose_name_plural = 'Odontólogos'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"Dr(a). {self.nombres} {self.apellidos} - Col. {self.numero_colegiatura}"

    @property
    def nombre_completo(self):
        return f"Dr(a). {self.nombres} {self.apellidos}"
