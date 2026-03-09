from django.test import TestCase
from datetime import time, timedelta
from django.utils import timezone
from reservations.models import Table, Reservation, RestaurantConfig
from reservations.services.availability_service import AvailabilityService
from reservations.services.reservation_service import ReservationService

class AvailabilityServiceTests(TestCase):
    def setUp(self):
        self.config = RestaurantConfig.objects.create(
            opening_time=time(18, 0),
            closing_time=time(23, 0),
            reservation_interval_minutes=30,
            reservation_duration_minutes=60
        )
        self.tomorrow = (timezone.localtime().date() + timedelta(days=1)).strftime('%Y-%m-%d')
        
    def test_case_1_all_tables_full(self):
        """Test Case 1: 5 tables of 4, all 5 booked at 20:00, no availability at 20:00"""
        tables = []
        for i in range(5):
             tables.append(Table.objects.create(number=str(10+i), capacity=4))

        # Book all 5 at 20:00
        for table in tables:
             ReservationService.create_reservation({
                  'table_id': table.id,
                  'name': f'P_{table.id}',
                  'email': 'x@x.com',
                  'phone': '1',
                  'date': self.tomorrow,
                  'time': '20:00',
                  'guests': 4
             })
             
        # Check availability specifically
        avail = AvailabilityService.get_availability(self.tomorrow)
        self.assertEqual(len(avail), 5, "Should return 5 tables' data")
        
        for t_data in avail:
            self.assertNotIn('20:00', t_data['available_times'], "20:00 should not be available on any table")
            # 19:30 should also not be available fully if config is 60m duration and 30m gaps 
            # (overlapping 19:30 -> 20:30 overlaps with 20:00 reservation)
            self.assertNotIn('19:30', t_data['available_times'])
            # 19:00 should be available
            self.assertIn('19:00', t_data['available_times'])
