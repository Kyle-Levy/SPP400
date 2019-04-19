from django import template
from assigned_procedures.models import AssignedProcedures

register = template.Library()


@register.filter
def modulo(num, val):
    return num % val


@register.simple_tag()
def average_completion_time(procedure_id):
    return AssignedProcedures.average_completion_time(procedure_id) + " days"


@register.simple_tag()
def assigned_procedure_id(patient, procedure, phase):
    procedures = AssignedProcedures.objects.filter(patient=patient, procedure=procedure, phaseNumber=phase)
    procedure_id = 0
    for proc in procedures:
        procedure_id = proc.id
    return str(procedure_id)
