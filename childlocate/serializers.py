from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Driver, Bus


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    picture_url = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    # picture_url = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'email', 'username', 'first_name', 'last_name', 'profession', 'phone_number',
            'longitude', 'latitude', 'password', 'password2', 'picture_url']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True}
        }

    def save(self, **kwargs):
        user = get_user_model().objects.create(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            profession=self.validated_data['profession'],
            phone_number=self.validated_data['phone_number'],
            longitude=self.validated_data['longitude'],
            latitude=self.validated_data['latitude'],
            password=self.validated_data['password']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        buses = Bus.objects.all()
        for bus in buses:
            if bus.reserved_places < bus.number_of_places:
                bus.reserved_places = int(bus.reserved_places)+1
                bus.save()
                user.bus_number = bus
                break
        if password != password2:
            raise serializers.ValidationError({"password": "password must match"})
        user.set_password(password)
        user.save()
        return user


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['_id', 'matricule', 'bus', 'phone_number', 'bus_number']


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['_id', 'bus_number', 'number_of_places', 'longitude', 'latitude']
