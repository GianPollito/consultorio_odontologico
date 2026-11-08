from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta, time
from decimal import Decimal
from apps.models import (
    Especialidad,
    Odontologo,
    Paciente,
    Cita,
    Diagnostico,
    Tratamiento,
    Receta
)

class Command(BaseCommand):
    help = 'Pobla la base de datos con usuarios y datos iniciales de prueba para el consultorio odontológico.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Iniciando la carga de datos iniciales..."))

        # 1. Crear Superusuario y Usuario de Recepción
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@sonrisaperfecta.pe', 'admin123', first_name='Administrador', last_name='Principal')
            self.stdout.write(self.style.SUCCESS("Superusuario 'admin' creado (clave: admin123)."))
        else:
            self.stdout.write("Superusuario 'admin' ya existe.")

        if not User.objects.filter(username='recepcion').exists():
            u = User.objects.create_user('recepcion', 'recepcion@sonrisaperfecta.pe', 'recepcion123', first_name='María', last_name='Gómez')
            self.stdout.write(self.style.SUCCESS("Usuario 'recepcion' creado (clave: recepcion123)."))

        # 2. Especialidades
        especialidades_datos = [
            ("Ortodoncia", "Diagnóstico, prevención y corrección de anomalías de posición de los dientes y huesos maxilares mediante brackets y alineadores.", "Activa"),
            ("Endodoncia", "Tratamiento de conductos radiculares para salvar piezas dentales con pulpa inflamada, infectada o necrosada.", "Activa"),
            ("Periodoncia", "Tratamiento de enfermedades de las encías y tejidos de soporte del diente (gingivitis, periodontitis).", "Activa"),
            ("Odontopediatría", "Atención dental integral especializada para bebés, niños y adolescentes.", "Activa"),
            ("Cirugía Bucal y Maxilofacial", "Extracciones de terceras molares, cirugías periapicales, frenectomías e implantes óseos.", "Activa"),
            ("Rehabilitación Oral", "Restauración de la función masticatoria y estética mediante prótesis fijas, removibles e implantes.", "Activa"),
            ("Odontología Estética", "Blanqueamiento dental, carillas de porcelana o resina, diseño de sonrisa y profilaxis avanzada.", "Activa"),
        ]

        especialidades_map = {}
        for nombre, desc, estado in especialidades_datos:
            esp, created = Especialidad.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': desc, 'estado': estado}
            )
            especialidades_map[nombre] = esp
        self.stdout.write(self.style.SUCCESS(f"{len(especialidades_map)} especialidades listas."))

        # 3. Odontólogos
        odontologos_datos = [
            ("Carlos Alberto", "Mendoza Ruiz", "COP-28491", "987112233", "carlos.mendoza@sonrisaperfecta.pe", "Ortodoncia", "Activo"),
            ("Valeria Sofía", "Paredes Castro", "COP-31204", "976223344", "valeria.paredes@sonrisaperfecta.pe", "Endodoncia", "Activo"),
            ("Javier Ignacio", "Salazar Vega", "COP-19842", "995334455", "javier.salazar@sonrisaperfecta.pe", "Cirugía Bucal y Maxilofacial", "Activo"),
            ("Elena Beatriz", "Torres Linares", "COP-42119", "964445566", "elena.torres@sonrisaperfecta.pe", "Odontopediatría", "Activo"),
            ("Gustavo Adolfo", "Flores Quiroz", "COP-35780", "953556677", "gustavo.flores@sonrisaperfecta.pe", "Rehabilitación Oral", "Activo"),
        ]

        odontologos_map = {}
        for nom, ape, col, tel, mail, esp_nom, est in odontologos_datos:
            odon, created = Odontologo.objects.get_or_create(
                numero_colegiatura=col,
                defaults={
                    'nombres': nom,
                    'apellidos': ape,
                    'telefono': tel,
                    'correo': mail,
                    'especialidad': especialidades_map[esp_nom],
                    'estado': est
                }
            )
            odontologos_map[col] = odon
        self.stdout.write(self.style.SUCCESS(f"{len(odontologos_map)} odontólogos listos."))

        # 4. Pacientes
        pacientes_datos = [
            ("Juan Diego", "Morales Chávez", "72458912", date(1994, 5, 14), "981234567", "Av. Javier Prado Este 2450, San Borja", "juan.morales@gmail.com"),
            ("Rosa Marina", "Alvarado Benítez", "45871239", date(1988, 11, 23), "972345678", "Jr. Huiracocha 1420, Jesús María", "rosa.alvarado@hotmail.com"),
            ("Mateo Sebastián", "Gutiérrez Peña", "78912345", date(2005, 3, 10), "963456789", "Calle Las Begonias 320, San Isidro", "mateo.gutierrez@yahoo.com"),
            ("Camila Lucía", "Ríos Navarrete", "71234567", date(1999, 8, 30), "954567890", "Av. Arequipa 3890, Miraflores", "camila.rios@gmail.com"),
            ("Jorge Luis", "Cárdenas Espinoza", "10293847", date(1975, 1, 18), "945678901", "Calle Los Sauces 145, Surco", "jorge.cardenas@outlook.com"),
            ("Ana Lucía", "Vargas Silva", "74859612", date(2001, 7, 5), "936789012", "Av. Salaverry 1120, Magdalena", "ana.vargas@gmail.com"),
            ("Ricardo José", "Quispe Mamani", "42157896", date(1983, 12, 12), "927890123", "Av. Colonial 560, Cercado de Lima", "ricardo.quispe@gmail.com"),
            ("Mariana Belén", "Herrera Domínguez", "73645129", date(1997, 4, 25), "918901234", "Jr. Junín 450, Pueblo Libre", "mariana.herrera@hotmail.com"),
        ]

        pacientes_map = {}
        for nom, ape, dni, fnac, tel, dirn, mail in pacientes_datos:
            pac, created = Paciente.objects.get_or_create(
                dni=dni,
                defaults={
                    'nombres': nom,
                    'apellidos': ape,
                    'fecha_nacimiento': fnac,
                    'telefono': tel,
                    'direccion': dirn,
                    'correo': mail
                }
            )
            pacientes_map[dni] = pac
        self.stdout.write(self.style.SUCCESS(f"{len(pacientes_map)} pacientes listos."))

        # 5. Citas
        hoy = date.today()
        citas_datos = [
            ("72458912", "COP-28491", hoy - timedelta(days=5), time(9, 30), "Control y ajuste mensual de brackets metálicos", "Atendida", "Paciente asistió puntual."),
            ("45871239", "COP-31204", hoy - timedelta(days=3), time(11, 0), "Dolor agudo pulsátil en segundo premolar superior izquierdo", "Atendida", "Requiere tratamiento de conductos de urgencia."),
            ("78912345", "COP-19842", hoy - timedelta(days=2), time(15, 30), "Evaluación para extracción de terceros molares inferiores", "Atendida", "Radiografía panorámica traída por el paciente."),
            ("71234567", "COP-42119", hoy, time(10, 0), "Profilaxis dental preventiva y aplicación de flúor barniz", "Confirmada", "Paciente confirmada vía WhatsApp."),
            ("10293847", "COP-35780", hoy, time(16, 0), "Toma de impresión definitiva para corona de zirconia", "Pendiente", "Laboratorio confirmó entrega de pilares."),
            ("74859612", "COP-28491", hoy + timedelta(days=2), time(14, 0), "Consulta inicial para ortodoncia estética con alineadores", "Confirmada", "Primera vez en el consultorio."),
            ("42157896", "COP-31204", hoy + timedelta(days=4), time(17, 30), "Segunda sesión de endodoncia pieza 46", "Pendiente", "Medicamento intraconducto colocado."),
            ("73645129", "COP-19842", hoy - timedelta(days=10), time(12, 0), "Limpieza profunda periodontal", "Atendida", "Evolución favorable."),
        ]

        citas_creadas = []
        for dni, col, f, h, mot, est, obs in citas_datos:
            pac = pacientes_map[dni]
            odon = odontologos_map[col]
            cita, created = Cita.objects.get_or_create(
                paciente=pac,
                odontologo=odon,
                fecha=f,
                hora=h,
                defaults={'motivo': mot, 'estado': est, 'observaciones': obs}
            )
            citas_creadas.append(cita)
        self.stdout.write(self.style.SUCCESS(f"{len(citas_creadas)} citas listas."))

        # 6. Diagnósticos
        diag1, _ = Diagnostico.objects.get_or_create(
            cita=citas_creadas[0],
            defaults={
                'descripcion': "Maloclusión Clase II división 1 con apiñamiento moderado anteroinferior y mordida profunda del 60%.",
                'recomendaciones': "Uso continuo de elásticos intermaxilares 3/16 mediana fuerza. Higiene estricta con cepillo interproximal y enjuague fluorado.",
                'fecha': hoy - timedelta(days=5)
            }
        )

        diag2, _ = Diagnostico.objects.get_or_create(
            cita=citas_creadas[1],
            defaults={
                'descripcion': "Pulpitis irreversible sintomática con necrosis parcial en pieza dental 24 secundaria a caries interproximal profunda.",
                'recomendaciones': "Evitar masticar alimentos duros por el lado izquierdo. Toma de analgésico y antibiótico según prescripción médica.",
                'fecha': hoy - timedelta(days=3)
            }
        )

        diag3, _ = Diagnostico.objects.get_or_create(
            cita=citas_creadas[2],
            defaults={
                'descripcion': "Impactación mesioangular de piezas 38 y 48 (terceros molares inferiores) en contacto estrecho con conducto dentario.",
                'recomendaciones': "Planificación quirúrgica bajo anestesia local troncular. Reposo absoluto de 72 horas y dieta blanda fría.",
                'fecha': hoy - timedelta(days=2)
            }
        )

        diag4, _ = Diagnostico.objects.get_or_create(
            cita=citas_creadas[7],
            defaults={
                'descripcion': "Gingivitis marginal generalizada inducida por placa bacteriana y sarro subgingival localizado en sector anteroinferior.",
                'recomendaciones': "Técnica de cepillado de Bass modificada dos veces al día. Colutorio con clorhexidina al 0.12% durante 14 días.",
                'fecha': hoy - timedelta(days=10)
            }
        )
        self.stdout.write(self.style.SUCCESS("4 diagnósticos clínicos registrados."))

        # 7. Tratamientos
        Tratamiento.objects.get_or_create(
            diagnostico=diag1,
            nombre="Tratamiento de Ortodoncia con Brackets Metálicos MBT",
            defaults={
                'descripcion': "Alineación, nivelación, cierre de espacios y detallado oclusal con aparatología fija bimaxilar.",
                'fecha_inicio': hoy - timedelta(days=90),
                'fecha_fin': hoy + timedelta(days=450),
                'costo': Decimal('3200.00'),
                'estado': 'En proceso'
            }
        )

        Tratamiento.objects.get_or_create(
            diagnostico=diag2,
            nombre="Endodoncia Birradicular Mecanizada en Pieza 24",
            defaults={
                'descripcion': "Instrumentación rotatoria con sistema WaveOne Gold, irrigación con hipoclorito al 5.25% y obturación termoplastificada.",
                'fecha_inicio': hoy - timedelta(days=3),
                'fecha_fin': hoy + timedelta(days=5),
                'costo': Decimal('450.00'),
                'estado': 'En proceso'
            }
        )

        Tratamiento.objects.get_or_create(
            diagnostico=diag3,
            nombre="Odontectomía Quirúrgica de Terceras Molares (Piezas 38 y 48)",
            defaults={
                'descripcion': "Cirugía menor con colgajo triangular, ostectomía vestibular, odontosección y sutura con seda 3-0.",
                'fecha_inicio': hoy + timedelta(days=7),
                'fecha_fin': hoy + timedelta(days=14),
                'costo': Decimal('700.00'),
                'estado': 'Pendiente'
            }
        )

        Tratamiento.objects.get_or_create(
            diagnostico=diag4,
            nombre="Destartraje Ultrasónico y Profilaxis Bimaxilar",
            defaults={
                'descripcion': "Eliminación de cálculo supragingival con ultrasonido Cavitron y pulido con pasta abrasiva y escobilla Robinson.",
                'fecha_inicio': hoy - timedelta(days=10),
                'fecha_fin': hoy - timedelta(days=10),
                'costo': Decimal('160.00'),
                'estado': 'Finalizado'
            }
        )
        self.stdout.write(self.style.SUCCESS("4 tratamientos registrados."))

        # 8. Recetas
        Receta.objects.get_or_create(
            diagnostico=diag2,
            medicamento="Amoxicilina + Ácido Clavulánico 875/125 mg",
            defaults={
                'dosis': "1 tableta recubierta",
                'frecuencia': "Cada 12 horas",
                'duracion': "7 días",
                'indicaciones': "Ingerir inmediatamente antes de las comidas principales con un vaso lleno de agua."
            }
        )

        Receta.objects.get_or_create(
            diagnostico=diag2,
            medicamento="Ketorolaco Trometamol 10 mg",
            defaults={
                'dosis': "1 tableta sublingual",
                'frecuencia': "Cada 8 horas (condicional al dolor)",
                'duracion': "3 días máximo",
                'indicaciones': "Disolver debajo de la lengua. No exceder 40 mg diarios ni consumir con el estómago vacío."
            }
        )

        Receta.objects.get_or_create(
            diagnostico=diag3,
            medicamento="Ibuprofeno 600 mg",
            defaults={
                'dosis': "1 tableta",
                'frecuencia': "Cada 8 horas",
                'duracion': "4 días",
                'indicaciones': "Iniciar 1 hora antes del procedimiento quirúrgico y continuar después de las comidas."
            }
        )

        Receta.objects.get_or_create(
            diagnostico=diag4,
            medicamento="Enjuague Bucal Clorhexidina al 0.12%",
            defaults={
                'dosis': "15 ml sin diluir",
                'frecuencia': "Cada 12 horas (después del cepillado)",
                'duracion': "14 días",
                'indicaciones': "Enjuagar durante 60 segundos y escupir. No ingerir alimentos ni bebidas durante 30 minutos."
            }
        )
        self.stdout.write(self.style.SUCCESS("4 recetas médicas registradas."))

        self.stdout.write(self.style.SUCCESS("¡Carga de datos completada exitosamente!"))
