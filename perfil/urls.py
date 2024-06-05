from django.urls import path
from .views import *

app_name= 'perfil'


urlpatterns = [
    path('CreateUser/',Criar.as_view(), name='CreateUser'),
    path('UpdateUser/',Atualizar.as_view(), name='UpdateUser'),
    path('Login/',Login.as_view(),name='Login'),
    path('Logout/',Logout.as_view(),name='Logout'),
]