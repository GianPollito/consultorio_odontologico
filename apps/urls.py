from django.urls import path
from apps import views

urlpatterns = [
    # Autenticación
    path('', views.dashboard_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # Panel de Control
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # 01 Pacientes (CRUD)
    path('pacientes/', views.paciente_lista, name='paciente_lista'),
    path('pacientes/nuevo/', views.paciente_crear, name='paciente_crear'),
    path('pacientes/<int:pk>/', views.paciente_detalle, name='paciente_detalle'),
    path('pacientes/<int:pk>/editar/', views.paciente_editar, name='paciente_editar'),
    path('pacientes/<int:pk>/eliminar/', views.paciente_eliminar, name='paciente_eliminar'),

    # 02 Odontólogos (CRUD)
    path('odontologos/', views.odontologo_lista, name='odontologo_lista'),
    path('odontologos/nuevo/', views.odontologo_crear, name='odontologo_crear'),
    path('odontologos/<int:pk>/editar/', views.odontologo_editar, name='odontologo_editar'),
    path('odontologos/<int:pk>/eliminar/', views.odontologo_eliminar, name='odontologo_eliminar'),

    # 03 Especialidades (CRUD)
    path('especialidades/', views.especialidad_lista, name='especialidad_lista'),
    path('especialidades/nueva/', views.especialidad_crear, name='especialidad_crear'),
    path('especialidades/<int:pk>/editar/', views.especialidad_editar, name='especialidad_editar'),
    path('especialidades/<int:pk>/eliminar/', views.especialidad_eliminar, name='especialidad_eliminar'),

    # 04 Citas (CRUD)
    path('citas/', views.cita_lista, name='cita_lista'),
    path('citas/nueva/', views.cita_crear, name='cita_crear'),
    path('citas/<int:pk>/editar/', views.cita_editar, name='cita_editar'),
    path('citas/<int:pk>/eliminar/', views.cita_eliminar, name='cita_eliminar'),
    path('citas/<int:pk>/estado/<str:nuevo_estado>/', views.cita_cambiar_estado, name='cita_cambiar_estado'),

    # 05 Diagnósticos (CRUD)
    path('diagnosticos/', views.diagnostico_lista, name='diagnostico_lista'),
    path('diagnosticos/nuevo/', views.diagnostico_crear, name='diagnostico_crear'),
    path('diagnosticos/<int:pk>/', views.diagnostico_detalle, name='diagnostico_detalle'),
    path('diagnosticos/<int:pk>/editar/', views.diagnostico_editar, name='diagnostico_editar'),
    path('diagnosticos/<int:pk>/eliminar/', views.diagnostico_eliminar, name='diagnostico_eliminar'),

    # 06 Tratamientos (CRUD)
    path('tratamientos/', views.tratamiento_lista, name='tratamiento_lista'),
    path('tratamientos/nuevo/', views.tratamiento_crear, name='tratamiento_crear'),
    path('tratamientos/<int:pk>/editar/', views.tratamiento_editar, name='tratamiento_editar'),
    path('tratamientos/<int:pk>/eliminar/', views.tratamiento_eliminar, name='tratamiento_eliminar'),

    # 07 Recetas (CRUD)
    path('recetas/', views.receta_lista, name='receta_lista'),
    path('recetas/nueva/', views.receta_crear, name='receta_crear'),
    path('recetas/<int:pk>/editar/', views.receta_editar, name='receta_editar'),
    path('recetas/<int:pk>/eliminar/', views.receta_eliminar, name='receta_eliminar'),

    # Reportes
    path('reportes/', views.reportes_index, name='reportes_index'),
    path('reportes/citas/', views.reporte_citas, name='reporte_citas'),
    path('reportes/diagnosticos/', views.reporte_diagnosticos, name='reporte_diagnosticos'),
    path('reportes/tratamientos/', views.reporte_tratamientos, name='reporte_tratamientos'),
    path('reportes/recetas/', views.reporte_recetas, name='reporte_recetas'),
]
