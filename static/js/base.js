document.addEventListener('DOMContentLoaded', function() {
    const loader = document.querySelector('.loader-wrapper');
    let loadTimeout;

    function showLoader() {
        loader.classList.add('show');
        // Timeout de seguridad: ocultar después de 5 segundos
        loadTimeout = setTimeout(() => {
            hideLoader();
        }, 5000);
    }

    function hideLoader() {
        clearTimeout(loadTimeout);
        loader.classList.remove('show');
    }

    // Mostrar loader cuando se hace clic en cualquier enlace
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function(e) {
            if (!this.hasAttribute('download') && 
                this.href && 
                !this.href.includes('#') && 
                !this.href.includes('javascript:')) {
                showLoader();
            }
        });
    });

    // Mostrar loader cuando se envía un formulario
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            showLoader();
        });
    });

    // Ocultar loader en varios eventos
    window.addEventListener('load', hideLoader);
    window.addEventListener('pageshow', hideLoader);
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            hideLoader();
        }
    });

    //acitvar menu si la pantalla es pequeña
    document.addEventListener('DOMContentLoaded', () => {
        const toggle = document.querySelector('.menu-toggle');
        const navbarRight = document.querySelector('.navbar-right');

        toggle.addEventListener('click', () => {
            navbarRight.classList.toggle('active');
        });
    });

});