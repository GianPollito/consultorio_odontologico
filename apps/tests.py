from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, time, timedelta
from decimal import Decimal
from apps.models import (
    Paciente,
    Especialidad,
    Odontologo,
    Cita,
    Diagnostico,
    Tratamiento,
    Receta
)

class ConsultorioOdontologicoTests(TestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='dentista_test',
            password='testpassword123',
            first_name='Dr. Juan',
            last_name='Pérez'
        )
        self.client = Client()

        # Crear modelos base
        self.especialidad = Especialidad.objects.create(
            nombre='Ortodoncia Test',
            descripcion='Especialidad de corrección dental',
            estado='Activa'
        )
        self.odontologo = Odontologo.objects.create(
            nombres='Carlos',
            apellidos='Mendoza',
            numero_colegiatura='COP-99999',
            telefono='987654321',
            correo='carlos@clinica.pe',
            especialidad=self.especialidad,
            estado='Activo'
        )
        self.paciente = Paciente.objects.create(
            nombres='Ana',
            apellidos='Gómez',
            dni='12345678',
            fecha_nacimiento=date(1995, 6, 15),
            telefono='912345678',
            direccion='Av. Las Flores 123',
            correo='ana@gmail.com'
        )
        self.cita = Cita.objects.create(
            paciente=self.paciente,
            odontologo=self.odontologo,
            fecha=date.today(),
            hora=time(10, 0),
            motivo='Revisión general',
            estado='Pendiente',
            observaciones='Primera visita'
        )
        self.diagnostico = Diagnostico.objects.create(
            cita=self.cita,
            descripcion='Caries superficial en pieza 16',
            recomendaciones='Curación con resina',
            fecha=date.today()
        )
        self.tratamiento = Tratamiento.objects.create(
            diagnostico=self.diagnostico,
            nombre='Curación con Resina',
            descripcion='Restauración estética de pieza 16',
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=2),
            costo=Decimal('120.00'),
            estado='En proceso'
        )
        self.receta = Receta.objects.create(
            diagnostico=self.diagnostico,
            medicamento='Ibuprofeno 400mg',
            dosis='1 tableta',
            frecuencia='Cada 8 horas',
            duracion='3 días',
            indicaciones='Tomar después de las comidas'
        )

    # 1. PROTECCIÓN DE DATOS: Las rutas deben requerir inicio de sesión
    def test_rutas_protegidas_redirigen_a_login(self):
        rutas = [
            reverse('dashboard'),
            reverse('paciente_lista'),
            reverse('odontologo_lista'),
            reverse('especialidad_lista'),
            reverse('cita_lista'),
            reverse('diagnostico_lista'),
            reverse('tratamiento_lista'),
            reverse('receta_lista'),
            reverse('reportes_index'),
        ]
        for url in rutas:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 302, f"Ruta {url} no redirigió a login")
            self.assertIn('/login/', res.url)

    # 2. AUTENTICACIÓN: Login y "Mantener mi cuenta abierta"
    def test_login_con_mantener_sesion(self):
        # Con checkbox activo: sesión debe durar 2 semanas (1209600s)
        res = self.client.post(reverse('login'), {
            'username': 'dentista_test',
            'password': 'testpassword123',
            'mantener_sesion': True
        })
        self.assertRedirects(res, reverse('dashboard'))
        self.assertEqual(self.client.session.get_expiry_age(), 1209600)

    def test_login_sin_mantener_sesion(self):
        # Sin checkbox: sesión expira al cerrar navegador
        res = self.client.post(reverse('login'), {
            'username': 'dentista_test',
            'password': 'testpassword123',
            'mantener_sesion': False
        })
        self.assertRedirects(res, reverse('dashboard'))
        self.assertEqual(self.client.session.get_expire_at_browser_close(), True)

    # 3. DASHBOARD CON INDICADORES
    def test_dashboard_indicadores(self):
        self.client.login(username='dentista_test', password='testpassword123')
        res = self.client.get(reverse('dashboard'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['total_pacientes'], 1)
        self.assertEqual(res.context['total_citas'], 1)
        self.assertEqual(res.context['total_diagnosticos'], 1)
        self.assertEqual(res.context['total_tratamientos'], 1)

    # 4. CRUD 01: PACIENTES
    def test_crud_pacientes(self):
        self.client.login(username='dentista_test', password='testpassword123')
        # Crear nuevo
        res = self.client.post(reverse('paciente_crear'), {
            'nombres': 'Lucía',
            'apellidos': 'Torres',
            'dni': '87654321',
            'fecha_nacimiento': '1998-04-20',
            'telefono': '998877665',
            'direccion': 'Jr. Los Álamos 450',
            'correo': 'lucia@gmail.com'
        })
        self.assertEqual(Paciente.objects.count(), 2)

        # Buscar en lista
        res_list = self.client.get(reverse('paciente_lista') + '?q=Torres')
        self.assertContains(res_list, 'Lucía Torres')

        # Editar
        p = Paciente.objects.get(dni='87654321')
        self.client.post(reverse('paciente_editar', args=[p.pk]), {
            'nombres': 'Lucía Elena',
            'apellidos': 'Torres',
            'dni': '87654321',
            'fecha_nacimiento': '1998-04-20',
            'telefono': '998877665',
            'direccion': 'Jr. Los Álamos 450',
            'correo': 'lucia@gmail.com'
        })
        p.refresh_from_db()
        self.assertEqual(p.nombres, 'Lucía Elena')

        # Eliminar
        self.client.post(reverse('paciente_eliminar', args=[p.pk]))
        self.assertEqual(Paciente.objects.count(), 1)

    # 5. VALIDACIÓN DE FORMULARIOS: DNI 8 DÍGITOS
    def test_validacion_dni_paciente(self):
        self.client.login(username='dentista_test', password='testpassword123')
        # DNI con menos de 8 dígitos
        res = self.client.post(reverse('paciente_crear'), {
            'nombres': 'Test',
            'apellidos': 'Invalido',
            'dni': '123',
            'fecha_nacimiento': '2000-01-01',
            'telefono': '999999999',
            'direccion': 'Calle 1',
            'correo': 'test@gmail.com'
        })
        self.assertFormError(res.context['form'], 'dni', 'El DNI debe tener exactamente 8 dígitos.')

    # 6. REPORTES FILTRABLES CON VISTA DE IMPRESIÓN Y PDF
    def test_reportes_con_impresion(self):
        self.client.login(username='dentista_test', password='testpassword123')
        reportes = [
            reverse('reporte_citas'),
            reverse('reporte_diagnosticos'),
            reverse('reporte_tratamientos'),
            reverse('reporte_recetas'),
        ]
        for url in reportes:
            # Vista interactiva
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Error en {url}")
            # Vista imprimible / PDF
            res_print = self.client.get(url + '?imprimir=1')
            self.assertEqual(res_print.status_code, 200, f"Error en {url}?imprimir=1")
            self.assertContains(res_print, 'Sonrisa Perfecta')
