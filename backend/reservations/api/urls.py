from django.urls import path
from .views.public.availability_view import AvailabilityView
from .views.public.reservation_view import ReservationView, ReservationCancelView
from .views.admin.reservation_admin_view import AdminDashboardView, AdminCancelView, AdminMetricsView
from .views.admin.table_admin_view import TableAdminView, TableAdminDetailView
from .views.admin.config_admin_view import ConfigAdminView

urlpatterns = [
    # Public
    path('availability/', AvailabilityView.as_view(), name='availability'),
    path('reservations/', ReservationView.as_view(), name='create_reservation'),
    path('reservations/<int:reservation_id>/cancel/', ReservationCancelView.as_view(), name='cancel_reservation'),
    
    # Admin
    path('admin/reservations/', AdminDashboardView.as_view(), name='admin_reservations'),
    path('admin/reservations/<int:reservation_id>/cancel/', AdminCancelView.as_view(), name='admin_cancel_reservation'),
    path('admin/metrics/', AdminMetricsView.as_view(), name='admin_metrics'),
    path('admin/tables/', TableAdminView.as_view(), name='admin_tables'),
    path('admin/tables/<int:table_id>/', TableAdminDetailView.as_view(), name='admin_table_detail'),
    path('admin/config/', ConfigAdminView.as_view(), name='admin_config'),
]
