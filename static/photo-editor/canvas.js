const mark_settings = {
    padding:0,
    size:null,
    backgroundColor:null,
}

const canvas = document.getElementById('canvas');
// canvas size
const canvas_sizes = [...document.getElementsByClassName('canvas-size')];
const update_size =(raw_size)=>{
    const [width,height] = raw_size.split(":")[1].split('x')
    mark_settings.size = `${width}x${height}`
    canvas.style.width = `${width/4}px`
    canvas.style.height= `${height/4}px`
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
    if(!(e.target == custom_width || e.target == custom_height)) return;
    update_size(
        `size:${custom_width.value}x${custom_height.value}`
    );
}
[custom_width,custom_height].forEach((input)=>{
    input.addEventListener('input', handle_update_custom_size);
})
canvas_sizes.forEach((element)=>{
    element.addEventListener('change',e=>{
       update_size(e.target.getAttribute('size'))
       if (e.target.id=="custom-size"){
        custom_size_inputs.className = ''
       }
       else{
        custom_size_inputs.className = 'hidden'
       }
    })
})



//padding
const update_padding = (raw_padding)=>{
    mark_settings.padding = raw_padding
    canvas.style.padding = `${mark_settings.padding/4}px`
    current_padding.innerText = `${mark_settings.padding}px`
}
const btn_adjust_padding = document.getElementById("btn-adjust-padding");
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
    mark_settings.backgroundColor = color.toRGBA().toString();
})