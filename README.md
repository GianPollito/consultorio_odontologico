# SISTEMA DE GESTIÓN PARA CONSULTORIO ODONTOLÓGICO "SONRISA PERFECTA"
### Caso Propuesto N.º 01 | Gestión de Pacientes y Atención Odontológica

Sistema web profesional desarrollado con **Python**, **Django**, **MariaDB**, **HTML**, **CSS** (Diseño exclusivo, **Sin Bootstrap**, tipografía base 16px) y **JavaScript**, tomando como referencia la estructura modular del proyecto "Veterinaria Profesional" y cumpliendo rigurosamente con los requerimientos técnicos y funcionales solicitados.

---

## 🚀 Características Principales

1. **Tecnologías Requeridas**:
   - **Backend**: Python 3.11+, Django 5.x.
   - **Base de Datos**: MariaDB en el puerto **3307**.
   - **Frontend**: HTML5 semántico, CSS3 personalizado modular (Tipografía base de 16px, diseño 100% adaptable/responsivo para móviles, tablets y monitores), JavaScript puro. **Cero uso de Bootstrap**, respetando las especificaciones.
   - **Seguridad**: Protección de rutas clínicas con autenticación obligatoria (`@login_required`), protección CSRF, sanitización contra inyecciones SQL y validación robusta de formularios.

