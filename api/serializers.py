from rest_framework import serializers

from main.models import Call


class CallSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(write_only=True, required=False)

    class Meta:
        model = Call
        fields = ('identifier', 'source', 'destination', 'timestamp')
        read_only_fields = ('identifier', )

    def create(self, validated_data):
        timestamp = validated_data.pop('timestamp', None)

        instance = super(CallSerializer, self).create(validated_data)
        instance.start_call(timestamp)
        return instance

    def to_representation(self, instance):
        ret = super(CallSerializer, self).to_representation(instance)

        ret.update({'call_start': instance.starts_at.timestamp})

        if instance.has_ended:
            ret.update({
                'call_end': instance.ends_at.timestamp,
                'price': instance.price,
                'duration': instance.get_duration_display()
            })

        return ret

    def validate(self, attrs):
        source = attrs.get('source')
        destination = attrs.get('destination')

        if source == destination:
            raise serializers.ValidationError('The phone numbers must be different.')

        return attrs
