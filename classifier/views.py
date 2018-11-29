from django.shortcuts import render

# Create your views here.

def classify(request):
    return render(request, 'classfier/home.html')
