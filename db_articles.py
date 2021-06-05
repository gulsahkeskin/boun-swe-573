import index
import json
import time
from django.db.utils import IntegrityError
from datetime import datetime

# from MediTagProject.wsgi import *
from Tagapp.models import Article, Author, RelatedKeywords


def fetch_articles():
    try:
        with open("articles.json", 'r') as fp:
            articles = json.load(fp)
            # print("Articles loaded from articles.json")
    except:
        search_handle = index.EntrezSearchRequest(index.keyword)
        total_batches = str(search_handle.total_articles // search_handle.article_limit)
        for i in range(0, search_handle.total_articles, search_handle.article_limit):
            start_batch_time = time.time()
            search_handle.pipeline(i)
            end_batch_time = time.time()
            time_elapsed = str(round(end_batch_time - start_batch_time, 2))
            batch_no = str(i // search_handle.article_limit + 1)
            # print("Current batch [{}/{}] took {} seconds.".format(batch_no, total_batches, time_elapsed))
        unique_ids = set()
        for article_id in search_handle.articles:
            unique_ids.add(article_id)
        search_handle.error_log.close()
        with open("articles.json", 'w') as fp:
            json.dump(search_handle.articles, fp)
        with open("article_ids.txt", 'w') as fp:
            for a in search_handle.article_ids:
                fp.write(a + "\n")
        articles = search_handle.articles
    finally:
        fp.close()
    # print(articles)
    return articles


def save_db():
    articles = fetch_articles()
    article_objects = []
    article_ids = []
    for p in articles:
        article_ids.append(p)
        authors = articles[p]['Authors']
        author_list = []
        related_keywords = articles[p]['Related Keywords']
        keyword_list = []

        for a in authors:
            author = Author.objects.get_or_create(full_name=a)
            author_list.append(author[0])
        for r in related_keywords:
            keyword = RelatedKeywords.objects.get_or_create(related_keywords=r)
            keyword_list.append(keyword[0])

        # deneme = articles[p]['Publication Date']
        # print(type(deneme))
        # print(deneme)

        for date_format in ('%Y %b %d', '%Y %m %d'):
            try:
                date_article = datetime.strptime(articles[p]['Publication Date'], date_format)
            except ValueError:
                pass
        article = Article(pm_id=p,
                          journal_title=articles[p]['Journal Title'],
                          article_title=articles[p]['Article Title'],
                          abstract=articles[p]['Abstract'],
                          publication_date=date_article,
                          keyword=articles[p]['Keyword']
                          )

        try:
            article.save()
            if author_list:
                article.authors.add(*author_list)
            if keyword_list:
                article.related_keywords.add(*keyword_list)
            # print("Article ", p, " saved.")
        except IntegrityError:
            # print("Article ", p, "cannot be saved.")
            pass
        else:
            # print("Article save failed.")
            pass


save_db()

# with open("articles.json", 'r') as fp:
#     articles = json.load(fp)
# with open("article_ids.txt", 'r') as fp:
#     article_ids = fp.readlines()
# articles = set(articles.keys())
# article_ids = set([ids.strip('\n') for ids in article_ids])
# id_diff = article_ids - articles
# for diff in id_diff:
#     print(diff)
