// JS base: comportamientos comunes a estudiante y admin.

document.addEventListener("DOMContentLoaded", () => {
    // Los mensajes flash se ocultan solos después de unos segundos
    const mensajes = document.querySelectorAll(".mensaje");
    mensajes.forEach((mensaje) => {
        setTimeout(() => {
            mensaje.style.transition = "opacity 0.4s ease";
            mensaje.style.opacity = "0";
            setTimeout(() => mensaje.remove(), 400);
        }, 4000);
    });
});
