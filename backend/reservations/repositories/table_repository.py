from reservations.models import Table

class TableRepository:
    @staticmethod
    def get_all_active():
        return Table.objects.filter(is_active=True).order_by('capacity', 'number')
    
    @staticmethod
    def get_by_id(table_id):
        return Table.objects.filter(id=table_id, is_active=True).first()
