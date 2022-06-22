from django import template
register = template.Library()

from users.models import Profile

@register.simple_tag
def adding(request):
    my_profile =Profile.objects.get(name =request.user)
    
    return my_profile