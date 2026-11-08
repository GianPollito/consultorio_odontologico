"""
Módulo de modelos de la aplicación de Consultorio Odontológico.
Cada modelo se encuentra en su archivo independiente cumpliendo el requerimiento de arquitectura modular.
"""
from .paciente import Paciente
from .especialidad import Especialidad
from .odontologo import Odontologo
from .cita import Cita
from .diagnostico import Diagnostico
from .tratamiento import Tratamiento
from .receta import Receta

__all__ = [
    'Paciente',
    'Especialidad',
    'Odontologo',
    'Cita',
    'Diagnostico',
    'Tratamiento',
    'Receta',
]
