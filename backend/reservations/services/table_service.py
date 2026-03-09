from rest_framework.exceptions import ValidationError
from reservations.models import Table

class TableService:
    @staticmethod
    def delete_table(table_id):
        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            raise ValidationError("No se encontró la mesa.")
            
        from reservations.models import Reservation
        from django.utils import timezone
        now = timezone.localtime().date()
        
        # Verificar si la mesa tiene reservaciones futuras
        future_res = Reservation.objects.filter(
            table=table, 
            date__gte=now,
            status__in=['pending', 'confirmed']
        ).exists()
        
        if future_res:
            raise ValidationError("No se puede eliminar la mesa con reservaciones futuras.")
        
        table.delete()
    @staticmethod
    def update_table(table_id, data):
        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            raise ValidationError("No se encontró la mesa.")
            
        new_capacity = data.get('capacity')
        if new_capacity is not None:
            new_capacity = int(new_capacity)
            if new_capacity < table.capacity:
                from reservations.models import Reservation
                from django.utils import timezone
                now = timezone.localtime().date()
                
                # Check if any future reservation exceeds new capacity
                if Reservation.objects.filter(
                    table=table,
                    date__gte=now,
                    status__in=['pending', 'confirmed'],
                    guests__gt=new_capacity
                ).exists():
                    raise ValidationError(f"No se puede reducir la capacidad a {new_capacity} porque hay reservaciones futuras con más invitados.")
        
        from reservations.serializers.table_serializer import TableSerializer
        serializer = TableSerializer(table, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        raise ValidationError(serializer.errors)
