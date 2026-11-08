from datetime import date
from apps.models import Cita

def global_clinic_info(request):
    """
    Context processor para proveer datos globales a las plantillas:
    Nombre de la clínica, fecha actual, citas pendientes hoy.
    """
    hoy = date.today()
    citas_hoy_pendientes = 0
    if request.user.is_authenticated:
        try:
            citas_hoy_pendientes = Cita.objects.filter(fecha=hoy, estado='Pendiente').count()
        except Exception:
            citas_hoy_pendientes = 0

    return {
        'CLINIC_NAME': 'Sonrisa Perfecta',
        'CLINIC_SLOGAN': 'Gestión de Pacientes y Atención Odontológica',
        'CLINIC_RUC': '20601234567',
        'CLINIC_PHONE': '(01) 456-7890 / +51 987 654 321',
        'CLINIC_EMAIL': 'contacto@sonrisaperfecta.pe',
        'CLINIC_ADDRESS': 'Av. Principal 1234, San Isidro, Lima - Perú',
        'CURRENT_YEAR': hoy.year,
        'TODAY_DATE': hoy,
        'citas_hoy_pendientes_count': citas_hoy_pendientes,
    }
