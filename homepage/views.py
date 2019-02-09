from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'login.html')
    #  return HttpResponse('<h1> Homepage </h1>')

def about(request):
    return HttpResponse('<h1> Testerooni </h1>')