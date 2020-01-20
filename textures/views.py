from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.conf import settings
from textures.models import FileNameModel
import sys, os

# Create your views here.
UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'



def form(request):
    if request.method != 'POST':
        return render(request,'textures/form.html')

    file = request.FILES['file']
    path = os.path.join(UPLOADE_DIR,file.name)
    destination = open(path,'wb')

    for chunk in file.chunks():
        destination.write(chunk)


    insert_data =FileNameModel(file_name= file.name)
    insert_data.save()


    return redirect('textures:complete')


def complete(request):
    return render(request, 'textures/complete.html')
