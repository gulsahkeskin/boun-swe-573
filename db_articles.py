import index
import json
import time
from django.db.utils import IntegrityError
from datetime import datetime

# from MediTagProject.wsgi import *
from Tagapp.models import Article, Author, RelatedKeywords


def fetch_articles():
    try:
        with open("articles_new.json", 'r') as fp:
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
            print("Current batch [{}/{}] took {} seconds.".format(batch_no, total_batches, time_elapsed))
        unique_ids = set()
        for article_id in search_handle.articles:
            unique_ids.add(article_id)
        search_handle.error_log.close()
        with open("articles_new.json", 'w') as fp:
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
    article_ids = set()
    dbsave_log = open('dbsave.log', 'a')
    dbsave_log.write("Database save started.\n")
    article_ids_db = set(Article.objects.values_list('pm_id', flat=True))
    for p in articles:
        start = time.time()
        article_ids.add(p)
        authors = articles[p]['Authors'].split(',')
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

        try:
            date_article = datetime.strptime(articles[p]['Publication Date'], '%d-%m-%Y')
        except:
            date_article = None
        article = Article(pm_id=p,
                          journal_title=articles[p]['Journal Title'],
                          article_title=articles[p]['Article Title'],
                          abstract=articles[p]['Abstract'],
                          publication_date=date_article,
                          keyword=articles[p]['Keyword']
                          )

        try:
            if p not in article_ids_db:
                article.save()

                for a in author_list:
                    article.authors.add(a)
                for k in keyword_list:
                    article.related_keywords.add(k)
                article_ids_db.add(p)
                dbsave_log.write("Article with pmid " + p + " successfully added.\n")
            # article.search_vector()

            # print("Article ", p, " saved.")
        except IntegrityError:
            dbsave_log.write("Article " + p + " cannot be saved. Cause: Integrity Error\n")
            pass

        finish = time.time()
    dbsave_log.write("Done.\n")
# save_db()


def save_doi():
    articles = fetch_articles()
    article_objs = Article.objects.all()
    article_pmids = Article.objects.values_list('pm_id', flat=True)

    for i, pmid in enumerate(article_pmids):
        article_objs[i].doi = articles[pmid]["DOI"]
        if (i+1) % 1000 == 0:
            print(i, len(articles))
    print("Started updating")
    Article.objects.bulk_update(article_objs, ['doi'], batch_size=512)
    print("Update done")
    """
    for p in articles:
        pmid = articles[p]["PMID"]
        doi = articles[p]["DOI"]
        Article.objects.filter(pm_id=pmid).update(doi=doi)
    """

