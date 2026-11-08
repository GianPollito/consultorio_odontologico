from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from apps.models import Especialidad
from apps.forms import EspecialidadForm

@login_required
def especialidad_lista(request):
    """Listar y buscar especialidades odontológicas"""
    query = request.GET.get('q', '').strip()
    especialidades = Especialidad.objects.all()

    if query:
        especialidades = especialidades.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )

    paginator = Paginator(especialidades, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'especialidades/lista.html', {
        'page_obj': page_obj,
        'query': query,
        'total_registros': especialidades.count(),
    })

@login_required
def especialidad_crear(request):
    """Crear nueva especialidad"""
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            esp = form.save()
            messages.success(request, f"Especialidad '{esp.nombre}' registrada con éxito.")
            return redirect('especialidad_lista')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = EspecialidadForm()

    return render(request, 'especialidades/form.html', {
        'form': form,
        'titulo': 'Registrar Especialidad',
        'boton_texto': 'Guardar Especialidad',
    })

@login_required
def especialidad_editar(request, pk):
    """Editar especialidad existente"""
    especialidad = get_object_or_404(Especialidad, pk=pk)
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            messages.success(request, f"Especialidad '{especialidad.nombre}' actualizada.")
            return redirect('especialidad_lista')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = EspecialidadForm(instance=especialidad)

    return render(request, 'especialidades/form.html', {
        'form': form,
        'especialidad': especialidad,
        'titulo': f'Editar Especialidad: {especialidad.nombre}',
        'boton_texto': 'Actualizar Especialidad',
    })

@login_required
def especialidad_eliminar(request, pk):
    """Eliminar especialidad"""
    especialidad = get_object_or_404(Especialidad, pk=pk)
    odontologos_count = especialidad.odontologos.count()

    if request.method == 'POST':
        if odontologos_count > 0:
            messages.error(request, f"No se puede eliminar la especialidad '{especialidad.nombre}' porque tiene {odontologos_count} odontólogo(s) asignados.")
            return redirect('especialidad_lista')
        nombre = especialidad.nombre
        especialidad.delete()
        messages.success(request, f"Especialidad '{nombre}' eliminada con éxito.")
        return redirect('especialidad_lista')

    return render(request, 'especialidades/confirmar_eliminar.html', {
        'especialidad': especialidad,
        'odontologos_count': odontologos_count,
    })
