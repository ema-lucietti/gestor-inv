from django.db import models
from django.core.exceptions import ValidationError

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Ubicaciones"

class Pallet(models.Model):
    numero_pallet = models.CharField(max_length=50, unique=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pallet {self.numero_pallet} en {self.ubicacion}"
    
    @property
    def total_productos(self):
        return self.productos.count()
    
    @property
    def total_stock(self):
        return sum(producto.cantidad for producto in self.productos.all())
    
class Producto(models.Model):
    pallet = models.ForeignKey(Pallet, on_delete=models.CASCADE, related_name='productos')
    codigo_barras = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    cantidad = models.IntegerField()    

    def __str__(self):
         return f"{self.nombre} ({self.cantidad})"
    
    def clean(self):
        if self.cantidad < 0:
            raise ValidationError('La cantidad no puede ser negativa')


class RemitoSalida(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    destino = models.CharField(max_length=200)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Remito {self.id} - {self.destino} ({self.fecha.strftime('%d/%m/%Y')})"
    
    @property
    def total_items(self):
        return sum(detalle.cantidad for detalle in self.detalles.all())
    
    class Meta:
        verbose_name_plural = "Remitos de Salida"
        ordering = ['-fecha']


class DetalleSalida(models.Model):
    remito = models.ForeignKey(RemitoSalida, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    
    class Meta:
        verbose_name_plural = "Detalles de Salida"

    def clean(self):
        if self.producto and self.cantidad:
            if self.cantidad > self.producto.cantidad:
                raise ValidationError(
                    f'Stock insuficiente para {self.producto.nombre}. '
                    f'Stock disponible: {self.producto.cantidad}'
                )

    def save(self, *args, **kwargs):
        # Validar antes de guardar
        self.clean()
        
        # Si es una nueva instancia, descontar del stock
        if not self.pk:
            if self.producto.cantidad < self.cantidad:
                raise ValidationError(f"Stock insuficiente para {self.producto.nombre}")
            
            self.producto.cantidad -= self.cantidad
            self.producto.save()
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Si se elimina un detalle, devolver el stock
        self.producto.cantidad += self.cantidad
        self.producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} - Cant: {self.cantidad}"