from django.contrib import admin
from .models import Article
from .models import Tag


admin.site.register(Article)
admin.site.register(Tag)