document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('carousel');
    if (!carousel) return; // Verificar si existe el carousel

    const slides = Array.from(carousel.children).filter(child => !child.classList.contains('carousel-nav'));
    if (slides.length === 0) return; // Verificar si hay slides

    let currentSlide = 0;
    
    // Create navigation dots
    const nav = document.createElement('div');
    nav.className = 'carousel-nav';
    
    for (let i = 0; i < slides.length; i++) {
        const dot = document.createElement('div');
        dot.className = 'carousel-dot';
        dot.addEventListener('click', () => goToSlide(i));
        nav.appendChild(dot);
    }
    
    carousel.appendChild(nav);
    
    // Process each slide
    slides.forEach(slide => {
        // Store the existing content
        const img = slide.querySelector('img');
        const content = slide.innerHTML;
        
        // Clear the slide
        slide.innerHTML = '';
        
        // Re-add the image if it exists
        if (img) {
            slide.appendChild(img);
        }
        
        // Create and add the event info
        const eventInfo = document.createElement('div');
        eventInfo.className = 'event-info';
        
        // Remove the img HTML from the content before setting event info
        const contentWithoutImg = content.replace(img ? img.outerHTML : '', '');
        eventInfo.innerHTML = contentWithoutImg.trim();
        
        if (eventInfo.innerHTML) { // Solo agregar si hay contenido
            slide.appendChild(eventInfo);
        }
    });
    
    function showSlide(n) {
        if (!slides.length) return; // Verificación adicional
        
        // Asegurarse de que n está dentro de los límites
        n = ((n % slides.length) + slides.length) % slides.length;
        
        slides.forEach(slide => slide.classList.remove('active'));
        Array.from(nav.children).forEach(dot => dot.classList.remove('active'));
        
        if (slides[n] && nav.children[n]) {
            slides[n].classList.add('active');
            nav.children[n].classList.add('active');
        }
    }
    
    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }
    
    function goToSlide(n) {
        currentSlide = n;
        showSlide(currentSlide);
    }
    
    // Show first slide
    showSlide(0);
    
    // Solo configurar el intervalo si hay más de un slide
    if (slides.length > 1) {
        setInterval(nextSlide, 5000);
    }
});