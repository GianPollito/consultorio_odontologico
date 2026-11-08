from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date
from apps.models import Diagnostico, Cita
from apps.forms import DiagnosticoForm

@login_required
def diagnostico_lista(request):
    """Listar y buscar diagnósticos clínicos"""
    query = request.GET.get('q', '').strip()
    fecha_filtro = request.GET.get('fecha', '').strip()
    diagnosticos = Diagnostico.objects.select_related('cita__paciente', 'cita__odontologo').all()

    if query:
        diagnosticos = diagnosticos.filter(
            Q(cita__paciente__nombres__icontains=query) |
            Q(cita__paciente__apellidos__icontains=query) |
            Q(cita__paciente__dni__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(cita__odontologo__nombres__icontains=query) |
            Q(cita__odontologo__apellidos__icontains=query)
        )
    if fecha_filtro:
        diagnosticos = diagnosticos.filter(fecha=fecha_filtro)

    paginator = Paginator(diagnosticos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'diagnosticos/lista.html', {
        'page_obj': page_obj,
        'query': query,
        'fecha_filtro': fecha_filtro,
        'total_registros': diagnosticos.count(),
    })

@login_required
def diagnostico_crear(request):
    """Registrar un nuevo diagnóstico para una cita"""
    cita_id = request.GET.get('cita')
    initial_data = {'fecha': date.today()}
    if cita_id:
        initial_data['cita'] = cita_id

    if request.method == 'POST':
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
            diag = form.save()
            # Al emitir diagnóstico, podemos marcar la cita como 'Atendida'
            cita = diag.cita
            if cita.estado != 'Atendida':
                cita.estado = 'Atendida'
                cita.save()
            messages.success(request, f"Diagnóstico #{diag.id} registrado y cita #{cita.id} marcada como Atendida.")
            return redirect('diagnostico_detalle', pk=diag.pk)
        else:
            messages.error(request, "Por favor corrija los datos del diagnóstico.")
    else:
        form = DiagnosticoForm(initial=initial_data)

    return render(request, 'diagnosticos/form.html', {
        'form': form,
        'titulo': 'Registrar Diagnóstico Odontológico',
        'boton_texto': 'Guardar Diagnóstico',
    })

@login_required
def diagnostico_editar(request, pk):
    """Editar diagnóstico clínico"""
    diagnostico = get_object_or_404(Diagnostico, pk=pk)
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST, instance=diagnostico)
        if form.is_valid():
            form.save()
            messages.success(request, f"Diagnóstico #{diagnostico.id} actualizado.")
            return redirect('diagnostico_detalle', pk=diagnostico.pk)
        else:
            messages.error(request, "Por favor revise las observaciones del formulario.")
    else:
        form = DiagnosticoForm(instance=diagnostico)

    return render(request, 'diagnosticos/form.html', {
        'form': form,
        'diagnostico': diagnostico,
        'titulo': f'Editar Diagnóstico #{diagnostico.id}',
        'boton_texto': 'Actualizar Diagnóstico',
    })

@login_required
def diagnostico_eliminar(request, pk):
    """Eliminar diagnóstico clínico"""
    diagnostico = get_object_or_404(Diagnostico, pk=pk)
    if request.method == 'POST':
        diag_num = diagnostico.id
        diagnostico.delete()
        messages.success(request, f"Diagnóstico #{diag_num} eliminado.")
        return redirect('diagnostico_lista')

    tratamientos_count = diagnostico.tratamientos.count()
    recetas_count = diagnostico.recetas.count()

    return render(request, 'diagnosticos/confirmar_eliminar.html', {
        'diagnostico': diagnostico,
        'tratamientos_count': tratamientos_count,
        'recetas_count': recetas_count,
    })

@login_required
def diagnostico_detalle(request, pk):
    """Detalle del diagnóstico con sus tratamientos y recetas prescritas"""
    diagnostico = get_object_or_404(Diagnostico.objects.select_related('cita__paciente', 'cita__odontologo'), pk=pk)
    tratamientos = diagnostico.tratamientos.all()
    recetas = diagnostico.recetas.all()

    return render(request, 'diagnosticos/detalle.html', {
        'diagnostico': diagnostico,
        'tratamientos': tratamientos,
        'recetas': recetas,
    })
