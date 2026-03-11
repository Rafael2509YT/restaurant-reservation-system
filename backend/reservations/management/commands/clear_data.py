import sys
from django.core.management.base import BaseCommand
from django.db import connection
from reservations.models import Table, Reservation

class Command(BaseCommand):
    help = 'Borra todos los datos de las tablas Table y Reservation y reinicia los contadores de ID'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-confirm',
            action='store_true',
            help='Ejecuta sin pedir confirmación',
        )

    def handle(self, *args, **options):
        if not options['no_confirm']:
            confirm = input("⚠️ ¿ESTÁS SEGURO? Se borrarán TODAS las reservaciones y mesas. (s/n): ")
            if confirm.lower() != 's':
                self.stdout.write(self.style.WARNING('Operación cancelada.'))
                return

        try:
            # 1. Borrar reservaciones (dependencia)
            self.stdout.write('Borrando reservaciones...')
            Reservation.objects.all().delete()

            # 2. Borrar mesas
            self.stdout.write('Borrando mesas...')
            Table.objects.all().delete()

            # 3. Reiniciar contadores (Opcional, solo funciona en PostgreSQL/SQLite)
            self.stdout.write('Reiniciando contadores de ID...')
            with connection.cursor() as cursor:
                db_engine = connection.vendor
                if db_engine == 'postgresql':
                    cursor.execute("TRUNCATE TABLE reservations_reservation, reservations_table RESTART IDENTITY CASCADE;")
                elif db_engine == 'sqlite':
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('reservations_reservation', 'reservations_table');")

            self.stdout.write(self.style.SUCCESS('✅ Base de datos vaciada y contadores reiniciados con éxito.'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
