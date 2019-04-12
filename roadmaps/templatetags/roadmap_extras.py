from django import template
from assigned_procedures.models import AssignedProcedures

register = template.Library()


@register.filter
def modulo(num, val):
    return num % val


@register.simple_tag()
def average_completion_time(procedure_id):
    return AssignedProcedures.average_completion_time(procedure_id)
