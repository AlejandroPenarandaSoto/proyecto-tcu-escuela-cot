// JS del módulo administrador.

/**
 * Muestra el campo de texto/URL o el campo de archivo, según el
 * tipo de contenido elegido en el formulario de "Agregar contenido".
 */
function mostrarCampoSegunTipo(tipo) {
    const campoTexto = document.getElementById("campo-texto");
    const campoArchivo = document.getElementById("campo-archivo");

    if (tipo === "imagen" || tipo === "archivo") {
        campoTexto.style.display = "none";
        campoArchivo.style.display = "block";
    } else {
        campoTexto.style.display = "block";
        campoArchivo.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const selectTipo = document.getElementById("tipo");
    if (selectTipo) {
        mostrarCampoSegunTipo(selectTipo.value);
    }
});
