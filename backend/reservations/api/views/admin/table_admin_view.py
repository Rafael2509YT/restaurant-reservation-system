from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reservations.models import Table
from reservations.serializers.table_serializer import TableSerializer
from reservations.services.table_service import TableService
from rest_framework.exceptions import ValidationError

class TableAdminView(APIView):
    def get(self, request):
        tables = Table.objects.all().order_by('number')
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TableAdminDetailView(APIView):
    def get_object(self, table_id):
        try:
            return Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            raise ValidationError("Table not found")

    def put(self, request, table_id):
        try:
            data = TableService.update_table(table_id, request.data)
            return Response(data)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, table_id):
        try:
            TableService.delete_table(table_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
             return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
