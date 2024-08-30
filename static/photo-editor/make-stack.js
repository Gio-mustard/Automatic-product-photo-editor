import { mark_settings } from "./canvas.js";
import { images } from "./main.js";

const btn_make_stack = document.getElementById("btn-make-stack");
const btn_save_stack = document.getElementById("btn-save-stack");
const canvas_image = document.getElementById("canvas-image");
const image_in_canvas =  {blob:null,url:null};
const interpreter_bg_color = (colors)=>{
    const new_colors = [];
    for (let color_object of colors){
        const new_color = color_object.color.replace("rgba(",'').replace(')','').split(',').map(i=>parseFloat(i))
        new_color[new_color.length-1] *= 255
        new_colors.push(new_color.map(i=>parseInt(i)))
    }
    return new_colors;
}
btn_make_stack.onclick = async () => {
    const new_settings = {...mark_settings}
    if (images.length <= 0) return 
    console.log(new_settings)
    new_settings.background_color = interpreter_bg_color(new_settings.background_color)
    const form = new FormData()
    
    images.forEach((image) => {
        form.append('images', image.file)
    })
    form.append('has_watermark', false)
    form.append('make_stack', true);
    form.append('stack_options', JSON.stringify(new_settings))
    form.append('remove_bg', false);
 
    const response = await fetch('http://localhost:8000/api/v1/make/stack/', {
        // TODO : We need modularize this endpoint.
        method: 'POST',
        body: form,
    })
    if (response.status==201){
        const blob = await response.blob();
        const url = URL.createObjectURL(blob)
        image_in_canvas.blob = blob;
        image_in_canvas.url = url;
        canvas_image.src = url
        btn_save_stack.onclick = () => {
            const enlaceDescarga = document.createElement('a');
            enlaceDescarga.href = url;
            enlaceDescarga.download = 'contenedor_capturado.png'; // Nombre del archivo de descarga
            enlaceDescarga.click();
        }
    }
    else{
        alert(`Error ${await response.text()}`)
    }
}
