from django.db import models

class Table(models.Model):
    number = models.CharField(max_length=10, unique=True)
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.number} (Capacity: {self.capacity})"
