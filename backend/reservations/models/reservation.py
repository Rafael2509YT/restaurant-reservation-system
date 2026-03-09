import uuid
from django.db import models
from .table import Table

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ]
    
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name='reservations')
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation {self.unique_code} for {self.name} on {self.date} at {self.time}"
