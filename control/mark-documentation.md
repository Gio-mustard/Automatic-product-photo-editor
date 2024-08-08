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
