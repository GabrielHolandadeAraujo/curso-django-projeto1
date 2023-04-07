from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    # o path na url do app terá a url e a chamada da função criada para renderizar o template escolhido 
    # É necessário importar a viws do próprio app para ter aceso a função, o nome no terceiro argumento 
    # é opcional, mas serve para identificar o caminho, então é recomendado
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
