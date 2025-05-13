from django import template

register = template.Library()

@register.filter(name='file_extension')
def file_extension(file_url, extension):
    return file_url.lower().endswith(extension)