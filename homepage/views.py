from django.shortcuts import render
from homepage.forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate
# Create your views here.



def home(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
    #  return HttpResponse('<h1> Homepage </h1>')

def about(request):
    return HttpResponse('<h1> Testerooni </h1>')

def login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                return HttpResponse('<h1> auth </h1>')
            else:
                return HttpResponse('<h1> bad </h1>')
                # return render(request, 'login.html', {'form': LoginForm()})
