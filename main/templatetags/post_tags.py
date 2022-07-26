from django import template
from ..models import Invitation, Module
register = template.Library()

@register.simple_tag
def modules():
    module_list = Module.objects.count()
    return module_list


@register.simple_tag
def get_status(test,user):
    return test.get_invitation(user).status

@register.simple_tag
def notif_test(user):
    return Invitation.objects.filter(candidat=user.candidat,status = 0).count()