from recipe.models import Ingredient

from rest_framework import serializers



class IngridientSerilaizer(serializers.ModelSerializer):
    class Meta:
        fields = ('ing_name',)
        model = Ingredient

    def to_representation(self, instance):
        return {'title': instance.ing_name, 'dimension': instance.get_unit_display()}


class CommonIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

