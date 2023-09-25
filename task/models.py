from django.db import models

# Create your models here.
class MenuInsert(models.Model):
    plato=models.CharField(max_length=200)
    tipo=models.CharField(max_length=200)
    class Meta:
        db_table="menu"

class Plato(models.Model):
    plato = models.CharField(max_length=100)
    clase = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    contenido = models.CharField(max_length=100)
    costo = models.CharField(max_length=100)
    estado = models.IntegerField()
    fecha_registro = models.DateTimeField()
    class Meta:
        db_table="plato"


