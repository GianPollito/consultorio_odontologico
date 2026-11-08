from django.db import models

class Cita(models.Model):
    """
    Modelo 04: Cita
    Registra la programación y atención de citas odontológicas entre un paciente y un odontólogo.
    """
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Atendida', 'Atendida'),
        ('Cancelada', 'Cancelada'),
    ]

    id = models.BigAutoField(primary_key=True)
    paciente = models.ForeignKey(
        'apps.Paciente',
        on_delete=models.CASCADE,
        related_name='citas',
        verbose_name="Paciente"
    )
    odontologo = models.ForeignKey(
        'apps.Odontologo',
        on_delete=models.CASCADE,
        related_name='citas',
        verbose_name="Odontólogo"
    )
    fecha = models.DateField(verbose_name="Fecha de Atención")
    hora = models.TimeField(verbose_name="Hora de Atención")
    motivo = models.CharField(max_length=200, verbose_name="Motivo de Consulta")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente', verbose_name="Estado")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")

    class Meta:
        db_table = 'citas'
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f"Cita #{self.id} - {self.paciente.nombre_completo} con {self.odontologo.nombre_completo} ({self.fecha})"
