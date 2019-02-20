from django.shortcuts import render
from procedures.forms import ProceduresTemplate
from django.http import HttpResponse


def index(request):
    if request.method == 'POST':
        form = ProceduresTemplate(request.POST)
        if form.is_valid():
            return render(request, 'procedures.html', {'form': ProceduresTemplate()})
    else:
        form = ProceduresTemplate()
        return render(request, 'procedures.html', {'form': ProceduresTemplate()})
