import { mark_settings } from "./canvas.js";
import { advance_options } from "./advance-mode.js";
import { images } from "./main.js";

const btn_make_stack = document.getElementById("btn-make-stack");
const canvas = document.getElementById("canvas");
const btn_save_stack = document.getElementById("btn-save-stack");
const canvas_image = document.getElementById("canvas-image");
const micro_canvas_image = document.getElementById("micro-canvas-image");
const image_in_canvas =  {blob:null,url:null};
const interpreter_single_bg_color = (color)=>{
    const new_color = color.replace("rgba(",'').replace(')','').split(',').map(i=>parseFloat(i))
    new_color[new_color.length-1] *= 255
    return new_color;
}
const interpreter_bg_color = (colors)=>{
    const new_colors = [];
    for (let color_object of colors){
        const new_color = interpreter_single_bg_color(color_object.color);
        new_colors.push(new_color.map(i=>parseInt(i)))
    }
    return new_colors;
}
btn_make_stack.onclick = async () => {
    const new_settings = JSON.parse(JSON.stringify(mark_settings))
    const background_image = advance_options.background_image
    const new_advanced_settings = JSON.parse(JSON.stringify(advance_options))
    new_advanced_settings['background_image'] = background_image
    if (images.length <= 0) return
    new_settings.background_color = interpreter_bg_color(new_settings.background_color)
    new_advanced_settings.remove_bg_options.background_color = interpreter_single_bg_color(
        new_advanced_settings.remove_bg_options.apply_bg_color?new_advanced_settings.remove_bg_options.background_color:'rgba(0,0,0,0)'
    );
    const form = new FormData()
    
    images.forEach((image) => {
        form.append('images', image.file)
    })
    form.append('has_watermark', new_advanced_settings.has_watermark);
    form.append('watermark',new_advanced_settings.watermark);
    form.append('make_stack', true);
    form.append('stack_options', JSON.stringify(new_settings));
    form.append('remove_bg', new_advanced_settings.remove_bg);
    form.append('remove_bg_options', JSON.stringify(new_advanced_settings.remove_bg_options));
    form.append('has_background_image',new_advanced_settings.has_background_image);
    form.append('background_image',new_advanced_settings.background_image);
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
        canvas.style.backgroundImage = `url(${url})`
        canvas_image.src = url
        micro_canvas_image.src = url
        btn_save_stack.className = "";
        btn_save_stack.onclick = (e) => {
            const enlaceDescarga = document.createElement('a');
            enlaceDescarga.href = url;
            enlaceDescarga.download = 'contenedor_capturado.png'; // Nombre del archivo de descarga
            enlaceDescarga.click();
        }
    }
    else{
        // TODO: hay que cambiar como notificar los errores.
        alert(`Error ${await response.text()}`)
    }
}

micro_canvas_image.onclick = (e)=>{
    if(e.target.classList.contains("hidden")){
        e.target.classList.remove("hidden");
    }
    else{
        e.target.classList.add("hidden");
    }
}