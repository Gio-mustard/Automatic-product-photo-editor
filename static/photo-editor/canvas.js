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
const bg_colors = [

]
const btn_add_bg_color = document.getElementById("btn-add-bg-color");
const max_selectors = 5;
const default_colors = [
    'rgba(255, 179, 186, 1)', 'rgba(255, 223, 186, 1)', 'rgba(255, 255, 186, 1)',
    'rgba(186, 255, 201, 1)', 'rgba(186, 225, 255, 1)', 'rgba(255, 205, 210, 1)',
    'rgba(248, 187, 208, 1)', 'rgba(197, 202, 233, 1)', 'rgba(255, 245, 157, 1)',
    'rgba(129, 212, 250, 1)', 'rgba(244, 143, 177, 1)', 'rgba(240, 98, 146, 1)',
    'rgba(186, 104, 200, 1)', 'rgba(171, 71, 188, 1)', 'rgba(149, 117, 205, 1)',
    'rgba(121, 134, 203, 1)', 'rgba(100, 181, 246, 1)', 'rgba(79, 195, 247, 1)',
    'rgba(77, 208, 225, 1)', 'rgba(77, 182, 172, 1)', 'rgba(129, 199, 132, 1)',
    'rgba(174, 213, 129, 1)', 'rgba(220, 231, 117, 1)', 'rgba(255, 241, 118, 1)',
    'rgba(255, 238, 88, 1)', 'rgba(255, 202, 40, 1)', 'rgba(255, 183, 77, 1)',
    'rgba(255, 138, 101, 1)', 'rgba(161, 136, 127, 1)', 'rgba(141, 110, 99, 1)',
    'rgba(255, 204, 128, 1)', 'rgba(255, 255, 141, 1)', 'rgba(178, 235, 242, 1)',
    'rgba(128, 222, 234, 1)', 'rgba(178, 223, 219, 1)', 'rgba(128, 203, 196, 1)',
    'rgba(165, 214, 167, 1)', 'rgba(230, 238, 156, 1)', 'rgba(255, 224, 130, 1)',
    'rgba(239, 154, 154, 1)', 'rgba(229, 115, 115, 1)', 'rgba(244, 143, 177, 1)',
    'rgba(206, 147, 216, 1)', 'rgba(179, 157, 219, 1)', 'rgba(159, 168, 218, 1)',
    'rgba(100, 181, 246, 1)', 'rgba(77, 208, 225, 1)', 'rgba(128, 222, 234, 1)',
    'rgba(128, 203, 196, 1)', 'rgba(165, 214, 167, 1)', 'rgba(255, 255, 141, 1)',
    'rgba(255, 241, 118, 1)', 'rgba(255, 202, 40, 1)', 'rgba(255, 167, 38, 1)',
    'rgba(255, 204, 128, 1)', 'rgba(255, 204, 188, 1)', 'rgba(255, 224, 178, 1)',
    'rgba(255, 245, 157, 1)', 'rgba(178, 223, 219, 1)', 'rgba(128, 203, 196, 1)',
    'rgba(179, 229, 252, 1)', 'rgba(130, 177, 255, 1)', 'rgba(180, 137, 255, 1)',
    'rgba(204, 156, 218, 1)', 'rgba(161, 157, 215, 1)', 'rgba(147, 169, 210, 1)',
    'rgba(120, 181, 223, 1)', 'rgba(90, 189, 230, 1)', 'rgba(83, 192, 204, 1)',
    'rgba(82, 191, 167, 1)', 'rgba(123, 201, 138, 1)', 'rgba(180, 210, 116, 1)',
    'rgba(250, 222, 129, 1)', 'rgba(250, 240, 150, 1)', 'rgba(250, 204, 124, 1)',
    'rgba(240, 144, 101, 1)', 'rgba(216, 115, 118, 1)', 'rgba(219, 132, 132, 1)',
    'rgba(240, 105, 144, 1)', 'rgba(200, 123, 210, 1)', 'rgba(180, 138, 211, 1)',
    'rgba(154, 156, 213, 1)', 'rgba(134, 171, 218, 1)', 'rgba(120, 192, 233, 1)',
    'rgba(80, 209, 236, 1)', 'rgba(76, 195, 191, 1)', 'rgba(90, 199, 145, 1)',
    'rgba(137, 215, 120, 1)', 'rgba(198, 225, 138, 1)', 'rgba(239, 238, 140, 1)',
    'rgba(239, 234, 112, 1)', 'rgba(239, 220, 98, 1)', 'rgba(249, 196, 77, 1)'
  ];

function choice(array) {
    if (array.length === 0) {
      return null;
    }
    const random_index = Math.floor(Math.random() * array.length);
    return array[random_index];
  }
const bg_color_maker = document.getElementById('bg-color-maker'); // este es el container

btn_add_bg_color.onclick = async ()=>{
    if (max_selectors == bg_colors.length) return
    const new_bg_color_selector = document.createElement('button');
    new_bg_color_selector.id = `btn-bg-color-${bg_colors.length}`;
    bg_color_maker.appendChild(new_bg_color_selector);
    const initial_color = choice(default_colors)
    bg_colors.push({id:new_bg_color_selector.id,color:initial_color});
    const new_pickr = Pickr.create({
        el: `#${new_bg_color_selector.id}`,
        theme: 'monolith', // o 'monolith', 'nano' , 'classic'
    comparison: false,
    default:initial_color,
        components: {
          preview: false,
          opacity: true,
          hue: true,
    
          interaction: {
            hex: true,
            rgba: true,
            hsla: false,
            input: true,
          }
        }
      });
    update_preview_bg_color();
    new_pickr.on('change',(color)=>{
        const element  = bg_colors.find((value)=>{
            return value.id == new_bg_color_selector.id 
        })
        element.color = color.toRGBA().toString();
        new_bg_color_selector.style.backgroundColor = color.toHEXA().toString();
        update_preview_bg_color();
    })
}
const background = document.getElementById("mark-result");
function roundRGBA(rgbaString) {
    // Utilizar una expresión regular para extraer los valores de RGBA
    const rgbaPattern = /rgba?\(([^)]+)\)/;
    const match = rgbaString.match(rgbaPattern);

    if (!match) {
        throw new Error('El formato del string no es válido');
    }

    // Obtener los valores de RGBA como un array de números
    const rgbaValues = match[1].split(',').map(value => parseFloat(value.trim()));

    // Redondear los valores de R, G y B
    const roundedR = Math.round(rgbaValues[0]);
    const roundedG = Math.round(rgbaValues[1]);
    const roundedB = Math.round(rgbaValues[2]);
    const alpha = rgbaValues[3]; // Mantener el valor alpha sin cambios

    // Construir el nuevo string RGBA
    return `rgba(${roundedR}, ${roundedG}, ${roundedB}, ${alpha})`;
}

const update_preview_bg_color = () => {
    return;
    if (bg_colors.length == 1){
        background.style.backgroundColor = bg_colors[0].color
        // canvas.style.backgroundColor = bg_colors[0].color
    }
    else{
        let gradient = 'linear-gradient(to right, '
        bg_colors.forEach(element => {
            gradient +=  roundRGBA(element.color) + ' , '
        })
        gradient = gradient.slice(0, -2);
        gradient += ')'
        background.style.background = gradient
        // canvas.style.background = gradient
    }
}
mark_settings.background_color = bg_colors
window.mark_settings = mark_settings
export {mark_settings}