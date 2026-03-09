from reservations.models import Reservation
from django.utils import timezone

class ReservationRepository:
    @staticmethod
    def create(data):
        return Reservation.objects.create(**data)
        
    @staticmethod
    def get_overlapping_reservations(table_id, start_time, end_time):
        return Reservation.objects.filter(
            table_id=table_id,
            status__in=['pending', 'confirmed'],
            start_time__lt=end_time,
            end_time__gt=start_time
        )

    @staticmethod
    def get_all_active_future():
        now = timezone.now()
        return Reservation.objects.filter(start_time__gte=now).exclude(status='cancelled').order_by('start_time')
