from datetime import date, timedelta
from django.db.models import Sum

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


class CallDetailSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(source='starts_at__timestamp')
    end_time = serializers.DateTimeField(source='ends_at__timestamp')
    duration = serializers.SerializerMethodField()
    price = serializers.FloatField(source='price')

    class Meta:
        model = Call
        fields = (
            'destination', 'start_time', 'end_time', 'duration', 'price'
        )

    def get_duration_field(self, obj):
        return obj.get_duration_display()


class PhoneBillSerializer(serializers.Serializer):
    phone = serializers.CharField()
    period = serializers.DateField(
        required=False,
        format='%m/%Y',
        input_formats=['%m/%Y', '%m/%y'],
        default=date(date.today().year, date.today().month, 1) - timedelta(days=1)
    )
    total_cost = serializers.SerializerMethodField()
    detailed_cost = serializers.SerializerMethodField()

    def validate_period(self, value):
        today = date.today()
        if value.month >= today.month:
            raise serializers.ValidationError(
                'The month does not have a closed period yet'
            )
        return value

    def _get_phone_records(self, data):
        return Call.objects.filter(
            source=data['phone'],
            starts_at__timestamp__year=data['period'].year,
            starts_at__timestamp__month=data['period'].month,
            ends_at__isnull=False
        )

    def get_total_cost(self, data):
        total_calls = self._get_phone_records(data)
        return total_calls.aggregate(Sum('price'))['price__sum'] or 0.00

    def get_detailed_cost(self, data):
        total_calls = self._get_phone_records(data)
        result = [CallDetailSerializer(call).data for call in total_calls]
        return result
