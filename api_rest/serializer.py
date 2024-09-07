# myapp/serializers.py
from rest_framework import serializers
from django.core.files.uploadedfile import TemporaryUploadedFile,InMemoryUploadedFile

required_fields = ('make_stack', 'remove_bg', 'has_watermark')

class StackOptionsSerializer(serializers.Serializer):
    background_color = serializers.ListField(child=serializers.ListField(),required=True)
    resolution = serializers.CharField(required=True)
    padding = serializers.IntegerField(required=True)
    gap = serializers.IntegerField(required=True)
    alignment = serializers.ListField(child=serializers.CharField(),required=True)
    scaling = serializers.CharField(required=True)
    direction = serializers.CharField(required=True)

class RemoveBgOptionsSerializer(serializers.Serializer):
    background_color = serializers.ListField(child=serializers.IntegerField(),required=True)
    hig_detail = serializers.BooleanField(required=False)

class RequestValidatorSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField(), required=True)
    has_watermark = serializers.BooleanField(required=True)
    watermark = serializers.CharField(required=False, allow_null=True,allow_blank=True)
    make_stack = serializers.BooleanField(required=True)
    stack_options = StackOptionsSerializer(required=False)
    remove_bg = serializers.BooleanField(required=True)
    remove_bg_options = RemoveBgOptionsSerializer(required=False)
    has_background_image = serializers.BooleanField(required=True)
    background_image = serializers.ListField(required=True)

    def validate(self, data):
        # Validar stack_options si make_stack es True
        
        if 'stack_options' not in data and data['make_stack']:
            raise serializers.ValidationError("stack_options is required when make_stack is true.")
        
        # Validar remove_bg_options si remove_bg es True
        if 'remove_bg_options' not in data and data['remove_bg'] :
            raise serializers.ValidationError("remove_bg_options is required when remove_bg is true.")
                
        if (
            (data['has_background_image'] == True and 'background_image' in data )
                and
                type(data['background_image'][0]) not in [TemporaryUploadedFile,InMemoryUploadedFile]
                ):
            raise serializers.ValidationError("background_image is required when has_background_image is true.")

        return data
        