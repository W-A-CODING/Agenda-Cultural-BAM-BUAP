
const contenedorToast = document.getElementById('contenedor-toast');

//evento para cerrar los botones
contenedorToast.addEventListener('click', (e) => {
	const toastId = e.target.closest('div.toast').id;

	if (e.target.closest('button.btn-cerrar')) {
		cerrarToast(toastId);
	}
});

//Funcion para cerrar el toast
const cerrarToast = (id) => {
	document.getElementById(id)?.classList.add('cerrando');
};
//Funcion para mostrar las notificacioness
const agregarToast = (tipo, titulo, descripcion, autoCierre) => {

    //Crear nuevo toast
    const nuevoToast = document.createElement('div');

    //agregar clases correspondientes 
    nuevoToast.classList.add('toast');
    nuevoToast.classList.add(tipo);
    if(autoCierre) nuevoToast.classList.add('autoCierre');

    //agregar id
    const numeroAlAzar = Math.floor(Math.random() * 100);
    const fecha = Date.now();
    const toastId = fecha + numeroAlAzar;
    nuevoToast.id = toastId;

    //Iconos
    const iconos ={
        exito:`<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
                                <path 
                                    d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zm10.03 4.97a.75.75 0 0 1 .011 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.75.75 0 0 1 1.08-.022z"
                                />
                              </svg>`,
        error:`<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
                                <path 
                                    d="M11.46.146A.5.5 0 0 0 11.107 0H4.893a.5.5 0 0 0-.353.146L.146 4.54A.5.5 0 0 0 0 4.893v6.214a.5.5 0 0 0 .146.353l4.394 4.394a.5.5 0 0 0 .353.146h6.214a.5.5 0 0 0 .353-.146l4.394-4.394a.5.5 0 0 0 .146-.353V4.893a.5.5 0 0 0-.146-.353zM8 4c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995A.905.905 0 0 1 8 4m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2"
                                />
                              </svg>`,
        info: `<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
                                <path 
                                    d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2"
                                />
                              </svg>`,
        warning:`<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
                                <path 
                                    d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2"
                                />
                              </svg>`,
    };

    //plantilla notificacion
    const toast =`
    <div class="contenido">
        <div class= "icono">
        ${iconos[tipo]}
        </div>
                        <div class="texto">
                            <p class="titulo">${titulo}</p>
                            <p class="descripcion">${descripcion}</p>
                        </div>
                    </div>
                    <button class="btn-cerrar">
                        <div class="icono">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
                                <path 
                                    d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"
                                />
                              </svg>
                        </div>
                    </button>
    `


    //agregar la plantilla al nuevo toast
    nuevoToast.innerHTML = toast;

    //agregar el nuevo toast al contenedor
    contenedorToast.appendChild(nuevoToast);

    //Funcion para manejar el cierre de toast
    const handleAnimacionCierre = (e) => {
       if(e.animationName === 'cierre'){
        nuevoToast.removeEventListener('animationend', handleAnimacionCierre);
        nuevoToast.remove();
       }
    };

    if (autoCierre) {
		setTimeout(() => cerrarToast(toastId), 10000);
	}

    //agregar event lisener final animacion
    nuevoToast.addEventListener('animationend', handleAnimacionCierre)
};
