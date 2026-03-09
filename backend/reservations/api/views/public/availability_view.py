from rest_framework.views import APIView
from rest_framework.response import Response
from reservations.services.availability_service import AvailabilityService

class AvailabilityView(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        party_size = request.query_params.get('party_size')
        if not date:
            return Response({"error": "Date parameter is required"}, status=400)
            
        try:
            data = AvailabilityService.get_availability(date, party_size)
            return Response(data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
