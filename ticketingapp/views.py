from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from ticketingapp.models import ParkingTicket, Mall
from ticketingapp.serializers import ParkingTicketSerializer, MallSerializer

# Create your views here.


class MallViewSet(ModelViewSet):
    
    serializer_class = MallSerializer
    queryset = Mall.objects.all()


class ParkingTicketViewSet(ModelViewSet):

    serializer_class = ParkingTicketSerializer
    queryset = ParkingTicket.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('status',)
    search_fields = ('plate_number',)


@api_view(['POST'])
def pay_ticket(request, ticket_id):
    parkingticket = get_object_or_404(ParkingTicket, pk=ticket_id)
    parkingticket.checkout()  # TODO: refactore checkout logic
    parkingticket.pay_ticket(request.data['fee_paid'])
    serializer = ParkingTicketSerializer(parkingticket)
    return Response(serializer.data)


@api_view(['GET'])
def exit_park(request, ticket_id):
    parkingticket = get_object_or_404(ParkingTicket, pk=ticket_id)
    if parkingticket.exit_park():
        serializer = ParkingTicketSerializer(parkingticket)
        return Response(serializer.data)
    return Response({'message': 'Outstanding payment, can\'t exit park'},
                    status=status.HTTP_400_BAD_REQUEST)
