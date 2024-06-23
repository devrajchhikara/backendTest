from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', admin.site.urls),  # Redirect to Django admin
    path('admin/', admin.site.urls),
    path('api/', include('file_management.urls')),
]
