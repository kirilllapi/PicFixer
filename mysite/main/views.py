from django.shortcuts import render
import numpy as np
import shutil
import cv2
import os
from .forms import UploadFileForm, UploadFileForm_M, UploadFileForm_B
from .models import UploadFiles, UploadFiles_M, UploadFiles_B



# Create your views here.
def index(request):
    os.remove('static/main/img/portfolio/sobel_result.jpg')
    shutil.copy('static/main/img/sobel_result.jpg', 'static/main/img/portfolio/')
    os.remove('static/main/img/portfolio/median_result.jpg')
    shutil.copy('static/main/img/median_result.jpg', 'static/main/img/portfolio/')
    os.remove('static/main/img/portfolio/bil_result.jpg')
    shutil.copy('static/main/img/bil_result.jpg', 'static/main/img/portfolio/')
    return render(request, 'main/index.html')


def handle_uploaded_file(f):
    with open(f"uploads/img.jpg", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def sobel(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'main/method_sobel.html', {'form':form})


def median(request):
    if request.method == 'POST':
        form = UploadFileForm_M(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles_M(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm_M()
    return render(request, 'main/median_filter.html', {'form': form})


def billateral(request):
    if request.method == 'POST':
        form = UploadFileForm_B(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles_B(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm_B()
    return render(request, 'main/billateral_filter.html', {'form':form})

