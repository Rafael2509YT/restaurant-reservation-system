from rest_framework import serializers
from reservations.models import RestaurantConfig, Reservation
from reservations.serializers.table_serializer import TableSerializer

class RestaurantConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantConfig
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    table_details = TableSerializer(source='table', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['unique_code', 'created_at']
