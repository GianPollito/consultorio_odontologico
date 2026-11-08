from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from datetime import date, datetime
from apps.models import Cita, Diagnostico, Tratamiento, Receta, Odontologo

@login_required
def reportes_index(request):
    """Página principal del centro de reportes"""
    return render(request, 'reportes/index.html', {
        'total_citas': Cita.objects.count(),
        'total_diagnosticos': Diagnostico.objects.count(),
        'total_tratamientos': Tratamiento.objects.count(),
        'total_recetas': Receta.objects.count(),
    })

@login_required
def reporte_citas(request):
    """
    Reporte filtrable de citas odontológicas con opción de impresión y guardado en PDF.
    Filtros: Rango de fechas (desde, hasta), Odontólogo, Estado de cita.
    """
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    odontologo_id = request.GET.get('odontologo', '')
    estado = request.GET.get('estado', '')
    imprimir = request.GET.get('imprimir', '') == '1'

    citas = Cita.objects.select_related('paciente', 'odontologo').all()

    if fecha_desde:
        citas = citas.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        citas = citas.filter(fecha__lte=fecha_hasta)
    if odontologo_id:
        citas = citas.filter(odontologo_id=odontologo_id)
    if estado:
        citas = citas.filter(estado=estado)

    odontologos = Odontologo.objects.filter(estado='Activo')

    context = {
        'citas': citas,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'odontologo_id': odontologo_id,
        'estado_filtro': estado,
        'odontologos': odontologos,
        'total_registros': citas.count(),
        'imprimir': imprimir,
        'generado_el': datetime.now(),
    }

    if imprimir:
        return render(request, 'reportes/citas_imprimir.html', context)
    return render(request, 'reportes/citas.html', context)


@login_required
def reporte_diagnosticos(request):
    """
    Reporte filtrable de diagnósticos clínicos con opción de impresión y PDF.
    Filtros: Rango de fechas (desde, hasta), Odontólogo, búsqueda de paciente.
    """
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    odontologo_id = request.GET.get('odontologo', '')
    query_paciente = request.GET.get('paciente', '').strip()
    imprimir = request.GET.get('imprimir', '') == '1'

    diagnosticos = Diagnostico.objects.select_related('cita__paciente', 'cita__odontologo').all()

    if fecha_desde:
        diagnosticos = diagnosticos.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        diagnosticos = diagnosticos.filter(fecha__lte=fecha_hasta)
    if odontologo_id:
        diagnosticos = diagnosticos.filter(cita__odontologo_id=odontologo_id)
    if query_paciente:
        diagnosticos = diagnosticos.filter(
            Q(cita__paciente__nombres__icontains=query_paciente) |
            Q(cita__paciente__apellidos__icontains=query_paciente) |
            Q(cita__paciente__dni__icontains=query_paciente)
        )

    odontologos = Odontologo.objects.filter(estado='Activo')

    context = {
        'diagnosticos': diagnosticos,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'odontologo_id': odontologo_id,
        'query_paciente': query_paciente,
        'odontologos': odontologos,
        'total_registros': diagnosticos.count(),
        'imprimir': imprimir,
        'generado_el': datetime.now(),
    }

    if imprimir:
        return render(request, 'reportes/diagnosticos_imprimir.html', context)
    return render(request, 'reportes/diagnosticos.html', context)


@login_required
def reporte_tratamientos(request):
    """
    Reporte filtrable de tratamientos odontológicos con montos, fechas y estados.
    Filtros: Rango de fechas inicio, estado, costo mínimo.
    """
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    estado = request.GET.get('estado', '')
    imprimir = request.GET.get('imprimir', '') == '1'

    tratamientos = Tratamiento.objects.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo').all()

    if fecha_desde:
        tratamientos = tratamientos.filter(fecha_inicio__gte=fecha_desde)
    if fecha_hasta:
        tratamientos = tratamientos.filter(fecha_inicio__lte=fecha_hasta)
    if estado:
        tratamientos = tratamientos.filter(estado=estado)

    total_monto = tratamientos.aggregate(total=Sum('costo'))['total'] or 0

    context = {
        'tratamientos': tratamientos,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'estado_filtro': estado,
        'total_registros': tratamientos.count(),
        'total_monto': total_monto,
        'imprimir': imprimir,
        'generado_el': datetime.now(),
    }

    if imprimir:
        return render(request, 'reportes/tratamientos_imprimir.html', context)
    return render(request, 'reportes/tratamientos.html', context)


@login_required
def reporte_recetas(request):
    """
    Reporte filtrable de prescripciones médicas y recetas entregadas.
    Filtros: Medicamento, rango de fechas, búsqueda de paciente.
    """
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    medicamento = request.GET.get('medicamento', '').strip()
    query_paciente = request.GET.get('paciente', '').strip()
    imprimir = request.GET.get('imprimir', '') == '1'

    recetas = Receta.objects.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo').all()

    if fecha_desde:
        recetas = recetas.filter(diagnostico__fecha__gte=fecha_desde)
    if fecha_hasta:
        recetas = recetas.filter(diagnostico__fecha__lte=fecha_hasta)
    if medicamento:
        recetas = recetas.filter(medicamento__icontains=medicamento)
    if query_paciente:
        recetas = recetas.filter(
            Q(diagnostico__cita__paciente__nombres__icontains=query_paciente) |
            Q(diagnostico__cita__paciente__apellidos__icontains=query_paciente) |
            Q(diagnostico__cita__paciente__dni__icontains=query_paciente)
        )

    context = {
        'recetas': recetas,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'medicamento_filtro': medicamento,
        'query_paciente': query_paciente,
        'total_registros': recetas.count(),
        'imprimir': imprimir,
        'generado_el': datetime.now(),
    }

    if imprimir:
        return render(request, 'reportes/recetas_imprimir.html', context)
    return render(request, 'reportes/recetas.html', context)
