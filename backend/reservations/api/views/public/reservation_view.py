from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reservations.services.reservation_service import ReservationService
from reservations.serializers.reservation_serializer import ReservationSerializer
from rest_framework.exceptions import ValidationError

# [API] Uso de APIView de Django Rest Framework para construir endpoints RESTful.
class ReservationView(APIView):
    def post(self, request):
        try:
            # [SERVICE LAYER] La vista solo orquesta; la lógica pesada reside en el servicio.
            reservation = ReservationService.create_reservation(request.data)
            serializer = ReservationSerializer(reservation)
            
            # [MANEJO DE ERRORES] Uso de códigos de estado HTTP semánticos (201 Created).
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # [MANEJO DE ERRORES] Captura de errores de validación con código 400 Bad Request.
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating reservation: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReservationCancelView(APIView):
    def delete(self, request, reservation_id):
        code = request.data.get('unique_code')
        try:
            ReservationService.cancel_reservation(reservation_id, unique_code=code, admin=False)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
