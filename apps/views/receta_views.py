from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from apps.models import Receta, Diagnostico
from apps.forms import RecetaForm

@login_required
def receta_lista(request):
    """Listar, buscar y filtrar recetas médicas emitidas"""
    query = request.GET.get('q', '').strip()

    recetas = Receta.objects.select_related('diagnostico__cita__paciente', 'diagnostico__cita__odontologo').all()

    if query:
        recetas = recetas.filter(
            Q(medicamento__icontains=query) |
            Q(dosis__icontains=query) |
            Q(diagnostico__cita__paciente__nombres__icontains=query) |
            Q(diagnostico__cita__paciente__apellidos__icontains=query) |
            Q(diagnostico__cita__paciente__dni__icontains=query) |
            Q(diagnostico__cita__odontologo__nombres__icontains=query) |
            Q(diagnostico__cita__odontologo__apellidos__icontains=query)
        )

    paginator = Paginator(recetas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recetas/lista.html', {
        'page_obj': page_obj,
        'query': query,
        'total_registros': recetas.count(),
    })

@login_required
def receta_crear(request):
    """Emitir una nueva receta odontológica"""
    diagnostico_id = request.GET.get('diagnostico')
    initial_data = {}
    if diagnostico_id:
        initial_data['diagnostico'] = diagnostico_id

    if request.method == 'POST':
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save()
            messages.success(request, f"Receta para '{receta.medicamento}' registrada exitosamente.")
            return redirect('receta_lista')
        else:
            messages.error(request, "Por favor corrija los datos de la receta.")
    else:
        form = RecetaForm(initial=initial_data)

    return render(request, 'recetas/form.html', {
        'form': form,
        'titulo': 'Emitir Receta Médica Odontológica',
        'boton_texto': 'Guardar Receta',
    })

@login_required
def receta_editar(request, pk):
    """Editar receta existente"""
    receta = get_object_or_404(Receta, pk=pk)
    if request.method == 'POST':
        form = RecetaForm(request.POST, instance=receta)
        if form.is_valid():
            form.save()
            messages.success(request, f"Receta para '{receta.medicamento}' actualizada.")
            return redirect('receta_lista')
        else:
            messages.error(request, "Por favor verifique los datos del formulario.")
    else:
        form = RecetaForm(instance=receta)

    return render(request, 'recetas/form.html', {
        'form': form,
        'receta': receta,
        'titulo': f'Editar Receta: {receta.medicamento}',
        'boton_texto': 'Actualizar Receta',
    })

@login_required
def receta_eliminar(request, pk):
    """Eliminar receta"""
    receta = get_object_or_404(Receta, pk=pk)
    if request.method == 'POST':
        med = receta.medicamento
        receta.delete()
        messages.success(request, f"Receta de '{med}' eliminada.")
        return redirect('receta_lista')

    return render(request, 'recetas/confirmar_eliminar.html', {'receta': receta})
