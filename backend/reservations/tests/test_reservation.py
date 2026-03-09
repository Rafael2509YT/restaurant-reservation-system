from django.test import TestCase
from datetime import time, timedelta, date
from django.utils import timezone
from reservations.models import Table, Reservation, RestaurantConfig
from reservations.services.reservation_service import ReservationService
from rest_framework.exceptions import ValidationError

class ReservationServiceTests(TestCase):
    def setUp(self):
        # Configure restaurant
        self.config = RestaurantConfig.objects.create(
            opening_time=time(18, 0),
            closing_time=time(23, 0),
            reservation_interval_minutes=30,
            reservation_duration_minutes=60
        )
        # Create Tables
        self.table_small = Table.objects.create(number="1", capacity=2)
        self.table_medium_1 = Table.objects.create(number="2", capacity=4)
        self.table_medium_2 = Table.objects.create(number="3", capacity=4)
        self.table_large = Table.objects.create(number="4", capacity=8)
        
        # Test targets tomorrow
        self.tomorrow = timezone.localtime().date() + timedelta(days=1)

    def test_invalid_time_past(self):
        """Test reserving in the past fails"""
        past_date = (timezone.localtime() - timedelta(days=1)).strftime('%Y-%m-%d')
        data = {
            'table_id': self.table_medium_1.id,
            'name': 'Past Test',
            'email': 't@t.com',
            'phone': '123',
            'date': past_date,
            'time': '19:00',
            'guests': 4
        }
        with self.assertRaisesMessage(ValidationError, "Cannot reserve in the past."):
            ReservationService.create_reservation(data)

    def test_invalid_time_outside_hours(self):
        """Test reserving outside opening hours fails"""
        future_date = self.tomorrow.strftime('%Y-%m-%d')
        data = {
            'table_id': self.table_medium_1.id,
            'name': 'Early Test',
            'email': 't@t.com',
            'phone': '123',
            'date': future_date,
            'time': '16:00', # opens at 18
            'guests': 4
        }
        with self.assertRaisesMessage(ValidationError, "Reservation is outside operating hours."):
            ReservationService.create_reservation(data)

    def test_insufficient_capacity(self):
        """Test Case 2: Reject if capacity < guests"""
        future_date = self.tomorrow.strftime('%Y-%m-%d')
        data = {
            'table_id': self.table_medium_1.id, # cap 4
            'name': 'Big Group Test',
            'email': 't@t.com',
            'phone': '123',
            'date': future_date,
            'time': '19:00',
            'guests': 8 # Requires 8
        }
        with self.assertRaisesMessage(ValidationError, "No hay mesas con capacidad suficiente."):
            ReservationService.create_reservation(data)

    def test_overbooking(self):
        """Test preventing overlapping reservations on same table"""
        future_date = self.tomorrow.strftime('%Y-%m-%d')
        # Person 1 books at 19:00
        data1 = {
            'table_id': self.table_medium_1.id,
            'name': 'Person 1',
            'email': 't@t.com',
            'phone': '123',
            'date': future_date,
            'time': '19:00',
            'guests': 4
        }
        ReservationService.create_reservation(data1)
        
        # Person 2 tries to book same table at same time
        with self.assertRaisesMessage(ValidationError, "No hay disponibilidad para la fecha y hora seleccionadas."):
             data2 = {**data1, 'name': 'Person 2'}
             ReservationService.create_reservation(data2)

        # Person 3 tries to book same table at 19:30 (overlaps with 19:00-20:00 block)
        with self.assertRaisesMessage(ValidationError, "No hay disponibilidad para la fecha y hora seleccionadas."):
             data3 = {**data1, 'name': 'Person 3', 'time': '19:30'}
             ReservationService.create_reservation(data3)

        # Person 4 tries to book same table at 20:00 (Should succeed, starts right when previous ends)
        data4 = {**data1, 'name': 'Person 4', 'time': '20:00'}
        ReservationService.create_reservation(data4)
        
        # Verify 2 active reservations exist
        self.assertEqual(Reservation.objects.filter(table=self.table_medium_1).count(), 2)
