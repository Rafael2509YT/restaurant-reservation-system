from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum
from reservations.models import Reservation, Table, RestaurantConfig
from reservations.serializers.reservation_serializer import ReservationSerializer
from reservations.services.reservation_service import ReservationService
from rest_framework.exceptions import ValidationError

class AdminDashboardView(APIView):
    def get(self, request):
        date_filter = request.query_params.get('date')
        status_filter = request.query_params.get('status')
        
        reservations = Reservation.objects.all().order_by('date', 'time')
        
        if date_filter:
            try:
                date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
                reservations = reservations.filter(date=date_obj)
            except ValueError:
                return Response({"error": "Invalid date format"}, status=400)
                
        if status_filter:
            reservations = reservations.filter(status=status_filter)
            
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class AdminCancelView(APIView):
    def delete(self, request, reservation_id):
        try:
            ReservationService.cancel_reservation(reservation_id, admin=True)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)

class AdminMetricsView(APIView):
    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            date_str = timezone.localtime().strftime('%Y-%m-%d')
            
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
             return Response({"error": "Invalid date format"}, status=400)

        total_capacity = Table.objects.filter(is_active=True).aggregate(total=Sum('capacity'))['total'] or 0
        
        if total_capacity == 0:
            return Response({"occupancy_percentage": 0, "date": date_str})

        config = RestaurantConfig.objects.first()
        if not config:
            return Response({"error": "Missing config"}, status=400)

        opening = datetime.combine(date_obj, config.opening_time)
        closing = datetime.combine(date_obj, config.closing_time)
        if config.closing_time < config.opening_time:
             closing += timedelta(days=1)
             
        duration = timedelta(minutes=config.reservation_duration_minutes)
        
        blocks = int((closing - opening).total_seconds() / duration.total_seconds())
        max_daily_capacity = total_capacity * blocks

        reserved_guests = Reservation.objects.filter(
            date=date_obj, 
            status__in=['confirmed', 'pending']
        ).aggregate(guests=Sum('guests'))['guests'] or 0

        occupancy_percent = (reserved_guests / max_daily_capacity) * 100 if max_daily_capacity else 0

        return Response({
            "date": date_str,
            "total_capacity": total_capacity,
            "max_daily_capacity": max_daily_capacity,
            "reserved_guests": reserved_guests,
            "occupancy_percentage": round(occupancy_percent, 2)
        })
