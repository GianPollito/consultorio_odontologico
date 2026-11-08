from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from apps.models import Paciente, Cita, Diagnostico, Tratamiento, Receta
from apps.forms import PacienteForm

@login_required
def paciente_lista(request):
    """Listar y buscar pacientes con paginación"""
    query = request.GET.get('q', '').strip()
    pacientes = Paciente.objects.all()

    if query:
        pacientes = pacientes.filter(
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(dni__icontains=query) |
            Q(telefono__icontains=query) |
            Q(correo__icontains=query)
        )

    paginator = Paginator(pacientes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pacientes/lista.html', {
        'page_obj': page_obj,
        'query': query,
        'total_registros': pacientes.count(),
    })

@login_required
def paciente_crear(request):
    """Registrar un nuevo paciente con validaciones"""
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f"Paciente '{paciente.nombre_completo}' registrado exitosamente.")
            return redirect('paciente_detalle', pk=paciente.pk)
        else:
            messages.error(request, "Por favor corrija los errores indicados en el formulario.")
    else:
        form = PacienteForm()

    return render(request, 'pacientes/form.html', {
        'form': form,
        'titulo': 'Registrar Nuevo Paciente',
        'boton_texto': 'Guardar Paciente',
    })

@login_required
def paciente_editar(request, pk):
    """Editar información de un paciente existente"""
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, f"Datos del paciente '{paciente.nombre_completo}' actualizados.")
            return redirect('paciente_detalle', pk=paciente.pk)
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = PacienteForm(instance=paciente)

    return render(request, 'pacientes/form.html', {
        'form': form,
        'paciente': paciente,
        'titulo': f'Editar Paciente: {paciente.nombre_completo}',
        'boton_texto': 'Actualizar Paciente',
    })

@login_required
def paciente_eliminar(request, pk):
    """Eliminar un paciente con confirmación previa"""
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        nombre = paciente.nombre_completo
        paciente.delete()
        messages.success(request, f"Paciente '{nombre}' eliminado correctamente.")
        return redirect('paciente_lista')

    citas_asociadas = paciente.citas.count()
    return render(request, 'pacientes/confirmar_eliminar.html', {
        'paciente': paciente,
        'citas_asociadas': citas_asociadas,
    })

@login_required
def paciente_detalle(request, pk):
    """Historial clínico completo del paciente"""
    paciente = get_object_or_404(Paciente, pk=pk)
    citas = paciente.citas.select_related('odontologo').order_by('-fecha', '-hora')
    diagnosticos = Diagnostico.objects.filter(cita__paciente=paciente).select_related('cita__odontologo').order_by('-fecha')
    tratamientos = Tratamiento.objects.filter(diagnostico__cita__paciente=paciente).select_related('diagnostico').order_by('-fecha_inicio')
    recetas = Receta.objects.filter(diagnostico__cita__paciente=paciente).select_related('diagnostico').order_by('-id')

    return render(request, 'pacientes/detalle.html', {
        'paciente': paciente,
        'citas': citas,
        'diagnosticos': diagnosticos,
        'tratamientos': tratamientos,
        'recetas': recetas,
    })
