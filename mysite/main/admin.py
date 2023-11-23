from django.contrib import admin
from .models import UploadFiles, UploadFiles_M, UploadFiles_B
# Register your models here.
admin.site.register(UploadFiles)
admin.site.register(UploadFiles_M)
admin.site.register(UploadFiles_B)