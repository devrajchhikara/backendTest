from django.contrib import admin
from .models import User, UploadedFile

admin.site.register(User)
admin.site.register(UploadedFile)
