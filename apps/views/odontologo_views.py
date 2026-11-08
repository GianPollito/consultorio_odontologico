from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from apps.models import Odontologo
from apps.forms import OdontologoForm

@login_required
def odontologo_lista(request):
    """Listar y buscar odontólogos"""
    query = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    odontologos = Odontologo.objects.select_related('especialidad').all()

    if query:
        odontologos = odontologos.filter(
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(numero_colegiatura__icontains=query) |
            Q(especialidad__nombre__icontains=query)
        )
    if estado:
        odontologos = odontologos.filter(estado=estado)

    paginator = Paginator(odontologos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'odontologos/lista.html', {
        'page_obj': page_obj,
        'query': query,
        'estado_filtro': estado,
        'total_registros': odontologos.count(),
    })

@login_required
def odontologo_crear(request):
    """Registrar un nuevo odontólogo"""
    if request.method == 'POST':
        form = OdontologoForm(request.POST)
        if form.is_valid():
            odon = form.save()
            messages.success(request, f"Odontólogo(a) '{odon.nombre_completo}' registrado exitosamente.")
            return redirect('odontologo_lista')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = OdontologoForm()

    return render(request, 'odontologos/form.html', {
        'form': form,
        'titulo': 'Registrar Odontólogo(a)',
        'boton_texto': 'Guardar Odontólogo',
    })

@login_required
def odontologo_editar(request, pk):
    """Editar información de un odontólogo"""
    odontologo = get_object_or_404(Odontologo, pk=pk)
    if request.method == 'POST':
        form = OdontologoForm(request.POST, instance=odontologo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Información de '{odontologo.nombre_completo}' actualizada.")
            return redirect('odontologo_lista')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = OdontologoForm(instance=odontologo)

    return render(request, 'odontologos/form.html', {
        'form': form,
        'odontologo': odontologo,
        'titulo': f'Editar Odontólogo: {odontologo.nombre_completo}',
        'boton_texto': 'Actualizar Odontólogo',
    })

@login_required
def odontologo_eliminar(request, pk):
    """Eliminar odontólogo con confirmación"""
    odontologo = get_object_or_404(Odontologo, pk=pk)
    citas_count = odontologo.citas.count()
    if request.method == 'POST':
        if citas_count > 0:
            messages.error(request, f"No se puede eliminar a {odontologo.nombre_completo} porque tiene {citas_count} citas registradas. Puede cambiar su estado a Inactivo.")
            return redirect('odontologo_lista')
        nombre = odontologo.nombre_completo
        odontologo.delete()
        messages.success(request, f"Odontólogo '{nombre}' eliminado correctamente.")
        return redirect('odontologo_lista')

    return render(request, 'odontologos/confirmar_eliminar.html', {
        'odontologo': odontologo,
        'citas_count': citas_count,
    })
