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

    full_name = models.TextField(default='')

    def __str__(self):
        return self.full_name


class RelatedKeywords(models.Model):
    related_keywords = models.TextField(null=True)

    def __str__(self):
        return self.related_keywords or ''


class Tag(models.Model):
    name = models.TextField()
    wiki_id = models.TextField(null=True)
    description = models.TextField(null=True)
    search_vector = SearchVectorField(null=True)
    aliases = models.TextField(null=True)

    def vector(self, *args, ** kwargs):
        self.search_vector = (
            SearchVector('name', weight='A')
            + SearchVector('description', weight='B')
            + SearchVector('aliases', weight='C')
                            )
        super().save(*args, **kwargs)


class Article(models.Model):
    pm_id = models.TextField()
    journal_title = models.TextField(null=True)
    article_title = models.TextField(null=True)
    authors = models.ManyToManyField(Author)
    abstract = models.TextField(null=True)
    publication_date = models.DateField(null=True)
    doi = models.TextField(null=True)
    keyword = models.TextField(default='')
    related_keywords = models.ManyToManyField(RelatedKeywords)
    tags = models.ManyToManyField(Tag)
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

    def get_object_or_404(self, pk):
        pass









