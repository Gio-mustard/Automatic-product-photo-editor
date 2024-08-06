## initial
Mantiene las dimensiones originales de cada imagen sobre el canvas, no se aplica ninguna transformación para su escalamiento.

## contain
Calcula a cuanto tiene que redimencionar cada imagen para que todas las imágenes quepan (sean visibles) en el mark stack.

## cover
En caso de que el canvas sea mas grande que las imagenes se les hara un sobre dimensionamiento para que cada imagen ocupe el 100% del height o width del canvas pero nunca los 2 a la vez.

-> Como se sabe si se ocupara el 100% del height o width del canvas ??
La dimension seleccionada para el sobre dimensionamiento sera la dimension mas chica, por ejemplo, si el canvas mide 500x200 las imágenes ocuparan el 100%  del height y el width de cada imagen crecerá según s escala original.
