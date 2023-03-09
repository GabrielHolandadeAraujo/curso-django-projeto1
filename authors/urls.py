from django.urls import path

from . import views

urlpatterns = [
    # o path na url do app terá a url e a chamada da função criada para renderizar o template escolhido 
    # É necessário importar a viws do próprio app para ter aceso a função, o nome no terceiro argumento 
    # é opcional, mas serve para identificar o caminho, então é recomendado
    path('register/', views.register_view, name='register'),
]
