from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from . serializer import RequestValidatorSerializer
from . request_interpreter import Interpreter
from . tools import fix_request_types
from django.http import HttpResponse
# Create your views here.

interpreter = Interpreter()

@api_view(['POST'])
def make_stack(request:Request)->Response:
    data = {**request.data}
    data = fix_request_types(data)
    serializer = RequestValidatorSerializer(data = data)
    if not serializer.is_valid():
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    buffer,mimetype = interpreter.make_stack(data)
    response = HttpResponse(buffer, content_type=f'image/{mimetype.lower()}',status=status.HTTP_201_CREATED)
    response['Content-Disposition'] = f'inline; filename="mi_imagen.{mimetype.lower()}"'
    return response