from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('<int:area_id>/', views.index, name='index_with_area_id'),
    path('login/', views.login_page, name='login'),
    path('registro/', views.registro_page, name='registro'),
    path('editarPerfil/', views.edit_page, name='editarPerfil'),
    path('trabajador/', views.trabajador, name='trabajador')
]