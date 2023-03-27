from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item, Bid
from datetime import datetime
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class ListingItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q_type = float(request.GET.get("type", "live"))
        today = datetime.now().today()
        now = datetime.now().time()
        if q_type == "live":
            qs = Item.objects.filter(
                start_date__lte=today,
                start_time__lte=now,
                end_date__gt=today,
                end_time__gt=now,
            )
        elif q_type == "upcoming":
            qs = Item.objects.filter(
                Q(start_date__gt=today) 
                | Q(start_date=today, 
                      start_time__gte=now)
            )
        elif q_type == "past":
            qs = Item.objects.filter(
                Q(end_date__lt=today) 
                | Q(end_date=today, 
                      end_time__lt=now)
            )
        elif q_type == "personal":
            qs = Item.objects.filter(owner=request.user)
        else:
            qs = Item.objects.all()
        return Response(qs.values(), status=status.HTTP_200_OK)


class BidView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        pass

    def post(self, request):
        data = request.data
        
