document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navbarRight = document.querySelector('.navbar-right');
    const body = document.body;

    if (menuToggle && navbarRight) {
        menuToggle.addEventListener('click', function() {
            menuToggle.classList.toggle('active');
            navbarRight.classList.toggle('active');
            body.style.overflow = navbarRight.classList.contains('active') ? 'hidden' : '';
        });

        // Cerrar menú al hacer click en un enlace
        const navLinks = navbarRight.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navbarRight.classList.remove('active');
                body.style.overflow = '';
            });
        });

        // Cerrar menú al hacer click fuera
        document.addEventListener('click', function(e) {
            if (!menuToggle.contains(e.target) && !navbarRight.contains(e.target)) {
                menuToggle.classList.remove('active');
                navbarRight.classList.remove('active');
                body.style.overflow = '';
            }
        });
    }
});