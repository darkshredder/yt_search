from api.models import APIProvider, APIKey, YTSearchQuery, YTSearchResult
from django.utils import timezone
from django.utils.timezone import make_aware

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

def change_api_key_next_use(api_key):
    tomorrow = timezone.datetime.now() + timezone.timedelta(days=1)
    api_key.next_use = tomorrow
    api_key.save()

def get_api_key_for_query_yt():
    api_provider = APIProvider.objects.get(name="YouTube")
    api_key = APIKey.objects.filter(provider=api_provider, next_use__lte=make_aware(timezone.datetime.now())).first()
    return api_key


class YoutubeSearch:

    def __init__(self, query, published_after=(datetime.datetime.strftime(
            datetime.datetime.now() - datetime.timedelta(hours=2),
            "%Y-%m-%dT%H:%M:%SZ",
        ))):
        self.query = query
        self.api_key = get_api_key_for_query_yt()
        self.youtube = self.build_youtube_object()
        self.published_after = published_after
        self.page_token = self.get_page_token() 
    
    def build_youtube_object(self):
        if not self.api_key:
            self.youtube = None
            return None
        self.youtube = build("youtube", "v3", developerKey=self.api_key.key)
        return self.youtube

    def get_page_token(self):
        return self.query.next_page_token
    
    def update_api_key_next_use(self):
        change_api_key_next_use(self.api_key)
        self.api_key = get_api_key_for_query_yt()

    def search_results(self):
        if not self.api_key:
            return [], "No API key available", None
        
        if not self.youtube:
            return [], "No API key available", None
        try:
            search_response = self.youtube.search().list(
                q=(self.query.query).replace(" ", "+"),
                part="id,snippet",
                order="date",
                publishedAfter=self.published_after,
                type="video",
                pageToken=self.page_token,

            ).execute()
        except HttpError as e:
            if "exceeded" in e._get_reason():
                self.update_api_key_next_use()
                return self.search_results()
            else:
                return [], e._get_reason(), None
        except Exception as e:
            return [], str(e.__class__.__name__), None
        
        self.page_token = search_response.get("nextPageToken", None)

        return search_response.get("items", []), None, self.page_token



            