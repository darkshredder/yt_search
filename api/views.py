from datetime import datetime
from django.shortcuts import render
from api.models import APIProvider, APIKey, YTSearchQuery, YTSearchResult
from yt_search.utils import change_api_key_next_use, get_api_key_for_query_yt
from django.db import transaction
from rest_framework import viewsets
from api.serializers import APIProviderSerializer, APIKeySerializer, YTSearchQuerySerializer, YTSearchResultSerializer
from rest_framework import generics
# filters
from rest_framework import filters

class YTSeachQueryListCreateAPIView(generics.ListCreateAPIView):
    queryset = YTSearchQuery.objects.all()
    serializer_class = YTSearchQuerySerializer

    # atomicity
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        super_values = super().post(request, *args, **kwargs)
        yt_search_query = YTSearchQuery.objects.get(id=super_values.data['id'])
        print("Start Clery task to search YouTube")
        from yt_search.tasks import search_yt
        # Create PreiodicTask to search YouTube for the query
        from django_celery_beat.models import PeriodicTask
        from django_celery_beat.schedulers import DatabaseScheduler
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        every_10_seconds, _ = IntervalSchedule.objects.get_or_create(
            every=10, period=IntervalSchedule.SECONDS,
        )
        PeriodicTask.objects.create(
            name='search_yt_' + str(yt_search_query.id),
            task='yt_search.tasks.search_yt',
            interval=every_10_seconds,
            start_time=datetime.now(),
            args=[yt_search_query.id],
        )
        return super_values


class YTSearchResultListAPIView(generics.ListAPIView):
    queryset = YTSearchResult.objects.all()
    serializer_class = YTSearchResultSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

