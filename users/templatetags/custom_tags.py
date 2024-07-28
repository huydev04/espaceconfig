from django import template
from django.conf import settings
import os

register = template.Library()

@register.simple_tag
def show_image(name):
    if name != None:
        filename = os.path.join('thumbnails', name)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        print("File Path: ", file_path)  # Kiểm tra đường dẫn tệp
        
        if os.path.exists(file_path):
            image_url = os.path.join(settings.MEDIA_URL, filename)
        else:
            image_url = None
        return image_url
    else: return ""

@register.simple_tag
def downloadfile(name):
    if name != None:
        filename = os.path.join('documents', name)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        print("File Path: ", file_path)  # Kiểm tra đường dẫn tệp
        
        if os.path.exists(file_path):
            doc_url = os.path.join(settings.MEDIA_URL, filename)
        else:
            doc_url = None
        return doc_url
    else: return ""

@register.simple_tag
def avatar(name):
    app_static_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'static', 'images', 'avatar'
    )
    if name:
        file_path = os.path.join(app_static_dir, name)
        
        if os.path.exists(file_path):
            return os.path.join(settings.STATIC_URL, 'images', 'avatar', name)
    return os.path.join(settings.STATIC_URL,'images', 'avatar', 'avatar.png')