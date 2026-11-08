from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from apps.forms import CustomLoginForm, RegistroUsuarioForm

def login_view(request):
    """
    Vista de inicio de sesión con opción 'Mantener mi cuenta abierta' y enlace a registro.
    Implementa patrón Post/Redirect/Get para evitar el cuadro de reenvío de formulario al actualizar.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            mantener_sesion = form.cleaned_data.get('mantener_sesion', False)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if mantener_sesion:
                        # 2 semanas de duración de sesión (1209600 segundos)
                        request.session.set_expiry(1209600)
                    else:
                        # Expira al cerrar el navegador
                        request.session.set_expiry(0)
                    messages.success(request, f"¡Bienvenido(a), {user.first_name or user.username}!")
                    next_url = request.GET.get('next', 'dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, "Esta cuenta ha sido desactivada.")
                    return redirect('login')
            else:
                messages.error(request, "Credenciales incorrectas. Verifique su usuario y contraseña.")
                request.session['failed_login_username'] = username
                return redirect('login')
        else:
            messages.error(request, "Credenciales incorrectas. Verifique su usuario y contraseña.")
            username_attempt = request.POST.get('username', '')
            if username_attempt:
                request.session['failed_login_username'] = username_attempt
            return redirect('login')
    else:
        initial_username = request.session.pop('failed_login_username', '')
        if initial_username:
            form = CustomLoginForm(initial={'username': initial_username})
        else:
            form = CustomLoginForm()

    return render(request, 'auth/login.html', {'form': form})


def register_view(request):
    """
    Vista de registro para nuevos usuarios del sistema.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Usuario '{user.username}' registrado correctamente. Inicie sesión ahora.")
            return redirect('login')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario de registro.")
    else:
        form = RegistroUsuarioForm()

    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    """
    Cierre de sesión seguro con redirección al login.
    """
    logout(request)
    messages.info(request, "Ha cerrado sesión de forma segura.")
    return redirect('login')
