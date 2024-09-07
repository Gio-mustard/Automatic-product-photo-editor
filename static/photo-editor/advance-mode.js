import { mark_settings } from "./canvas.js";

const btn_advance_mode = document.getElementById('btn-open-advance-mode');
const container = document.getElementById('advance-options-aside');

const initial_bg_color = "rgba(0,0,0,0)"
const advance_options = {
    has_watermark:false,
    watermark:"",
    remove_bg:false,
    remove_bg_options:{
        apply_bg_color:false,
        background_color:initial_bg_color,
        hig_detail:false
    },
    has_background_image:false,
    background_image:[]
}
let is_hidden = true;
let sub_menus_open = 0;
const settings_stack = document.getElementById('settings-stack');
const update_dom_from = (container,is_show)=>{
    /*
    Muestra u oculta una sub opción del modo avanzado que se le pase por parámetro
    */
    if (is_show){
        container.style.height = "5vh";
        container.style.opacity = "1";
        sub_menus_open++;
    }
    else{
        container.style.height = "0px";
        container.style.opacity = "0"; 
        sub_menus_open--;
        if (sub_menus_open < 0)sub_menus_open=0;
    }
    const stack_spans = [...settings_stack.getElementsByTagName('span')]
    const stack_options = [...settings_stack.getElementsByTagName('div')]
    if (sub_menus_open == 2){
        stack_spans.forEach(e=>e.style.display="none");
        stack_options.forEach(e=>e.classList.add('contracted'));
    }
    else{
        stack_spans.forEach(e=>e.style.display="block");
        stack_options.forEach(e=>e.classList.remove('contracted'));
    }
}
btn_advance_mode.onclick = ()=>{
    if (is_hidden) {
        container.className = "";
        btn_advance_mode.textContent = "Close Advance";
    }
    else{
        container.className = "hidden";
        btn_advance_mode.textContent = "Open Advance";
    }
    is_hidden = !is_hidden;
}


// settings for each image
//* remove background
const remove_background = document.getElementById('remove-background')
remove_background.onchange = (e)=>{
    advance_options.remove_bg = e.target.checked;
}
//* hig detail
const hig_detail = document.getElementById('hig-detail');
hig_detail.onchange = (e)=>{
    advance_options.remove_bg_options.hig_detail = e.target.checked;
}
// * 

// * advance background color
const bg_color_options = document.getElementById('bg-color-options');
const check_apply_bg_color = document.getElementById('apply-bg-color');
// const initial_color = "#917DFE"

const pickr = Pickr.create({
    el: `#advance-bg-color`,
    theme: 'monolith', // o 'monolith', 'nano' , 'classic'
comparison: false,
default:initial_bg_color,
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

pickr.on('change',(color)=>{
    if (advance_options.remove_bg_options.apply_bg_color){
        advance_options.remove_bg_options.background_color = color.toRGBA().toString();
    }
})
check_apply_bg_color.onchange = (e)=>{
    advance_options.remove_bg_options.apply_bg_color = e.target.checked;
    update_dom_from(bg_color_options,e.target.checked);
}

// watermark
const has_watermark = document.getElementById('has-watermark');
const watermark = document.getElementById('watermark');

has_watermark.onchange = (e)=>{
    advance_options.watermark = watermark.textContent;
    update_dom_from(watermark,e.target.checked)
}

// settings stack

// direction
const directions = [ document.getElementById('row-direction'),document.getElementById('column-direction') ];// row,column
directions.forEach((button)=>{
    button.addEventListener('click',function(e){
        directions.forEach(button=>button.classList.remove('active'));
        e.target.classList.add('active');
        mark_settings.direction = e.target == directions[0] ? 'row': 'column';
    })
})
const init_direction = ()=>{
    directions.forEach((button,index)=>{
        if (button.classList.contains('active')){
            mark_settings.direction = index == 0 ? 'row' : 'column';
        }
    });
}

// alignment
const alignments = [...document.getElementsByClassName('alignments-options')];
// each id : [top-lef,top-center,bottom-left,bottom-center + align]

alignments.forEach((button)=>{
    button.addEventListener('click',  (e)=>{
        alignments.forEach(button=>button.classList.remove('active'))
        e.target.classList.add('active')
        update_alignment();
        
    })
})
const update_alignment = ()=>{
    for (let i = 0; i < alignments.length; i++) {
        if (!(alignments[i].classList.contains('active')))continue;
        switch(i){
            case 0:
                mark_settings.alignment=[];
                break
            case 1:
                mark_settings.alignment = ['horizontal'];
                break;
            case 2:
                mark_settings.alignment = ['vertical'];
                break;
            case 3:
                mark_settings.alignment = ['vertical','horizontal'];
                break;

        }
    }
}
// scaling
const scale_options = [...document.getElementsByClassName('scale-label')];
scale_options.forEach((element)=>{
    element.onclick = e=>{
        //TODO : hay que hacer otro sistema de verificación de scales.
        mark_settings.scaling =  e.target.textContent
    }
})
// background image
const background_drop_area = document.getElementById('drop-background');
const background_input = document.getElementById('background-input');
const preview_drop_background = document.getElementById('preview-drop-background')
const update_background_image = (file)=>{
    advance_options.background_image = file
    advance_options.has_background_image = true;
    preview_drop_background.src = URL.createObjectURL(advance_options.background_image);
}
background_drop_area.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    const files = Array.from(dt.files)
    update_background_image(files[0])
}, false);
background_drop_area.onclick = ()=>{
    if (advance_options.has_background_image){
        advance_options.has_background_image = false;
        advance_options.background_image = [];
        preview_drop_background.src='';
    }
    else{
        background_input.click();
    }
}
background_input.onchange = (e)=>{
    update_background_image(e.target.files[0]);
};
// ! Initialized
update_dom_from(watermark,has_watermark.checked);
update_dom_from(bg_color_options,check_apply_bg_color.checked);
scale_options[1].click();
init_direction();
update_alignment();
export {advance_options};