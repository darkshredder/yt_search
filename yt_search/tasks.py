from datetime import datetime
from celery import shared_task
from api.models import YTSearchQuery, YTSearchResult, APIKey, APIProvider
from yt_search.utils import get_api_key_for_query_yt, YoutubeSearch
from django.utils.dateparse import parse_datetime


@shared_task
def search_yt(query_id): 
    print("Start Celery task to search YouTube")
    yt_search_query = YTSearchQuery.objects.filter(id=query_id).first()

    if not yt_search_query:
        return "No query found"
    
    if yt_search_query.status == "running":
        return "Query is running"
    yt_search_query.status = "running"
    yt_search_query.save()
    try:


        youtube_search_object = YoutubeSearch(yt_search_query)

        # Get Search Results
        (search_response, err, pageToken) = youtube_search_object.search_results()
        if err:
            if "No API key available" in err:
                api_provider = APIProvider.objects.get(name="YouTube")
                earliest_updated_api_key = APIKey.objects.filter(
                    provider=api_provider,
                ).order_by("modified_at").first()
                # Run task again after some time update periodic task
                from django_celery_beat.models import PeriodicTask
                periodic_task = PeriodicTask.objects.get(name="search_yt_%s" % query_id)
                periodic_task.start_time = earliest_updated_api_key.next_use
                periodic_task.save()
                yt_search_query.status = "complete"
                yt_search_query.save()
                return err
            else:
                yt_search_query.status = "complete"
                yt_search_query.save()
                return err

        # Save Search Results

        bulkObjectList = list()

        for video in search_response:

            bulkObjectList.append(
                YTSearchResult(
                    query=yt_search_query,
                    video_id = video['id']['videoId'],
                    title = video['snippet']['title'],
                    description = video['snippet']['description'],
                    published_at = parse_datetime(video['snippet']['publishedAt']),
                    thumbnail_url = video['snippet']['thumbnails']['high']['url']
                )
            )

        YTSearchResult.objects.bulk_create(bulkObjectList, ignore_conflicts=True, batch_size=100)

        # Update Query
        yt_search_query.next_page_token = pageToken
        yt_search_query.save()
        print("Celery task to search YouTube completed")
    except Exception as e:
        print(e)
        yt_search_query.status = "complete"
        yt_search_query.save()
        return str(e)
    yt_search_query.status = "complete"
    yt_search_query.save()
    return "Celery task to search YouTube completed"