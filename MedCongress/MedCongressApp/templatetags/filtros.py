from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
       group = Group.objects.get(name=group_name) 
       return True if group in user.groups.all() else False

@register.filter(name='my_div')
def my_div(num, div): 
       
       return True if int(num+1)%int(div)==0 else False