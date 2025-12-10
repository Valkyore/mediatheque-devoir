from django.contrib import admin
from django.urls import path, include
from bibliotheque.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),  # Admin pour données test
    path('biblio/', include('bibliotheque.urls')),  # Routes biblio (/biblio/menu/)
    path('membre/', include('membres.urls')),      # Routes membres (/membre/menu/)
]