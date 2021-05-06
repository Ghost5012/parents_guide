import hashlib
import json
from json import JSONEncoder

from django.contrib.auth import get_user_model, authenticate
from pyparsing import unicode
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.utils.timezone import now
from bson import ObjectId
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from django.core.mail import EmailMessage

from .models import Parent, Driver, Bus
from .serializers import UserSerializer, DriverSerializer, BusSerializer


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class UserViewSet(generics.CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class GetAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            user.is_active = True
            user.last_login = now()
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(json.loads(JSONEncoder().encode({
                'token': token.key,
                # 'user_id': user.pk,
                'user': json.loads(JSONEncoder().encode({
                    'user_id': user.pk,
                    'username': user.username,
                    'email': user.email,
                    'phone': user.phone_number,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'logitude': user.longitude,
                    'latitude': user.latitude,
                    'picture': json.dumps(unicode(user.picture))
                }))

            })))
        return Response({
            "type": "Error",
            "message": "User not found"
        })


class GetAllParents(APIView):
    def get(self, request):
        model = Parent.objects.all()
        serializer_class = UserSerializer(model, many=True)
        return Response({'data': json.loads(JSONEncoder().encode(serializer_class.data)),
                  'status': status.HTTP_200_OK})


class LogoutView(APIView):
    def post(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return Response({
            'type': 'success',
            'message': "logout successful"
        })


class ParentsPositionView(APIView):
    """
    Modifie les renvoie les coordonnees d'un parent
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # print(id)
        user = request.user
        return Response({
            'position': {'longitude': user.longitude, 'latitude': user.latitude}
        })

    def post(self, request):
        position = request.data
        user = request.user
        user.longitude = position['longitude']
        user.latitude = position['latitude']
        user.save()
        return Response({
            'position': {'longitude': user.longitude, 'latitude': user.latitude}
        })


class DriverViewSet(APIView):
    """
    cree et retourne la liste des conducteurs
    """
    def get(self,request):
        queryset = Driver.objects.all()
        serializer_class = DriverSerializer(queryset, many=True)
        return Response({'data': json.loads(JSONEncoder().encode(serializer_class.data)),
                             'status': status.HTTP_200_OK})


class BusViewSet(APIView):
    """
    cree un nouveau bus et retourne la liste des bus
    """
    def get(self,request):
        queryset = Bus.objects.all()
        serializer_class = BusSerializer(queryset, many=True)
        return Response({'data': json.loads(JSONEncoder().encode(serializer_class.data)),
                             'status': status.HTTP_200_OK})


class BusPositionViewSet(APIView):
    """
    modifie et retourne les coordonnees d'un bus
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        bus = Bus.objects.get(bus_number=request.params['number'])
        return Response({
            'position': {'longitude': bus.longitude, 'latitude': bus.latitude}
        })
    
    def post(self, request):
        position = request.data
        user = request.user
        bus = user.bus_number
        bus.longitude = position['longitude']
        bus.latitude = position['latitude']
        bus.save()
        return Response({
            'position': {'longitude': user.longitude, 'latitude': user.latitude}
        })
