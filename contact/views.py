from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def contact(request):
    return render(request, template_name='contact.html')