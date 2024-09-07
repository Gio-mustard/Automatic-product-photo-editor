from django.shortcuts import render
from .default_canvas_sizes import sizes,scales
# Create your views here.
def editor(request):
    context = {
        "canvas_sizes":sizes,
        "scales":scales
    }
    return render(request,"index_editor.html",context)