from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date
from apps.models import Tratamiento, Diagnostico
from apps.forms import TratamientoForm

@login_required
def tratamiento_lista(request):
    """Listar, buscar y filtrar tratamientos odontológicos"""
    query = request.GET.get('q', '').strip()
    estado_filtro = request.GET.get('estado', '').strip()

    tratamientos = Tratamiento.objects.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo').all()

    if query:
        tratamientos = tratamientos.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(diagnostico__cita__paciente__nombres__icontains=query) |
            Q(diagnostico__cita__paciente__apellidos__icontains=query) |
            Q(diagnostico__cita__paciente__dni__icontains=query)
        )
    if estado_filtro:
        tratamientos = tratamientos.filter(estado=estado_filtro)

    paginator = Paginator(tratamientos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tratamientos/lista.html', {
        'page_obj': page_obj,
        'query': query,
        'estado_filtro': estado_filtro,
        'total_registros': tratamientos.count(),
    })

@login_required
def tratamiento_crear(request):
    """Registrar un nuevo tratamiento"""
    diagnostico_id = request.GET.get('diagnostico')
    initial_data = {
        'fecha_inicio': date.today(),
        'fecha_fin': date.today(),
    }
    if diagnostico_id:
        initial_data['diagnostico'] = diagnostico_id

    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            trat = form.save()
            messages.success(request, f"Tratamiento '{trat.nombre}' asignado correctamente.")
            return redirect('tratamiento_lista')
        else:
            messages.error(request, "Por favor revise las observaciones del formulario.")
    else:
        form = TratamientoForm(initial=initial_data)

    return render(request, 'tratamientos/form.html', {
        'form': form,
        'titulo': 'Registrar Plan de Tratamiento',
        'boton_texto': 'Guardar Tratamiento',
    })

@login_required
def tratamiento_editar(request, pk):
    """Editar tratamiento existente"""
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        form = TratamientoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            form.save()
            messages.success(request, f"Tratamiento '{tratamiento.nombre}' actualizado.")
            return redirect('tratamiento_lista')
        else:
            messages.error(request, "Por favor verifique los errores en el formulario.")
    else:
        form = TratamientoForm(instance=tratamiento)

    return render(request, 'tratamientos/form.html', {
        'form': form,
        'tratamiento': tratamiento,
        'titulo': f'Editar Tratamiento: {tratamiento.nombre}',
        'boton_texto': 'Actualizar Tratamiento',
    })

@login_required
def tratamiento_eliminar(request, pk):
    """Eliminar tratamiento"""
    tratamiento = get_object_or_404(Tratamiento, pk=pk)
    if request.method == 'POST':
        nombre = tratamiento.nombre
        tratamiento.delete()
        messages.success(request, f"Tratamiento '{nombre}' eliminado.")
        return redirect('tratamiento_lista')

    return render(request, 'tratamientos/confirmar_eliminar.html', {'tratamiento': tratamiento})
