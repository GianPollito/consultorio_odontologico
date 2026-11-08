from .auth_views import login_view, register_view, logout_view
from .dashboard_views import dashboard_view
from .paciente_views import (
    paciente_lista, paciente_crear, paciente_editar, paciente_eliminar, paciente_detalle
)
from .odontologo_views import (
    odontologo_lista, odontologo_crear, odontologo_editar, odontologo_eliminar
)
from .especialidad_views import (
    especialidad_lista, especialidad_crear, especialidad_editar, especialidad_eliminar
)
from .cita_views import (
    cita_lista, cita_crear, cita_editar, cita_eliminar, cita_cambiar_estado
)
from .diagnostico_views import (
    diagnostico_lista, diagnostico_crear, diagnostico_editar, diagnostico_eliminar, diagnostico_detalle
)
from .tratamiento_views import (
    tratamiento_lista, tratamiento_crear, tratamiento_editar, tratamiento_eliminar
)
from .receta_views import (
    receta_lista, receta_crear, receta_editar, receta_eliminar
)
from .reporte_views import (
    reportes_index, reporte_citas, reporte_diagnosticos, reporte_tratamientos, reporte_recetas
)
