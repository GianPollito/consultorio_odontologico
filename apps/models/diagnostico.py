from django.db import models

class Diagnostico(models.Model):
    """
    Modelo 05: Diagnóstico
    Registra la evaluación clínica emitida por el odontólogo al atender una cita.
    """
    id = models.BigAutoField(primary_key=True)
    cita = models.ForeignKey(
        'apps.Cita',
        on_delete=models.CASCADE,
        related_name='diagnosticos',
        verbose_name="Cita"
    )
    descripcion = models.TextField(verbose_name="Diagnóstico Clínico")
    recomendaciones = models.TextField(verbose_name="Recomendaciones")
    fecha = models.DateField(verbose_name="Fecha del Diagnóstico")

    class Meta:
        db_table = 'diagnosticos'
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'
        ordering = ['-fecha', '-id']

    def __str__(self):
        return f"Diagnóstico #{self.id} (Cita #{self.cita_id} - {self.cita.paciente.nombre_completo})"
