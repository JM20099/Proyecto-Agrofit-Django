// -------------------------------------------------------------
// FUNCIÓN 1: Controla la visibilidad de las fechas según el Radio seleccionado
// -------------------------------------------------------------
function toggleCamposContrato() {
  const radioSeleccionado = document.querySelector('input[name="tipoContrato"]:checked');
  const seccionContrato = document.getElementById('seccionContrato');

  if (radioSeleccionado && seccionContrato) {
    // Se compara en minúscula para que funcione con "Contrato" o "contrato"
    if (radioSeleccionado.value.trim().toLowerCase() === 'contrato') {
      seccionContrato.style.display = 'block';
    } else {
      seccionContrato.style.display = 'none';
    }
  }
}


// -------------------------------------------------------------
// EVENTO PRINCIPAL: Se ejecuta cuando la página termina de cargar
// -------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {

  const botonesRol = document.querySelectorAll('.registro__botton, .registro__aprendiz');
  const grupoTipoContrato = document.getElementById('grupoTipoContrato');
  const seccionContrato = document.getElementById('seccionContrato');
  const seccionFicha = document.getElementById('seccionFicha');
  const seccionDependencia = document.getElementById('seccionDependencia');
  const seccionPassword = document.getElementById('seccionPassword');
  const seccionCentrodeFormacion = document.getElementById('seccionCentrodeFormacion');

  // Los radios de Planta / Contrato avisan solos al cambiar (ya no dependen del onchange del HTML)
  document.querySelectorAll('input[name="tipoContrato"]').forEach(radio => {
    radio.addEventListener('change', toggleCamposContrato);
  });

  botonesRol.forEach(boton => {
    boton.addEventListener('click', () => {

      botonesRol.forEach(btn => btn.style.backgroundColor = 'white');
      boton.style.backgroundColor = 'rgb(210, 241, 210)';

      const textoRol = boton.textContent.trim().toLowerCase();

      if (textoRol === 'aprendiz') {
        if (grupoTipoContrato) grupoTipoContrato.style.display = 'none';
        if (seccionContrato) seccionContrato.style.display = 'none';
        if (seccionDependencia) seccionDependencia.style.display = 'none';
        if (seccionFicha) seccionFicha.style.display = 'block';
        if (seccionPassword) seccionPassword.style.display = 'block';
        if (seccionCentrodeFormacion) seccionCentrodeFormacion.style.display = 'none';
      } else {
        if (grupoTipoContrato) grupoTipoContrato.style.display = 'block';
        if (seccionDependencia) seccionDependencia.style.display = 'block';
        if (seccionFicha) seccionFicha.style.display = 'none';
        if (seccionPassword) seccionPassword.style.display = 'block';
        if (seccionCentrodeFormacion) seccionCentrodeFormacion.style.display = 'block';

        toggleCamposContrato();
      }
    });
  });

  // Ejecución inicial para asegurar el estado correcto al cargar el formulario
  toggleCamposContrato();
});