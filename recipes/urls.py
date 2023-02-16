from django.urls import path
from recipes.views import home, apagar

urlpatterns = [
    path('', home),
    path('apagar/', apagar)
]
