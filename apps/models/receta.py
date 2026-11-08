from django.db import models

class Receta(models.Model):
    """
    Modelo 07: Receta
    Registra la prescripción médica de medicamentos indicada al paciente tras un diagnóstico clínico.
    """
    id = models.BigAutoField(primary_key=True)
    diagnostico = models.ForeignKey(
        'apps.Diagnostico',
        on_delete=models.CASCADE,
        related_name='recetas',
        verbose_name="Diagnóstico"
    )
    medicamento = models.CharField(max_length=150, verbose_name="Medicamento Indicado")
    dosis = models.CharField(max_length=100, verbose_name="Dosis Prescrita")
    frecuencia = models.CharField(max_length=100, verbose_name="Frecuencia de Administración")
    duracion = models.CharField(max_length=100, verbose_name="Duración del Tratamiento")
    indicaciones = models.TextField(verbose_name="Indicaciones Adicionales")

    class Meta:
        db_table = 'recetas'
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'
        ordering = ['-id']

    def __str__(self):
        return f"{self.medicamento} ({self.dosis} c/{self.frecuencia}) - Diag #{self.diagnostico_id}"
