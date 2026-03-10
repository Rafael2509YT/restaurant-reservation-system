import uuid
from django.db import models
from .table import Table

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ]
    
    # [MODELOS] Uso de UUID para códigos de cancelación únicos y seguros.
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # [MODELOS] Relación ForeignKey con Table, usando PROTECT para integridad referencial.
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name='reservations')
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    
    # [MODELOS] Uso de choices para manejar estados finitos de la reserva.
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    
    # [MODELOS] Timestamps automáticos para trazabilidad de creación.
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Reservation {self.unique_code} for {self.name} on {self.date} at {self.time}"
