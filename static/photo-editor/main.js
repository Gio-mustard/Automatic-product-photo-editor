/*
Este script se encarga de controlar la entrada y salidas de la imágenes al stack, todo se resume en que los objetos `PreviewImage` que estén en el array `images` son las imágenes que están listas para ser enviadas a editar al servidor.
*/
// inicializaron del script
globalThis.imagesInStack = 0

function PreviewImage(file) {
    this.src = URL.createObjectURL(file);
    this.file = file;
    this.id = `image-${globalThis.imagesInStack++}`
    this.get_html = () => {
        return (`<div class="image-in-view" id='${this.id}'>
            <button class='delete btn-delete-from-view' onclick='remove_image("${this.id}")'>
            <img src="static/img/ic_trash.png">
            </button>
            <img src="${this.src}">
            </div>`)
    }
}
const images_view = document.getElementById('images-view') // contenedor de la vista en vivo de las images.
const input_images = document.getElementById('images-input');// punto de entrada para las imágenes
const drop_area = document.getElementById('drop-image');
const modal_upload_image = document.getElementById('modal-upload-image');
let images = [];// se actualiza a la par del DOM


const __update_images_view = async () => {
    images_view.innerHTML = "";
    images.forEach((image) => {
        images_view.innerHTML += image.get_html();
    })
}
const __handle_push_files = (files) => {
    files.forEach((file, index) => {
        push_image(file, index == files.length - 1);
    });
}
input_images.onchange = (e) => {
    const files = Array.from(e.target.files);
    __handle_push_files(files)

}
drop_area.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    const files = Array.from(dt.files);
    __handle_push_files(files)

}, false);


const push_image = async (file, update_dom = false) => {
    /*
    Esta es la función principal que actualiza el array de las imágenes actuales y a la par actualiza el DOM para mostrar su previsualización
    */
   const new_image = new PreviewImage(file);
   // ! actualización del array de imágenes
   images.push(new_image)
   // ! notificar en modal
   temp_images_to_show_modal.push(new_image)
   if (update_dom) {
        show_modal_preview()
    }
    // ! actualización del DOM
    if (!update_dom) return
    __update_images_view()
}
let temp_images_to_show_modal = [];
const show_modal_preview = () => {
    document.getElementById('modal-preview').src = temp_images_to_show_modal[0].src
    document.getElementById('modal-filename').innerText = temp_images_to_show_modal[0].file.name
    document.getElementById('count-upload-images').innerText = `${temp_images_to_show_modal.length}`;
    modal_upload_image.className = ""
    setTimeout(() => {
        modal_upload_image.className = "hidden"
    }, 2000)
    temp_images_to_show_modal = [];
}
const remove_image = (id) => {
    images = images.filter(image => image.id != id)
    __update_images_view()
}
const _show_images = async () => {
    console.log(images)
}
const btn_upload_image = document.getElementById("btn-upload-image");
btn_upload_image.onclick = () => input_images.click()