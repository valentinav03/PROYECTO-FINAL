from django.db import models
from django.contrib.auth.models import User

class Trabajador(models.Model):

    precio = models.IntegerField()
    experiencia = models.IntegerField()
    descripcion = models.CharField(max_length=150)
    id_cuenta = models.IntegerField()
    calificacion_promedio = models.FloatField(default=0.0)

    def __str__(self):
        # Obtener el objeto de autenticación del trabajador
        try:
            user = User.objects.get(id=self.id_cuenta)
            return f"{user.username}-{user.email}-{self.precio}-{self.experiencia}-{self.descripcion}-{self.calificacion_promedio}"
        except User.DoesNotExist:
            return f"Trabajador {self.id_cuenta}"

        return f"{self.precio}-{self.experiencia}-{self.descripcion}"
        
    
class Calificacion(models.Model):

    nota = models.IntegerField()
    id_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)

    pass

class AreaTrabajo(models.Model):

    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class AreaEjerce(models.Model):

    id_area = models.ForeignKey(AreaTrabajo, on_delete=models.CASCADE)
    id_trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)