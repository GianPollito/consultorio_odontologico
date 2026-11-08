from django.db import models

class Tratamiento(models.Model):
    """
    Modelo 06: Tratamiento
    Registra el plan o procedimiento terapéutico derivado de un diagnóstico, con fechas y costos.
    """
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En proceso', 'En proceso'),
        ('Finalizado', 'Finalizado'),
    ]

    id = models.BigAutoField(primary_key=True)
    diagnostico = models.ForeignKey(
        'apps.Diagnostico',
        on_delete=models.CASCADE,
        related_name='tratamientos',
        verbose_name="Diagnóstico"
    )
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Tratamiento")
    descripcion = models.TextField(verbose_name="Descripción del Procedimiento")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Finalización")
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo del Tratamiento (S/.)")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente', verbose_name="Estado")

    class Meta:
        db_table = 'tratamientos'
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'
        ordering = ['-fecha_inicio', '-id']

    def __str__(self):
        return f"{self.nombre} - S/. {self.costo} ({self.estado})"
