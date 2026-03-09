from datetime import datetime, timedelta, date, time
from django.utils import timezone
from reservations.models import Table, Reservation, RestaurantConfig

class AvailabilityService:
    @staticmethod
    def get_availability(date_str, party_size=None):
        try:
            req_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        config = RestaurantConfig.objects.first()
        if not config:
            raise ValueError("Restaurant configuration is missing.")

        tables = Table.objects.filter(is_active=True)
        if party_size:
            tables = tables.filter(capacity__gte=int(party_size))
        
        # Calculate all possible start times for the day
        slots = []
        current_time_dt = datetime.combine(req_date, config.opening_time)
        closing_time_dt = datetime.combine(req_date, config.closing_time)
        
        # Determine if closing time is on the next day (e.g., opens at 18:00, closes at 02:00)
        if config.closing_time < config.opening_time:
             closing_time_dt += timedelta(days=1)

        interval = timedelta(minutes=config.reservation_interval_minutes)
        duration = timedelta(minutes=config.reservation_duration_minutes)

        while current_time_dt + duration <= closing_time_dt:
            slots.append(current_time_dt.time())
            current_time_dt += interval

        reservations = Reservation.objects.filter(
            table__in=tables,
            date=req_date,
            status__in=['pending', 'confirmed']
        )

        availability = []
        # Check availability per slot per table
        now = timezone.localtime()
        
        for table in tables:
            table_res = reservations.filter(table=table)
            available_slots = []
            
            for slot_time in slots:
                # If checking today, don't return past slots
                slot_datetime = timezone.make_aware(datetime.combine(req_date, slot_time))
                if req_date == now.date() and slot_datetime <= now:
                    continue
                elif req_date < now.date():
                    continue

                slot_end_datetime = slot_datetime + duration
                slot_end_time = slot_end_datetime.time()
                
                # Check overlaps
                overlap = False
                for res in table_res:
                    res_start_datetime = timezone.make_aware(datetime.combine(res.date, res.time))
                    res_end_datetime = res_start_datetime + duration
                    
                    # Overlap condition:
                    if (slot_datetime < res_end_datetime) and (slot_end_datetime > res_start_datetime):
                        overlap = True
                        break
                
                if not overlap:
                    available_slots.append(slot_time.strftime('%H:%M'))
            
            if available_slots:
                availability.append({
                    'table_id': table.id,
                    'table_capacity': table.capacity,
                    'table_number': table.number,
                    'available_times': available_slots
                })
            
        return availability
