from api.models import APIProvider, APIKey, YTSearchQuery, YTSearchResult
from rest_framework import serializers


class APIProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIProvider
        fields = '__all__'

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = '__all__'

class YTSearchQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = YTSearchQuery
        fields = '__all__'

class YTSearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = YTSearchResult
        fields = '__all__'
