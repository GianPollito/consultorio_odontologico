from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from apps.models import (
    Paciente,
    Odontologo,
    Especialidad,
    Cita,
    Diagnostico,
    Tratamiento,
    Receta
)

# ==========================================
# FORMULARIOS DE AUTENTICACIÓN
# ==========================================

class CustomLoginForm(forms.Form):
    """Formulario de inicio de sesión con opción 'Mantener mi cuenta abierta'"""
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ingrese su usuario',
            'autocomplete': 'username',
            'required': 'required'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ingrese su contraseña',
            'autocomplete': 'current-password',
            'required': 'required'
        })
    )
    mantener_sesion = forms.BooleanField(
        label="Mantener mi cuenta abierta",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )


class RegistroUsuarioForm(forms.ModelForm):
    """Formulario para registro de nuevos usuarios del sistema"""
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Mínimo 6 caracteres'}),
        min_length=6
    )
    password_confirm = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Repita la contraseña'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'correo@ejemplo.com'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("Este nombre de usuario ya está registrado.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')
        if p1 and p2 and p1 != p2:
            self.add_error('password_confirm', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# ==========================================
# 01 FORMULARIO PACIENTE
# ==========================================

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombres', 'apellidos', 'dni', 'fecha_nacimiento', 'telefono', 'direccion', 'correo']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombres del paciente'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Apellidos del paciente'}),
            'dni': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '8 dígitos numéricos', 'maxlength': '8'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'telefono': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. 987654321'}),
            'direccion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Av. / Jr. / Calle y número'}),
            'correo': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'paciente@ejemplo.com'}),
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni', '').strip()
        if not dni.isdigit():
            raise ValidationError("El DNI debe contener únicamente dígitos numéricos.")
        if len(dni) != 8:
            raise ValidationError("El DNI debe tener exactamente 8 dígitos.")
        
        # Validar unicidad (excluyendo la instancia actual si está editando)
        qs = Paciente.objects.filter(dni=dni)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Ya existe un paciente registrado con este número de DNI.")
        return dni

    def clean_fecha_nacimiento(self):
        f_nac = self.cleaned_data.get('fecha_nacimiento')
        if f_nac and f_nac > date.today():
            raise ValidationError("La fecha de nacimiento no puede ser posterior a la fecha actual.")
        return f_nac


# ==========================================
# 02 FORMULARIO ODONTÓLOGO
# ==========================================

class OdontologoForm(forms.ModelForm):
    class Meta:
        model = Odontologo
        fields = ['nombres', 'apellidos', 'numero_colegiatura', 'telefono', 'correo', 'especialidad', 'estado']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombres del odontólogo'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Apellidos del odontólogo'}),
            'numero_colegiatura': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. COP-45678'}),
            'telefono': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. 987654321'}),
            'correo': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'doctor@sonrisaperfecta.pe'}),
            'especialidad': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_numero_colegiatura(self):
        col = self.cleaned_data.get('numero_colegiatura', '').strip()
        if not col:
            raise ValidationError("El número de colegiatura es obligatorio.")
        qs = Odontologo.objects.filter(numero_colegiatura__iexact=col)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Ya existe un odontólogo con este número de colegiatura.")
        return col


# ==========================================
# 03 FORMULARIO ESPECIALIDAD
# ==========================================

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Ortodoncia, Periodoncia'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Descripción detallada de la especialidad'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise ValidationError("El nombre de la especialidad es obligatorio.")
        qs = Especialidad.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Ya existe una especialidad con este nombre.")
        return nombre


# ==========================================
# 04 FORMULARIO CITA
# ==========================================

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'odontologo', 'fecha', 'hora', 'motivo', 'estado', 'observaciones']
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'odontologo': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'motivo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Limpieza dental, dolor en molar, revisión'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Observaciones previas o antecedentes (opcional)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        paciente = cleaned_data.get('paciente')
        odontologo = cleaned_data.get('odontologo')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')
        
        if odontologo and fecha and hora:
            # Validar cruce de horario con el mismo odontólogo (mismo día y hora exacta)
            qs = Cita.objects.filter(odontologo=odontologo, fecha=fecha, hora=hora).exclude(estado='Cancelada')
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError(f"El Dr(a). {odontologo.nombre_completo} ya tiene otra cita programada el {fecha} a las {hora}.")
        return cleaned_data


# ==========================================
# 05 FORMULARIO DIAGNÓSTICO
# ==========================================

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['cita', 'descripcion', 'recomendaciones', 'fecha']
        widgets = {
            'cita': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Hallazgos clínicos, piezas afectadas, patologías observadas...'}),
            'recomendaciones': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Indicaciones de cuidado bucal, prevención o hábitos'}),
            'fecha': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }


# ==========================================
# 06 FORMULARIO TRATAMIENTO
# ==========================================

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['diagnostico', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'costo', 'estado']
        widgets = {
            'diagnostico': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Endodoncia pieza 36, Resina compuesta'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Procedimiento terapéutico a ejecutar'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'costo': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        f_inicio = cleaned_data.get('fecha_inicio')
        f_fin = cleaned_data.get('fecha_fin')
        costo = cleaned_data.get('costo')

        if f_inicio and f_fin and f_fin < f_inicio:
            self.add_error('fecha_fin', "La fecha de finalización no puede ser anterior a la fecha de inicio.")
        
        if costo is not None and costo < 0:
            self.add_error('costo', "El costo del tratamiento debe ser un monto positivo o cero.")
        return cleaned_data


# ==========================================
# 07 FORMULARIO RECETA
# ==========================================

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['diagnostico', 'medicamento', 'dosis', 'frecuencia', 'duracion', 'indicaciones']
        widgets = {
            'diagnostico': forms.Select(attrs={'class': 'form-select'}),
            'medicamento': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Amoxicilina 500mg, Ketorolaco 10mg'}),
            'dosis': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. 1 tableta, 500 mg, 1 ampolla'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. Cada 8 horas, Cada 12 horas'}),
            'duracion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej. 7 días, 5 días'}),
            'indicaciones': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Tomar con las comidas o abundante agua, evitar alcohol...'}),
        }
