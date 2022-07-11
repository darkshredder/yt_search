from datetime import datetime
from django.db import models
from django.utils import timezone
# Create your models here.

class AbstractBaseModel(models.Model):
    """
    An abstract base class model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    extras_json = models.JSONField(
        blank=True, default=None, null=True, verbose_name="Extras JSON"
    )

    class Meta:
        abstract = True
        ordering = ["-created_at", "-modified_at"]

class APIProvider(AbstractBaseModel):
    """
    API Provider
    """

    name = models.CharField(max_length=255, unique=True, verbose_name="Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "API Provider"
        verbose_name_plural = "API Providers"


class APIKey(AbstractBaseModel):
    """
    API Key
    """

    provider = models.ForeignKey(
        APIProvider, on_delete=models.CASCADE, verbose_name="Provider"
    )
    key = models.CharField(max_length=255, unique=True, verbose_name="Key")
    is_exhausted = models.BooleanField(
        default=False, verbose_name="Is Exhausted"
    )
    next_use = models.DateTimeField(
        blank=True, null=True, verbose_name="Next Use Date", default=datetime.now
    )

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

STATUS_OPTIONS = (
    ("running", "running"),
    ("complete", "complete"),
)

class YTSearchQuery(AbstractBaseModel):
    """
    Search Query
    """

    query = models.CharField(max_length=255, unique=True, verbose_name="Query")
    latest_published_date = models.DateTimeField(
        blank=True, default=None, null=True, verbose_name="Latest Published Date"
    )
    next_page_token = models.TextField(
        blank=True, default="", null=True, verbose_name="Next Page Token"
    )
    status = models.CharField(
        max_length=255, default="complete", verbose_name="Status"
    )
    def __str__(self):
        return self.query

    class Meta:
        verbose_name = "Search Query"
        verbose_name_plural = "Search Queries"

class YTSearchResult(AbstractBaseModel):
    """
    Search Result
    """

    query = models.ForeignKey(
        YTSearchQuery, on_delete=models.CASCADE, verbose_name="Query"
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    published_at = models.DateTimeField(verbose_name="Published At")
    thumbnail_url = models.URLField(verbose_name="Thumbnail URL")
    video_id = models.CharField(max_length=255, verbose_name="Video ID")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Search Result"
        verbose_name_plural = "Search Results"
        indexes = [
            models.Index(fields=['title', 'description']),
            models.Index(fields=['published_at']),
        ]
        ordering = ["-published_at"]