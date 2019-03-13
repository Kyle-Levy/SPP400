from django.shortcuts import render


def error(request):
    return render(request, 'errorpage.html', {'title': 'Error'})
