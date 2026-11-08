/**
 * Sonrisa Perfecta - Sistema de Gestión de Consultorio Odontológico
 * Scripts personalizados en JavaScript puro (Vanilla JS)
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Toggle del Menú Lateral en Dispositivos Móviles
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function (e) {
            e.stopPropagation();
            sidebar.classList.toggle('open');
        });

        // Cerrar menú al hacer clic fuera del sidebar en pantallas pequeñas
        document.addEventListener('click', function (e) {
            if (window.innerWidth <= 992 && sidebar.classList.contains('open')) {
                if (!sidebar.contains(e.target) && e.target !== menuToggle) {
                    sidebar.classList.remove('open');
                }
            }
        });
    }

    // 2. Auto-cierre de alertas informativas después de 6 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300);
            });
        }

        setTimeout(function () {
            if (alert && alert.parentElement) {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }
        }, 6000);
    });

    // 3. Restricción numérica para campos DNI (8 dígitos)
    const dniInputs = document.querySelectorAll('input[name="dni"]');
    dniInputs.forEach(function (input) {
        input.addEventListener('input', function () {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 8);
        });
    });

    // 4. Botones de Impresión / Guardar en PDF
    const printButtons = document.querySelectorAll('.btn-print-report');
    printButtons.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            window.print();
        });
    });

    // 5. Confirmación para acciones críticas de eliminación
    const deleteButtons = document.querySelectorAll('.btn-confirm-delete');
    deleteButtons.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm('¿Está completamente seguro(a) de eliminar este registro? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });
});
