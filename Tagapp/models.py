from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.search import SearchVector, SearchVectorField


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Author(models.Model):
    """
    LastName = models.CharField(max_length=32, default='')
    ForeName = models.CharField(max_length=32, default='')

    def __str__(self):
        return self.ForeName + ' ' + self.LastName
    """
    full_name = models.CharField(max_length=50, default='')


class RelatedKeywords(models.Model):
    related_keywords = models.CharField(max_length=300,  null=True)

    def __str__(self):
        return self.related_keywords


class Article(models.Model):
    pm_id = models.CharField(max_length=16)
    journal_title = models.CharField(max_length=256)
    article_title = models.TextField(max_length=500)
    authors = models.ManyToManyField(Author)
    abstract = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True)
    keyword = models.CharField(max_length=300)
    related_keywords = models.ManyToManyField(RelatedKeywords)
    # tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.article_title


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True)
    search = SearchVectorField(null=True)
    wikidata_url = models.URLField(null=True)



