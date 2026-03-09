from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reservations.models import RestaurantConfig
from reservations.serializers.reservation_serializer import RestaurantConfigSerializer

class ConfigAdminView(APIView):
    def get(self, request):
        config = RestaurantConfig.objects.first()
        if not config:
            config = RestaurantConfig.objects.create()
        serializer = RestaurantConfigSerializer(config)
        return Response(serializer.data)

    def put(self, request):
        config = RestaurantConfig.objects.first()
        if not config:
            config = RestaurantConfig.objects.create()
            
        serializer = RestaurantConfigSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
