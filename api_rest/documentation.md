# Documentación del Endpoint de la API

## Descripción General -  make/stack/
POST ```api/v1/make/stack```

Este endpoint está diseñado para manejar solicitudes de procesamiento de imágenes con dos funcionalidades principales:
1. **Apilamiento de Imágenes** - Configurable utilizando `stack_options`.
2. **Eliminación de Fondo** - Configurable utilizando `remove_bg_options`.

Los usuarios deben especificar si desean apilar imágenes, eliminar sus fondos, o realizar ambas acciones. Dependiendo de estas opciones, se deben proporcionar diferentes parámetros y configuraciones.

## Formato de la Solicitud

La solicitud debe enviarse como un objeto JSON con la siguiente estructura:

```json
{
  "images": [<Archivos de Imagen>],
  "has_watermark": <Booleano>,
  "watermark": <Cadena de texto, opcional>,
  "make_stack": <Booleano>,
  "stack_options": {
    "background_color": [[<Cuarteto de números>],[...]],
    "resolution": <Cadena de texto>,
    "padding": <Entero>,
    "gap": <Entero>,
    "alignment": [<Cadena de texto>],
    "scaling": <Cadena de texto>,
    "direction": <Cadena de texto>
  },
  "remove_bg": <Booleano>,
  "remove_bg_options": {
    "background_color": [<Cadena de texto>],
    "hig_detail": <Booleano, opcional>
  }
}
```
## Descripción de los Campos

### Campos Requeridos:
- **images**:  
  - **Tipo**: Lista de archivos de imagen  
  - **Requerido**: Sí  
  - **Descripción**: Una lista que contiene las imágenes a procesar.

- **has_watermark**:  
  - **Tipo**: Booleano  
  - **Requerido**: Sí  
  - **Descripción**: Indica si las imágenes tienen una marca de agua. Si es `True`, el campo `watermark` puede proporcionarse opcionalmente.

- **make_stack**:  
  - **Tipo**: Booleano  
  - **Requerido**: Sí  
  - **Descripción**: Si es `True`, las imágenes se apilarán según la configuración proporcionada en `stack_options`. Si es `True`, el campo `stack_options` se convierte en requerido.

- **remove_bg**:  
  - **Tipo**: Booleano  
  - **Requerido**: Sí  
  - **Descripción**: Si es `True`, se eliminará el fondo de las imágenes según la configuración proporcionada en `remove_bg_options`. Si es `True`, el campo `remove_bg_options` se convierte en requerido.

### Campos Opcionales:
- **watermark**:  
  - **Tipo**: Cadena de texto  
  - **Requerido**: No (opcional)  
  - **Descripción**: Especifica el texto o identificador de la marca de agua a utilizar. Este campo es opcional y solo es relevante si `has_watermark` es `True`.

- **stack_options**:  
  - **Tipo**: Objeto  
  - **Requerido**: Condicionalmente requerido (si `make_stack` es `True`)  
  - **Descripción**: Configuración para apilar imágenes. Los siguientes campos son requeridos dentro de `stack_options`:
    - **background_color**: Lista de números que representa el color en el sistema RGBA.
    - **resolution**: Cadena de texto que representa la resolución deseada.
    - **padding**: Entero que representa el relleno alrededor de las imágenes.
    - **gap**: Entero que representa el espacio entre las imágenes apiladas.
    - **alignment**: Lista de cadenas de texto que especifican opciones de alineación.
    - **scaling**: Cadena de texto que especifica el método de escalado.
    - **direction**: Cadena de texto que especifica la dirección de apilamiento.

- **remove_bg_options**:  
  - **Tipo**: Objeto  
  - **Requerido**: Condicionalmente requerido (si `remove_bg` es `True`)  
  - **Descripción**: Configuración para eliminar el fondo de las imágenes. Los siguientes campos son compatibles dentro de `remove_bg_options`:
    - **background_color**: Lista de cadenas de texto que representan los colores de fondo.
    - **hig_detail**: Booleano (opcional), cuando es `True`, aplica una eliminación de fondo de alto detalle.

## Reglas de Validación

1. **Requisito de `stack_options`**:  
   - Si `make_stack` es `True`, se debe proporcionar el campo `stack_options`.  
   - Si no se proporciona, se genera un error: `"stack_options is required when make_stack is true."`

2. **Requisito de `remove_bg_options`**:  
   - Si `remove_bg` es `True`, se debe proporcionar el campo `remove_bg_options`.  
   - Si no se proporciona, se genera un error: `"remove_bg_options is required when remove_bg is true."`

## Ejemplo de Solicitud

Aquí tienes un ejemplo de una solicitud válida:

```json
{
  "images": ["image1.png", "image2.jpg"],
  "has_watermark": true,
  "watermark": "Marca de Agua de Ejemplo",
  "make_stack": true,
  "stack_options": {
    "background_color": [[255,0,255,255]],
    "resolution": "1920x1080",
    "padding": 10,
    "gap": 5,
    "alignment": ["center"],
    "scaling": "contain", // cover || initial
    "direction": "row" // column
  },
  "remove_bg": false
}
```
## Mensajes de error

### 400
```json
{
  "error": "stack_options is required when make_stack is true."
}
```

## Notas de uso
* Asegúrese de que todos los campos requeridos se proporcionen en el formato correcto.
* Utilice las opciones de configuración apropiadas según sus necesidades de procesamiento (apilamiento de imágenes o eliminación de fondo).