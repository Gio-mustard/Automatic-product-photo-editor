/*
! CANVAS
Es el recuadro donde estará la imagen edita final, al canvas le vas a apilar las configuraciones del panel de la izquierda de la pantalla, osea puedes cambiar su...
* background color
* padding
* size [width, height]
El canvas tiene una abstracción que es el objeto `mark_settings` ese sera el objeto que se usara para hacer la petición de la edición de la imagen, este objeto actualiza sus propiedades automáticamente y el algoritmo para que esto sea asi esta en este archivo.
*/

const mark_settings = {
    padding:0,
    resolution:null,
    background_color:"rgba(0,0,0,0)",
    gap:0,
    padding:0,
    direction:'row',
    alignment:['vertical'],
    scaling:'contain'
}
/*  
!
Esta variable se usa para sub escalar el resolution del canvas y su padding (para que no se sobre salgan de la pantalla)
su funcionamiento es simple, solo es el divisor para el width, height y padding.
*/
let sub_scale_constant = 4;
const canvas = document.getElementById('canvas');
// canvas resolution
const canvas_sizes = [...document.getElementsByClassName('canvas-size')]; // los radio buttons con los sizes predeterminados.
const update_size =(raw_size)=>{
    // formato del size -> resolution:widthxheight -> resolution:1920x1080
    // resolution es una propiedad de cada etiqueta radio button que se use para seleccionar un resolution para el canvas(la única excepción es el custom resolution pero se transforma para usar esta función).
    const [width,height] = raw_size.split(":")[1].split('x')
    mark_settings.resolution = `${width}x${height}`
    canvas.style.width = `${width/sub_scale_constant}px`
    canvas.style.height= `${height/sub_scale_constant}px`
}
const default_size = document.querySelector('.canvas-size:checked');
update_size(
    default_size.getAttribute('size')
)

const [custom_width,custom_height] = [
    document.getElementById('width-canvas'),document.getElementById('height-canvas')
]
const custom_size_inputs = document.getElementById('custom-size-inputs');
const handle_update_custom_size = (e)=>{
    if(!(e.target == custom_width || e.target == custom_height)) return;// * no es tan necesaria pero igual quiero validarlo...
    update_size(
        `size:${custom_width.value}x${custom_height.value}`
    );
}
[custom_width,custom_height].forEach((input)=>{
    input.addEventListener('input', handle_update_custom_size);
})
canvas_sizes.forEach((element)=>{
    element.addEventListener('change',radio_button=>{
       update_size(radio_button.target.getAttribute('size'))
       /*
       Este algoritmo es para mostrar u ocultar el panel para poner el custom size.
       */
       if (radio_button.target.id=="custom-size"){
        custom_size_inputs.className = ''
       }
       else{
        custom_size_inputs.className = 'hidden'
       }
    })
})



//padding
const update_padding = (raw_padding)=>{
    mark_settings.padding = parseInt(raw_padding)
    canvas.style.padding = `${mark_settings.padding/sub_scale_constant}px`
    current_padding.innerText = `${mark_settings.padding}px`
}
const btn_adjust_padding = document.getElementById("btn-adjust-padding");
/*
El botón muestra u oculta el panel de control (padding_settings) para ajustar el padding, solo tiene esa funcionalidad.
*/
const padding_range = document.getElementById("padding-range");
const padding_settings = document.getElementById("adjust-padding-controls");
const current_padding = document.getElementById("current-padding");


let is_show_padding_controls = false;
btn_adjust_padding.onclick = ()=>{
    is_show_padding_controls ? (
        padding_settings.className ='hidden'
    ):
    (
        padding_settings.className =''
    )
    is_show_padding_controls = !is_show_padding_controls
}
padding_range.addEventListener('input', (e)=>{
    update_padding(e.target.value)
})

//gap
const update_gap = (raw_gap)=>{
    mark_settings.gap = parseInt(raw_gap)
    current_gap.innerText = `${mark_settings.gap}px`
}
const btn_adjust_gap = document.getElementById("btn-adjust-gap");
/*
El botón muestra u oculta el panel de control (gap_settings) para ajustar el gap, solo tiene esa funcionalidad.
*/
const gap_range = document.getElementById("gap-range");
const gap_settings = document.getElementById("adjust-gap-controls");
const current_gap = document.getElementById("current-gap");


let is_show_gap_controls = false;
btn_adjust_gap.onclick = ()=>{
    is_show_gap_controls ? (
        gap_settings.className ='hidden'
    ):
    (
        gap_settings.className =''
    )
    is_show_gap_controls = !is_show_gap_controls
}
gap_range.addEventListener('input', (e)=>{
    update_gap(e.target.value)
})


// ! background color

const pickr = Pickr.create({
    el: '#btn-bg-color',
    theme: 'classic', // o 'monolith', 'nano' , 'classic'

    components: {
      preview: true,
      opacity: true,
      hue: true,

      interaction: {
        hex: true,
        rgba: true,
        hsla: true,
        input: true,
      }
    }
  });
const background = document.getElementById("mark-result");
pickr.on('change',(color)=>{
    // Obtener el color seleccionado en formato HEXA
    const selectedColor = color.toHEXA().toString();

    
    background.style.background = `linear-gradient(to left,  ${selectedColor}, #E6F6EA,${selectedColor})`;
    canvas.style.backgroundColor = color.toHEXA().toString();
    mark_settings.background_color = color.toRGBA().toString();
})
export {mark_settings}