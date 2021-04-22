from django.db import models

class Search(models.Model):
    search_text = models.CharField(max_length=100)
