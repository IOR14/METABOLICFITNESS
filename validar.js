// validar.js — Validación de certificados 100% en el navegador (sin servidor).
// Lee el parámetro ?serial= de la URL, lo busca en window.CERTIFICADOS
// (definido en certificados-data.js) y muestra el resultado.

(function () {
    const contenedor = document.getElementById('resultado');
    if (!contenedor) return;

    const CERTS = window.CERTIFICADOS || {};

    // Evita inyección de HTML al mostrar texto del usuario o de los datos.
    function esc(texto) {
        return String(texto == null ? '' : texto)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    function obtenerSerial() {
        const params = new URLSearchParams(window.location.search);
        return (params.get('serial') || '').trim();
    }

    function vistaValido(serial, cert) {
        return (
            '<div class="bg-white rounded-2xl shadow-xl border border-green-200 overflow-hidden">' +
              '<div class="bg-gradient-to-r from-metabolic-green to-[#4ba572] px-8 py-6 flex items-center gap-4">' +
                '<div class="flex items-center justify-center w-14 h-14 rounded-full bg-white/20 shrink-0">' +
                  '<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>' +
                '</div>' +
                '<div><h2 class="font-heading font-bold text-2xl text-white">Certificado Válido</h2>' +
                '<p class="font-body text-white/90 text-sm">Este certificado fue emitido oficialmente por Metabolic Fitness.</p></div>' +
              '</div>' +
              '<div class="p-8 space-y-5">' +
                '<div class="grid sm:grid-cols-2 gap-5">' +
                  '<div><p class="font-body text-xs uppercase tracking-wider text-metabolic-charcoal/50 mb-1">Estudiante</p>' +
                  '<p class="font-heading font-bold text-lg text-metabolic-charcoal">' + esc(cert.nombre_estudiante) + '</p></div>' +
                  '<div><p class="font-body text-xs uppercase tracking-wider text-metabolic-charcoal/50 mb-1">Fecha de emisión</p>' +
                  '<p class="font-body font-semibold text-metabolic-charcoal">' + esc(cert.fecha) + '</p></div>' +
                '</div>' +
                '<div><p class="font-body text-xs uppercase tracking-wider text-metabolic-charcoal/50 mb-1">Curso / Programa</p>' +
                '<p class="font-body font-semibold text-metabolic-charcoal">' + esc(cert.curso) + '</p></div>' +
                '<div class="pt-4 border-t border-gray-100"><p class="font-body text-xs uppercase tracking-wider text-metabolic-charcoal/50 mb-1">Código de verificación</p>' +
                '<p class="font-mono text-sm text-metabolic-purple font-semibold">' + esc(serial) + '</p></div>' +
              '</div>' +
            '</div>' +
            '<div class="text-center mt-6"><a href="validar.html" class="font-body text-sm text-metabolic-purple hover:underline">Validar otro certificado</a></div>'
        );
    }

    function vistaInvalido(serial) {
        return (
            '<div class="bg-white rounded-2xl shadow-xl border border-red-200 overflow-hidden">' +
              '<div class="bg-gradient-to-r from-red-500 to-red-600 px-8 py-6 flex items-center gap-4">' +
                '<div class="flex items-center justify-center w-14 h-14 rounded-full bg-white/20 shrink-0">' +
                  '<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"></path></svg>' +
                '</div>' +
                '<div><h2 class="font-heading font-bold text-2xl text-white">Certificado no encontrado</h2>' +
                '<p class="font-body text-white/90 text-sm">No pudimos validar este código. Revísalo e inténtalo nuevamente.</p></div>' +
              '</div>' +
              '<div class="p-8">' +
                '<p class="font-body text-metabolic-charcoal/70 mb-2">El código ingresado no corresponde a ningún certificado válido:</p>' +
                '<p class="font-mono text-sm text-red-600 font-semibold mb-6 break-all">' + esc(serial) + '</p>' +
                formularioBuscador('Verificar de nuevo') +
              '</div>' +
            '</div>'
        );
    }

    function vistaBuscador() {
        return (
            '<div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-8 sm:p-10">' +
              '<p class="font-body text-metabolic-charcoal/70 mb-6 text-center">Ingresa el código de verificación que aparece en tu certificado para comprobar su autenticidad.</p>' +
              formularioBuscador('Validar', true) +
              '<p class="font-body text-xs text-metabolic-charcoal/50 mt-4 text-center">El código está al pie de tu certificado, junto al sello.</p>' +
            '</div>'
        );
    }

    function formularioBuscador(textoBoton, autofocus) {
        return (
            '<form action="validar.html" method="get" class="flex flex-col sm:flex-row gap-3">' +
              '<input type="text" name="serial" placeholder="Ej: MF-FRM-02" ' +
                'class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-metabolic-green focus:border-transparent font-body" required ' +
                (autofocus ? 'autofocus' : '') + '>' +
              '<button type="submit" class="bg-metabolic-green text-white px-6 py-3 rounded-lg font-body font-semibold hover:bg-[#4CA84C] transition-colors whitespace-nowrap">' +
                esc(textoBoton) + '</button>' +
            '</form>'
        );
    }

    function render() {
        const serial = obtenerSerial();
        if (!serial) {
            contenedor.innerHTML = vistaBuscador();
            return;
        }
        const cert = CERTS[serial];
        contenedor.innerHTML = cert ? vistaValido(serial, cert) : vistaInvalido(serial);
    }

    render();
})();
