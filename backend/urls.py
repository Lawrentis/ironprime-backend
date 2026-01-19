from django.contrib import admin
from django.urls import path
from construccion.views import contacto_form  # ← Importa desde tu app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/contacto/', contacto_form, name='contacto_form'),
]