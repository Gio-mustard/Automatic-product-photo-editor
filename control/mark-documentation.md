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