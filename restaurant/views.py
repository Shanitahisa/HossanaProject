from django.shortcuts import render

# Create your views here.

def resortIndex(request):
    return render(request, 'index-1.html')
