from django.shortcuts import render

# Create your views here.
def home(request):
    print(f"{request=}")
    return render(request, "index.html")