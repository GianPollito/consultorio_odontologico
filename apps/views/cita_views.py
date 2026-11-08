from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from apps.models import Cita, Odontologo
from apps.forms import CitaForm

@login_required
def cita_lista(request):
    """Listar, buscar y filtrar citas odontológicas"""
    query = request.GET.get('q', '').strip()
    fecha_filtro = request.GET.get('fecha', '').strip()
    estado_filtro = request.GET.get('estado', '').strip()
    odontologo_id = request.GET.get('odontologo', '').strip()

    citas = Cita.objects.select_related('paciente', 'odontologo').all()

    if query:
        citas = citas.filter(
            Q(paciente__nombres__icontains=query) |
            Q(paciente__apellidos__icontains=query) |
            Q(paciente__dni__icontains=query) |
            Q(motivo__icontains=query) |
            Q(odontologo__nombres__icontains=query) |
            Q(odontologo__apellidos__icontains=query)
        )
    if fecha_filtro:
        citas = citas.filter(fecha=fecha_filtro)
    if estado_filtro:
        citas = citas.filter(estado=estado_filtro)
    if odontologo_id:
        citas = citas.filter(odontologo_id=odontologo_id)

    paginator = Paginator(citas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    odontologos = Odontologo.objects.filter(estado='Activo')

    return render(request, 'citas/lista.html', {
        'page_obj': page_obj,
        'query': query,
        'fecha_filtro': fecha_filtro,
        'estado_filtro': estado_filtro,
        'odontologo_id': odontologo_id,
        'odontologos': odontologos,
        'total_registros': citas.count(),
    })

@login_required
def cita_crear(request):
    """Programar una nueva cita odontológica"""
    paciente_id = request.GET.get('paciente')
    initial_data = {}
    if paciente_id:
        initial_data['paciente'] = paciente_id

    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()
            messages.success(request, f"Cita #{cita.id} para {cita.paciente.nombre_completo} programada con éxito.")
            return redirect('cita_lista')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = CitaForm(initial=initial_data)

    return render(request, 'citas/form.html', {
        'form': form,
        'titulo': 'Programar Cita Odontológica',
        'boton_texto': 'Guardar Cita',
    })

@login_required
def cita_editar(request, pk):
    """Editar cita existente"""
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cita #{cita.id} actualizada correctamente.")
            return redirect('cita_lista')
        else:
            messages.error(request, "Por favor revise las observaciones del formulario.")
    else:
        form = CitaForm(instance=cita)

    return render(request, 'citas/form.html', {
        'form': form,
        'cita': cita,
        'titulo': f'Editar Cita #{cita.id}',
        'boton_texto': 'Actualizar Cita',
    })

@login_required
def cita_eliminar(request, pk):
    """Eliminar cita odontológica"""
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        cita_num = cita.id
        cita.delete()
        messages.success(request, f"Cita #{cita_num} eliminada.")
        return redirect('cita_lista')

    return render(request, 'citas/confirmar_eliminar.html', {'cita': cita})

@login_required
def cita_cambiar_estado(request, pk, nuevo_estado):
    """Cambio rápido de estado de la cita desde el listado"""
    cita = get_object_or_404(Cita, pk=pk)
    estados_validos = [e[0] for e in Cita.ESTADO_CHOICES]
    if nuevo_estado in estados_validos:
        cita.estado = nuevo_estado
        cita.save()
        messages.success(request, f"Cita #{cita.id} actualizada a '{nuevo_estado}'.")
    return redirect(request.META.get('HTTP_REFERER', 'cita_lista'))
