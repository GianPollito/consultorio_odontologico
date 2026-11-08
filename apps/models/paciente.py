from django.db import models

class Paciente(models.Model):
    """
    Modelo 01: Paciente
    Registra los datos personales y de contacto del paciente atendido en el consultorio.
    """
    id = models.BigAutoField(primary_key=True)
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    correo = models.EmailField(verbose_name="Correo Electrónico")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        db_table = 'pacientes'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.dni})"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
