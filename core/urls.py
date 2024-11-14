from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('clientes/',include("clientes.urls")),
    path('',include("transacoes.urls")),
    path('',include("bancos.urls")),
    path('operacoes/',include("operacoes.urls")),
]
