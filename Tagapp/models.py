from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.search import SearchVector, SearchVectorField


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Author(models.Model):

    # LastName = models.CharField(max_length=32, default='')
    # ForeName = models.CharField(max_length=32, default='')
    #
    # def __str__(self):
    #     return self.ForeName + ' ' + self.LastName

    full_name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.full_name


class RelatedKeywords(models.Model):
    related_keywords = models.CharField(max_length=300,  null=True)

    def __str__(self):
        return self.related_keywords or ''


class Article(models.Model):
    pm_id = models.CharField(max_length=16)
    journal_title = models.CharField(max_length=255)
    article_title = models.TextField(max_length=511)
    authors = models.ManyToManyField(Author)
    abstract = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True)
    keyword = models.CharField(max_length=300, default='')
    related_keywords = models.ManyToManyField(RelatedKeywords)
    # related_keywords = models.CharField(max_length=255, null=True)
    tags = models.CharField(max_length=255, null=True)
    search_vector = SearchVectorField(null=True)

    def __str__(self):
        return self.article_title or ''

    def vector(self, *args, ** kwargs):
        self.search_vector = (
            SearchVector('article_title', weight='A')
            + SearchVector('abstract', weight='B')
            + SearchVector('related_keywords', weight='B')
                            )
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    wiki_id = models.CharField(max_length=64, null=True)
    description = models.TextField(max_length=1000, null=True)
    search_vector = SearchVectorField(null=True)
    # wikidata_url = models.URLField(null=True)
    aliases = models.TextField(max_length=1000, null=True)

    def vector(self, *args, ** kwargs):
        self.search_vector = (
            SearchVector('name', weight='A')
            + SearchVector('description', weight='B')
            + SearchVector('aliases', weight='C')
                            )
        super().save(*args, **kwargs)






