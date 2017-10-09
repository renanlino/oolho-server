from rest_framework import serializers
from app.models import Movement, Sensor

class SensorSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movements = serializers.HyperlinkedRelatedField(many=True,
        view_name='movement-detail', read_only=True)

    class Meta:
        model = Sensor
        fields = ('id', 'display_name', 'created_date',
            'last_seen', 'owner', 'movements')

class MovementSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Movement
        fields = ('id', 'sensor', 'direction', 'received_date',
            'occurrence_date', 'owner')
