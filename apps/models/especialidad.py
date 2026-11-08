from django.db import models

class Especialidad(models.Model):
    """
    Modelo 03: Especialidad
    Define las especialidades odontológicas disponibles en la clínica (Ortodoncia, Endodoncia, etc.).
    """
    ESTADO_CHOICES = [
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
    ]

    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de Especialidad")
    descripcion = models.TextField(verbose_name="Descripción")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activa', verbose_name="Estado")

    class Meta:
        db_table = 'especialidades'
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
