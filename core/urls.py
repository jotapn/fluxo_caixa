from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    #path('',admin.site.urls),
    path('cadastro/',include("cadastro.urls")),
    path('operacoes/',include("operacoes.urls")),
    path('accounts/', include('allauth.urls')),
]
