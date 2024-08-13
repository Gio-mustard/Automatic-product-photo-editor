# Resumen
Para manipular\editar imágenes (que es el objetivo de la app) existe una clase la cual administra cada imagen que instancie a partir de sus bytes o como copia de un objeto `PIL.Image.Image`.
Esta clase es llamada `MarkImage`.

-> Mark no significa nada, solo es una forma de identificar a los objetos o clases del proyecto.

Para manipular y agrupar un conjunto de imágenes existe una clase llamada `MarkStack`.

## MarkImage
Esta clase contiene...
* la imagen en crudo que se abre en la instancia.
* una imagen `Image` que tiene un color solido con canal alpha activo (Solo se ve si la imagen en crudo tiene transparencia).
* un ID el cual no tiene funcionalidad por el momento pero identifica de forma explicita a cada instancia.

Actualmente cada MarkImage tiene la capacidad de...

* Eliminar fondo de una imagen.
* Copiar el contenido creando una nueva instancia.

Y como sub funcionalidades...
* Convertir la instancia en `bytes`.
* Convertir la instancia en `Image`.


### Transform
Una transformación es una función la cual cambia el aspecto de la `MarkImage` entre las transformaciones actuales están...

* default -> esta la tienen todas las MarkImage por defecto y no hace nada.
* rotate
* out_shadow

#### Comportamiento
Una trasformación sigue el siguiente patron...
```py
def default(im:Image.Image,**kwargs)->Image.Image:
    returned = __check_history(im,id_mark_image,rotate)
    if isinstance(returned,Image.Image):return returned
    # do something...
    return im
```
La transformación recibe la imagen , verifica en el historial si esta trasformación ya se aplico y si es asi no la aplica otra vez y solo retorna la imagen.

#### History
El historial es una clase la cual guarda las transformaciones que se le han hecho a cada una de las `MarkImages` activas en el momento.
Cada `MarkImage` tiene un ID el cual se usa para guardar en un diccionario un conjunto con las referencias de las transformaciones que ya se han aplicado al objeto `MarkImage` con ese ID.

Este objeto es necesario ya que no es eficiente aplicar una misma transformación mas de 1 vez a una `MarkImage` ya que en la mayoría de transformaciones requieren crear multiples imágenes para obtener su resultado asi que es mejor que el programador pre calcule con exactitud como quiere que sea el resultado final de su transformación.
#### Como usarla
```py
from transforms import out_shadow
mark_image.set_transform(
    out_shadow,
    blur=10,
    radius=20,
    shadow_color=(0,0,0,150),
    offset=(0,100)
)
mark_image.apply_transform()
```
Es importante no llamar la función de transformación al momento de usar el metodo `set_transform` ya que se usa ese referencia para después ser llamada y actualizar el historial.

## MarkStack
Esta clase puede juntar y administrar una serie de `MarkImage` (en una tupla).

-> Esta clase esta dividida (conceptualmente) en dos partes.
### Canvas
Es un objeto delegado de tipo `Image` el cual es llamado `background` en la propiedad de la clase.
El canvas es la imagen donde se Iran colocando cada una de las `MarkImage` que contenga el `MarkStack`, se van colocando según su orden en la tupla.

### Images
Es la propiedad de tipo tupla en donde se guardan las referencias de cada `MarkImage` dentro de cualquier proceso que pueda tener el `MarkStack` nunca se modifica nada de las referencias a las `MarkImage`.

----
El `MarkStack` agrupa a todas las `MarkImage's` de manera inteligente.

> Puedes ver el archivo [scaling_functions.py](./scaling_funtions.py) para saber como se escalan cada una de las `MarkImage's` en el canvas del `MarkStack`.

> O también puedes ver el resumen de las reglas [aquí](./rules-stale.md).