from django.shortcuts import render


def error(request):
    if request.method == 'GET':
        return render(request, 'errorpage.html', {'title': 'Error'})
