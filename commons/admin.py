from django.contrib import admin
from .models import Trabajador, Calificacion, AreaEjerce, AreaTrabajo

class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'precio', 'experiencia', 'descripcion')

class AreaEjerceAdmin(admin.ModelAdmin):
    list_display = ('id_area', 'id_trabajador')

# Register your models here.
admin.site.register(Trabajador, TrabajadorAdmin)
admin.site.register(Calificacion)
admin.site.register(AreaEjerce, AreaEjerceAdmin)
admin.site.register(AreaTrabajo)