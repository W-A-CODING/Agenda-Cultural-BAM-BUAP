function mostrarEventos(dia) {
        document.querySelectorAll('.tooltip-eventos').forEach(t => t.style.display = 'none');
        const tooltip = document.getElementById('eventos-' + dia);
        if (tooltip) tooltip.style.display = 'block';
    }

    document.addEventListener('click', function(e) {
        if (!e.target.closest('.celda-dia')) {
            document.querySelectorAll('.tooltip-eventos').forEach(t => t.style.display = 'none');
        }
    });
