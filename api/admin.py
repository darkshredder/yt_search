from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from api.models import APIProvider, APIKey, YTSearchQuery, YTSearchResult
admin.site.register(APIProvider)
admin.site.register(APIKey)
admin.site.register(YTSearchQuery)
admin.site.register(YTSearchResult)
