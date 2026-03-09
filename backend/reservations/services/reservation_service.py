from datetime import datetime, timedelta, date, time
from django.utils import timezone
from django.db import transaction
from rest_framework.exceptions import ValidationError
from reservations.models import Table, Reservation, RestaurantConfig

class ReservationService:
    @staticmethod
    def create_reservation(data):
        table_id = data.get('table_id')
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        res_date_str = data.get('date')
        res_time_str = data.get('time')
        guests = data.get('guests')

        if not all([table_id, name, res_date_str, res_time_str, guests]):
            raise ValidationError("Missing required fields.")

        try:
            guests = int(guests)
            res_date = datetime.strptime(res_date_str, '%Y-%m-%d').date()
            res_time = datetime.strptime(res_time_str, '%H:%M:%S').time() if len(res_time_str) > 5 else datetime.strptime(res_time_str, '%H:%M').time()
        except ValueError:
            raise ValidationError("Invalid date/time/guests format.")


        #se valida si la fecha es menor a la actual
        # Rule 1: Cannot reserve in the past
        now = timezone.localtime()
        res_datetime = timezone.make_aware(datetime.combine(res_date, res_time))
        #si la fecha es menor o igual a la actual no permite reservar
        if res_datetime <= now:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed reservation: past time {res_datetime}")
            raise ValidationError("Cannot reserve in the past.")

        config = RestaurantConfig.objects.first()
        if not config:
            raise ValidationError("System configuration missing.")

        # Regla 2: La reserva debe estar dentro del horario de atención del restaurante
        # ---------------------------------------------------------------------------

        # Crea un objeto datetime completo uniendo la fecha elegida con la hora de apertura configurada y le añade la zona horaria (timezone aware)
        opening_dt = timezone.make_aware(datetime.combine(res_date, config.opening_time))

        # Crea un objeto datetime completo uniendo la fecha elegida con la hora de cierre configurada y le añade la zona horaria
        closing_dt = timezone.make_aware(datetime.combine(res_date, config.closing_time))

        # Verifica si el horario de cierre es menor al de apertura (ejemplo: abre 7:00 PM y cierra 2:00 AM del día siguiente)
        if config.closing_time < config.opening_time:
            # Si cierra de madrugada, le suma un día a la fecha de cierre para que la comparación sea lógica
            closing_dt += timedelta(days=1)

        # Define cuánto tiempo durará la reserva convirtiendo los minutos configurados en un objeto de tiempo (timedelta)
        duration = timedelta(minutes=config.reservation_duration_minutes)

        # Valida dos condiciones: 
        # 1. Que la reserva no empiece antes de abrir.
        # 2. Que la reserva sumada a su duración no termine después de la hora de cierre.
        if res_datetime < opening_dt or res_datetime + duration > closing_dt:
            # Si alguna de las condiciones falla, lanza un error de validación que detiene el proceso
            raise ValidationError("Reservation is outside operating hours.")

        
        # --- MANEJO DE CONCURRENCIA Y PREVENCIÓN DE DOBLE RESERVA ---
        # Se utiliza un bloque 'transaction.atomic' para asegurar que todas las operaciones 
        # se realicen como una sola unidad. Si algo falla, no se guarda nada en la BD.
        with transaction.atomic():
            # 1. Intentar validar la mesa solicitada originalmente
            table = None
            try:
                requested_table = Table.objects.select_for_update().get(id=table_id, is_active=True)
                # Verificar si la mesa solicitada cumple con la capacidad y disponibilidad
                if requested_table.capacity >= guests:
                    # Verificar solapamiento para esta mesa específica
                    existing_reservations = Reservation.objects.filter(
                        table=requested_table,
                        date=res_date,
                        status__in=['pending', 'confirmed']
                    )
                    
                    res_end_datetime = res_datetime + duration
                    overlap = False
                    for existing_res in existing_reservations:
                        ext_start = timezone.make_aware(datetime.combine(existing_res.date, existing_res.time))
                        ext_end = ext_start + duration
                        if (res_datetime < ext_end) and (res_end_datetime > ext_start):
                            overlap = True
                            break
                    
                    if not overlap:
                        table = requested_table
            except Table.DoesNotExist:
                pass

            # 2. Si la mesa original no sirve (capacidad/disponibilidad), buscar OTRA mesa automáticamente
            if not table:
                # Buscamos mesas activas que SI tengan la capacidad
                # Ordenamos por capacidad ascendente para usar la "más pequeña que quepa"
                candidate_tables = Table.objects.filter(
                    is_active=True, 
                    capacity__gte=guests
                ).exclude(id=table_id).order_by('capacity')

                for candidate in candidate_tables:
                    # Bloquear la mesa candidata para verificar disponibilidad de forma segura
                    locked_candidate = Table.objects.select_for_update().get(id=candidate.id)
                    
                    existing_reservations = Reservation.objects.filter(
                        table=locked_candidate,
                        date=res_date,
                        status__in=['pending', 'confirmed']
                    )
                    
                    res_end_datetime = res_datetime + duration
                    overlap = False
                    for existing_res in existing_reservations:
                        ext_start = timezone.make_aware(datetime.combine(existing_res.date, existing_res.time))
                        ext_end = ext_start + duration
                        if (res_datetime < ext_end) and (res_end_datetime > ext_start):
                            overlap = True
                            break
                    
                    if not overlap:
                        table = locked_candidate
                        break

            # 3. Si después de buscar no encontramos nada, lanzar error
            if not table:
                # Verificar si es un problema de capacidad absoluta o de disponibilidad temporal
                if not Table.objects.filter(is_active=True, capacity__gte=guests).exists():
                    raise ValidationError("No hay mesas con capacidad suficiente.")
                else:
                    raise ValidationError("No hay disponibilidad para la fecha y número de personas en ninguna mesa.")

            # --- CREACIÓN DE LA RESERVA ---
            # Si llegamos aquí, 'table' es una mesa válida (la original o una reasignada)
            reservation = Reservation.objects.create(
                table=table,
                name=name,
                email=email,
                phone=phone,
                date=res_date,
                time=res_time,
                guests=guests,
            )
            return reservation

        
    @staticmethod
    def cancel_reservation(reservation_id, unique_code=None, admin=False):
        try:
            res = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise ValidationError("Reservation not found.")
            
        if not admin and str(res.unique_code) != unique_code:
            raise ValidationError("Invalid cancellation code.")
            
        res.status = 'cancelled'
        res.save()
        return res
