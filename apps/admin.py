from django.contrib import admin
from apps.models import (
    Paciente,
    Odontologo,
    Especialidad,
    Cita,
    Diagnostico,
    Tratamiento,
    Receta
)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'dni', 'nombres', 'apellidos', 'telefono', 'correo', 'created_at')
    search_fields = ('dni', 'nombres', 'apellidos', 'telefono', 'correo')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'estado')
    search_fields = ('nombre',)
    list_filter = ('estado',)

@admin.register(Odontologo)
class OdontologoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_colegiatura', 'nombres', 'apellidos', 'especialidad', 'telefono', 'estado')
    search_fields = ('numero_colegiatura', 'nombres', 'apellidos', 'telefono')
    list_filter = ('especialidad', 'estado')

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'odontologo', 'fecha', 'hora', 'estado', 'motivo')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'paciente__dni', 'odontologo__nombres', 'motivo')
    list_filter = ('estado', 'fecha', 'odontologo')
    date_hierarchy = 'fecha'

@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cita', 'fecha', 'descripcion_corta')
    search_fields = ('cita__paciente__nombres', 'cita__paciente__apellidos', 'descripcion')
    list_filter = ('fecha',)
    date_hierarchy = 'fecha'

    def descripcion_corta(self, obj):
        return (obj.descripcion[:60] + '...') if len(obj.descripcion) > 60 else obj.descripcion
    descripcion_corta.short_description = "Diagnóstico"

@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'diagnostico', 'fecha_inicio', 'fecha_fin', 'costo', 'estado')
    search_fields = ('nombre', 'diagnostico__cita__paciente__nombres')
    list_filter = ('estado', 'fecha_inicio')

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('id', 'medicamento', 'dosis', 'frecuencia', 'duracion', 'diagnostico')
    search_fields = ('medicamento', 'diagnostico__cita__paciente__nombres')
