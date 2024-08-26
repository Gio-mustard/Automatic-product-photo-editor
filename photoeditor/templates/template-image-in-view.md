-> Este es el template para agregar una nueva imagen en el dom y en el stack de manera visual solamente.
```jinja
{% comment %} ! esto solo es un template se tiene que quitar antes del commit {% endcomment %}
                {% comment %} TODO : crea  un documento que explique como agregar imagenes aqui{% endcomment %}
                <div class="image-in-view">
                    <button class='delete btn-delete-from-view'>
                        <img src="{%static 'img/ic_trash.png'%}">
                    </button>
                    <img src="{% static 'img/test.jpg'%}" id='xxxxxxx'>
                </div>
                <div class="image-in-view">
                    <button class='delete btn-delete-from-view'>
                        <img src="{%static 'img/ic_trash.png'%}">
                    </button>
                    <img src="{% static 'img/(15).jpg'%}" id='xxxxxxx'>
                </div>
```
En `imagas-view` hay un `input:file` que se usara para almacenar de manera temporal las imagenes del stack, cuando el contenido del `input:file` cambie se refrescara las imagenes que se ven en el DOM.