from rest_framework import serializers

from main.models import Call


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ('identifier', 'source', 'destination')
        read_only_fields = ('identifier', )

    def create(self, validated_data):
        instance = super(CallSerializer, self).create(validated_data)
        instance.start_call()
        return instance

    def to_representation(self, instance):
        ret = super(CallSerializer, self).to_representation(instance)

        ret.update({'call_start': instance.starts_at.timestamp})

        if instance.has_ended:
            ret.update({'call_end': instance.ends_at.timestamp})

        return ret

    def validate(self, attrs):
        source = attrs.get('source')
        destination = attrs.get('destination')

        if source == destination:
            raise serializers.ValidationError('The phone numbers must be different.')

        return attrs
