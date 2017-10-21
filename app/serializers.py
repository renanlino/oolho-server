from rest_framework import serializers
from app.models import Movement, Sensor, Space

class SpaceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    sensors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Space
        fields = ('id', 'display_name', 'created_date',
                'owner', 'sensors')

class SpaceChartSerializer(serializers.Serializer):
    response = serializers.BooleanField()

class SensorSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movements = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = ('id', 'display_name', 'created_date',
            'last_seen', 'owner', 'movements')

class MovementSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Movement
        fields = ('id', 'sensor', 'direction', 'received_date',
            'occurrence_date', 'owner', 'value')
