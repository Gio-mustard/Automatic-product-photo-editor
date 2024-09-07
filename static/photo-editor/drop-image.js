/*
Este script solo deja listo el componente de drop image
para poder usar el evento `drop` en el script main...
*/


const dropArea = document.getElementById('drop-image');
const secondDropArea = document.getElementById('drop-background');
// Evita el comportamiento predeterminado de arrastrar y soltar
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    secondDropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Agrega y remueve las clases cuando se arrastra el archivo sobre el área
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.add('hover'), false);
    secondDropArea.addEventListener(eventName, () => secondDropArea.classList.add('hover'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.remove('hover'), false);
    secondDropArea.addEventListener(eventName, () => secondDropArea.classList.remove('hover'), false);
});
