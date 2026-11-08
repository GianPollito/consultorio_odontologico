from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from datetime import date
from apps.models import Paciente, Odontologo, Especialidad, Cita, Diagnostico, Tratamiento, Receta

@login_required
def dashboard_view(request):
    """
    Panel de Control principal con indicadores clave de rendimiento (KPIs)
    de pacientes, citas, tratamientos y diagnósticos.
    """
    hoy = date.today()

    # Indicadores de Pacientes
    total_pacientes = Paciente.objects.count()
    pacientes_este_mes = Paciente.objects.filter(
        created_at__year=hoy.year,
        created_at__month=hoy.month
    ).count()

    # Indicadores de Citas
    total_citas = Cita.objects.count()
    citas_hoy = Cita.objects.filter(fecha=hoy).count()
    citas_pendientes = Cita.objects.filter(estado='Pendiente').count()
    citas_confirmadas = Cita.objects.filter(estado='Confirmada').count()
    citas_atendidas = Cita.objects.filter(estado='Atendida').count()
    citas_canceladas = Cita.objects.filter(estado='Cancelada').count()

    # Indicadores de Diagnósticos
    total_diagnosticos = Diagnostico.objects.count()
    diagnosticos_mes = Diagnostico.objects.filter(
        fecha__year=hoy.year,
        fecha__month=hoy.month
    ).count()

    # Indicadores de Tratamientos
    total_tratamientos = Tratamiento.objects.count()
    tratamientos_en_proceso = Tratamiento.objects.filter(estado='En proceso').count()
    tratamientos_finalizados = Tratamiento.objects.filter(estado='Finalizado').count()
    tratamientos_pendientes = Tratamiento.objects.filter(estado='Pendiente').count()
    monto_total_tratamientos = Tratamiento.objects.aggregate(total=Sum('costo'))['total'] or 0

    # Indicadores adicionales
    total_recetas = Receta.objects.count()
    total_odontologos = Odontologo.objects.filter(estado='Activo').count()

    # Listados de actividad reciente
    citas_recientes = Cita.objects.select_related('paciente', 'odontologo').order_by('-fecha', '-hora')[:6]
    tratamientos_activos = Tratamiento.objects.select_related('diagnostico__cita__paciente').filter(
        estado='En proceso'
    ).order_by('-fecha_inicio')[:5]

    # Datos para gráfico de estado de citas
    estados_citas_data = [
        {'label': 'Pendientes', 'valor': citas_pendientes, 'color': '#F59E0B'},
        {'label': 'Confirmadas', 'valor': citas_confirmadas, 'color': '#3B82F6'},
        {'label': 'Atendidas', 'valor': citas_atendidas, 'color': '#10B981'},
        {'label': 'Canceladas', 'valor': citas_canceladas, 'color': '#EF4444'},
    ]

    context = {
        'total_pacientes': total_pacientes,
        'pacientes_este_mes': pacientes_este_mes,
        'total_citas': total_citas,
        'citas_hoy': citas_hoy,
        'citas_pendientes': citas_pendientes,
        'citas_confirmadas': citas_confirmadas,
        'citas_atendidas': citas_atendidas,
        'citas_canceladas': citas_canceladas,
        'total_diagnosticos': total_diagnosticos,
        'diagnosticos_mes': diagnosticos_mes,
        'total_tratamientos': total_tratamientos,
        'tratamientos_en_proceso': tratamientos_en_proceso,
        'tratamientos_finalizados': tratamientos_finalizados,
        'tratamientos_pendientes': tratamientos_pendientes,
        'monto_total_tratamientos': monto_total_tratamientos,
        'total_recetas': total_recetas,
        'total_odontologos': total_odontologos,
        'citas_recientes': citas_recientes,
        'tratamientos_activos': tratamientos_activos,
        'estados_citas_data': estados_citas_data,
        'hoy': hoy,
    }
    return render(request, 'dashboard/dashboard.html', context)
