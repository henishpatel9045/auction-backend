from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

# Create your views here.
class GoogleLoginView(APIView):
    def post(self, request):
        email = request.POST.data.get("email")
        user = User.objects.filter(email=email)
        if user.exists():
            refresh = RefreshToken(user.first())
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": f"User with emailId {email} does not exists."
            }, status=status.HTTP_400_BAD_REQUEST)