2. **Arquitectura Modular de Estilos CSS (`static/css/`)**:
   Los estilos están organizados en archivos independientes por módulo y propósito, sin concentrar todo en un solo archivo:
   - [`base.css`](file:///c:/Users/Lenovo/Downloads/sistema_gestion_consultorio_odontologico/static/css/base.css): Reset de estilos, tipografía base de **16 px** y variables globales de color.
   - [`layout.css`](file:///c:/Users/Lenovo/Downloads/sistema_gestion_consultorio_odontologico/static/css/layout.css): Menú lateral (sidebar), barra superior (topbar), contenedor principal y footer.
   - [`components.css`](file:///c:/Users/Lenovo/Downloads/sistema_gestion_consultorio_odontologico/static/css/components.css): Botones, tarjetas (cards), tablas de datos, badges de estado, alertas y paginación.
   - [`forms.css`](file:///c:/Users/Lenovo/Downloads/sistema_gestion_consultorio_odontologico/static/css/forms.css): Controles de formulario, inputs, selects, textareas, checkboxes y mensajes de validación.
   - [`auth.css`](file:///c:/Users/Lenovo/Downloads/sistema_gestion_consultorio_odontologico/static/css/auth.css): Pantallas de inicio de sesión y registro de usuarios.
   - [`dashboard.css`](file:///c:/Users/Lenovo/Downloads/sistema_gestion_consultorio_odontologico/static/css/dashboard.css): Tarjetas métricas KPI, gráficos porcentuales y distribución del panel de control.
   - [`pacientes.css`](file:///c:/Users/Lenovo/Downloads/sistema_gestion_consultorio_odontologico/static/css/pacientes.css): Cabecera de paciente e historial clínico detallado.
   - [`print.css`](file:///c:/Users/Lenovo/Downloads/sistema_gestion_consultorio_odontologico/static/css/print.css): Reglas `@media print`, membrete oficial y bloques de firma para impresión y PDF.
   - [`responsive.css`](file:///c:/Users/Lenovo/Downloads/sistema_gestion_consultorio_odontologico/static/css/responsive.css): Reglas y media queries para diseño adaptable en tablets y móviles.
   - [`main.css`](file:///c:/Users/Lenovo/Downloads/sistema_gestion_consultorio_odontologico/static/css/main.css): Hoja maestra que importa de forma ordenada los submódulos.

3. **Arquitectura de Modelos en Archivos Independientes (`apps/models/`)**:
   Cada clase de negocio se encuentra aislada en su propio archivo dentro de `apps/models/` y reexportada mediante `apps/models/__init__.py`:
   - `01 Paciente` (`apps/models/paciente.py`): DNI (8 dígitos validados), nombres, apellidos, fecha de nacimiento, teléfono, dirección, correo, fecha de registro.
   - `02 Odontologo` (`apps/models/odontologo.py`): Nombres, apellidos, número de colegiatura (COP), teléfono, correo, clave foránea a Especialidad, estado (Activo/Inactivo).
   - `03 Especialidad` (`apps/models/especialidad.py`): Nombre de especialidad, descripción, estado (Activa/Inactiva).
   - `04 Cita` (`apps/models/cita.py`): Clave foránea a Paciente, clave foránea a Odontólogo, fecha, hora, motivo, estado (Pendiente, Confirmada, Atendida, Cancelada), observaciones.
   - `05 Diagnostico` (`apps/models/diagnostico.py`): Clave foránea a Cita, descripción de hallazgos clínicos, recomendaciones del especialista, fecha.
   - `06 Tratamiento` (`apps/models/tratamiento.py`): Clave foránea a Diagnóstico, nombre del procedimiento, descripción, fecha de inicio, fecha de fin, costo (S/.), estado (Pendiente, En proceso, Finalizado).
   - `07 Receta` (`apps/models/receta.py`): Clave foránea a Diagnóstico, medicamento indicado, dosis prescrita, frecuencia de administración, duración del tratamiento, indicaciones adicionales.

3. **Requisitos Funcionales Implementados**:
   - **CRUD Completo**: Registrar, listar, buscar, editar y eliminar para las 7 tablas de negocio con mensajes dinámicos de éxito y error.
   - **Formularios Validados**: Restricciones de DNI a 8 dígitos exactos, cruces de agenda en citas, coherencia en fechas de inicio y fin de tratamientos, montos no negativos, campos requeridos y formato de correo electrónico.
   - **Autenticación con Seguridad**:
     - Pantalla de inicio de sesión con opción **"Mantener mi cuenta abierta"** (extiende la expiración de sesión a 14 días con `set_expiry(1209600)`; al desmarcarla la sesión expira inmediatamente al cerrar el navegador con `set_expiry(0)`).
     - Enlace directo a pantalla de registro de usuarios del sistema.
   - **Dashboard con Indicadores Clave (KPIs)**:
     - Total de pacientes registrados y nuevos del mes.
     - Total de citas programadas, citas para hoy y citas pendientes.
     - Total de diagnósticos clínicos emitidos.
     - Total de tratamientos con montos presupuestados y desglose por estados (En proceso, finalizados).
     - Gráfico visual interactivo del estado de citas (puro CSS/SVG).
     - Listado de agenda reciente y tratamientos activos con accesos rápidos.
   - **Historial Clínico Integral del Paciente**: Vista unificada donde se aprecian cronológicamente todas sus citas, diagnósticos, procedimientos terapéuticos y medicamentos prescritos.
   - **Módulo de Reportes Filtrables con Impresión y Guardado en PDF**:
     - Reporte de Citas (filtros: fecha desde/hasta, odontólogo, estado).
     - Reporte de Diagnósticos (filtros: fecha desde/hasta, odontólogo, búsqueda de paciente).
     - Reporte de Tratamientos (filtros: fecha desde/hasta, estado, desglose de costos y montos acumulados).
     - Reporte de Recetas (filtros: medicamento, fecha desde/hasta, búsqueda de paciente).
     - Todos los reportes cuentan con un formato institucional con membrete oficial de "Sonrisa Perfecta", RUC, datos de contacto, tabla con bordes de impresión y bloque para firmas médicas, listos para imprimir o guardar directamente como archivo PDF desde el navegador (`Ctrl + P` o botón "Imprimir / Guardar en PDF").

---

## ⚙️ Configuración y Variables de Entorno (`.env`)

El sistema utiliza variables de entorno cargadas automáticamente:

```ini
# .env
SECRET_KEY=django-insecure-sonrisaperfecta-consultorio-odontologico-2026-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
PORT=8000

# Base de datos MariaDB
DB_ENGINE=django.db.backends.mysql
DB_NAME=consultorio_odontologico_db
DB_USER=root
DB_PASSWORD=gian123
DB_HOST=127.0.0.1
DB_PORT=3307
```

---

## 👥 Credenciales de Acceso Precargadas

| Rol | Usuario | Contraseña |
|---|---|---|
| **Administrador** | `admin` | `admin123` |
| **Recepción / Asistente** | `recepcion` | `recepcion123` |

*(También es posible crear nuevos usuarios desde el enlace de registro del login)*.

---

## 🏁 Cómo Iniciar el Sistema

### Opción 1: Lanzador Automático (Recomendado)
Haga doble clic en el archivo:
- `iniciar_servidor.bat` (o ejecute `.\iniciar_servidor.ps1` en PowerShell).

El script comprueba la disponibilidad de MariaDB en el puerto 3307 y verifica que el puerto web no colisione con sus otros proyectos (usando el puerto libre 8000 o 8088 de respaldo).

### Opción 2: Ejecución Manual desde la Terminal
```powershell
# 1. Aplicar migraciones a MariaDB (si fuera necesario)
python manage.py migrate

# 2. Cargar datos de prueba iniciales (opcional)
python manage.py seed_data

# 3. Iniciar el servidor de desarrollo
python manage.py runserver 127.0.0.1:8000
```

Abra su navegador en: **http://127.0.0.1:8000/**

---

## 🧪 Ejecución de Pruebas Automatizadas

El proyecto incluye una suite completa de pruebas unitarias y de integración que verifican autenticación, validación de DNI, sesiones, protección de rutas y generación de reportes imprimibles:

```powershell
python manage.py test
```
Resultados: **7/7 pruebas OK**.
