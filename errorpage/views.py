from django.shortcuts import render
from homepage import static

def error(request):
    if request.method == 'GET':
        return render(request, 'errorpage.html', {'title': 'Error'})
