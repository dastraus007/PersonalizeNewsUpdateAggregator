from rest_framework import serializers

from .models import usernews


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = usernews
        fields = '__all__'