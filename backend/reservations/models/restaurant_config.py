from django.db import models
from datetime import time

class RestaurantConfig(models.Model):
    opening_time = models.TimeField(default=time(18, 0))
    closing_time = models.TimeField(default=time(23, 0))
    # Available reservation intervals (e.g., every 30 mins)
    reservation_interval_minutes = models.IntegerField(default=30)
    # How long a block of reservation lasts (e.g., 90 mins)
    reservation_duration_minutes = models.IntegerField(default=90)

    class Meta:
        verbose_name = "Restaurant Configuration"
        verbose_name_plural = "Restaurant Configurations"

    def __str__(self):
        return f"Config (Hours: {self.opening_time.strftime('%H:%M')} - {self.closing_time.strftime('%H:%M')})"

    def save(self, *args, **kwargs):
        if not self.pk and RestaurantConfig.objects.exists():
            return
        super().save(*args, **kwargs)
