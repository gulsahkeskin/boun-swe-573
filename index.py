import collections.abc
import os
import pprint
import requests
from datetime import datetime
# from Tagapp.models import RelatedKeywords

# from dotenv import load_dotenv, find_dotenv

import functions

# config = load_dotenv(find_dotenv())
# API_KEY = os.environ.get("API_KEY")
API_KEY = '0801d08efda8bc62efb416ebdcfa4ed6f00a'
keyword = "bipolar disorder"


class Article:

    def __init__(self, pm_id, title, journal_issn, journal_name, abstract,
                 pubmed_link, author_list, instutation_list, article_date, article_type):
        self.pm_id = pm_id
        self.title = title
        self.journal_issn = journal_issn
        self.journal_name = journal_name
        self.abstract = abstract
        self.pubmed_link = pubmed_link
        self.author_list = author_list
        self.institution_list = instutation_list
        self.article_date = article_date


class EntrezSearchRequest:
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    # article_limit = 20
    # total_articles = 50000
    total_articles = 50000

    def __init__(self, keyword, article_limit=200):  # articld_limit = 200
        self.keyword = keyword
        self.article_limit = article_limit
        self.error_log = open('parse_err_ids.log', 'a')
        self.article_ids = []
        self.article_list = []
        self.articles = {}

    def __str__(self):
        return self.base_url + "efetch.fcgi?db=pubmed&id=" + self.keyword + "&retmax" + str(self.article_limit)

    def print(self):
        pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)
        pp.pprint(self.articles)

    def get_article_ids(self):
        try:
            response = requests.get(self.base_url + "esearch.fcgi",
                                    params={"term": self.keyword,
                                            "db": "pubmed",
                                            "retmax": self.total_articles,
                                            "api_key": API_KEY}
                                    )

            if response.ok:
                data = functions.xmltojson(response.text)
                self.article_ids = data["eSearchResult"]["IdList"]["Id"]
            else:
                print("Article id can not be retrieved.")
        except:
            print("Wrong.")

    def get_articles(self, begin=0):
        end = begin + self.article_limit
        response = requests.get(self.base_url + "efetch.fcgi",
                                params={"db": "pubmed",
                                        "id": self.article_ids[begin:end],
                                        "retmode": "xml",
                                        "api_key": API_KEY},
                                headers={"Content-Type": "application/xml;charset=UTF-8"}
                                )
        article_data = functions.xmltojson(response.text)

        if response.ok:
            self.article_list = article_data["PubmedArticleSet"]["PubmedArticle"]
        # print(*article_ids, sep="\n")
        # print(articles)

    def parse_article_abstract(self, abstract, pmid):
        abstract_text = ""
        try:
            if abstract == '':
                return abstract_text
            else:
                abstract = abstract.get("AbstractText", "")

            if type(abstract) == str:
                abstract_text += abstract
            elif type(abstract) == list:
                for obj in abstract:
                    if obj is not None:
                        if type(obj) == dict:
                            label = obj.get("@Label", "")
                            text = obj.get("#text", "")
                            if label != "":
                                abstract_text += label + ": "
                            abstract_text += text + "\n\n"
                        elif type(obj) == str:
                            abstract_text += obj + "\n\n"
        except:
            print("Could not parse abstract with PMID: ", pmid, "its type: ", type(abstract))
            self.error_log.write("Abstract error: " + pmid)
        return abstract_text

    def parse_authors(self, author_itr, pmid):
        author_list = []
        try:
            if type(author_itr) == list:
                for pros in author_itr:
                    firstName = pros.get("ForeName", "")
                    lastName = pros.get("LastName", "")
                    full_name = firstName + " " + lastName
                    full_name = full_name.strip()
                    author_list.append(full_name)
            elif type(author_itr) == collections.abc.Mapping:
                firstName = author_itr.get("ForeName", "")
                lastName = author_itr.get("LastName", "")
                full_name = firstName + " " + lastName
                full_name = full_name.strip()
                author_list.append(full_name)
        except:
            print("Could not parse authors, PMID: ", pmid)
            self.error_log.write("Author error: " + pmid)

        return ', '.join(author_list)

    def parse_date(self, date_obj, pmid):
        # date = ""
        if date_obj.get("Year") and date_obj.get("Month") and date_obj.get("Day"):
            date_deneme = date_obj.get("Year") + "-" + \
                          date_obj.get("Month") + "-" + \
                          date_obj.get("Day")
            for date_format in ('%Y-%b-%d', '%Y-%m-%d'):
                try:
                    return datetime.strptime(date_deneme, date_format)

                except ValueError:
                    pass
            raise ValueError('no valid format found')
        elif date_obj.get("Year") and date_obj.get("Month"):
            date_deneme = date_obj.get("Year") + "-" + date_obj.get("Month")
            for date_format in ('%Y-%b', '%Y-%m'):
                try:
                    return datetime.strptime(date_deneme, date_format)
                except ValueError:
                    pass
            raise ValueError('no valid format found')
        elif date_obj.get("Year"):
            date_deneme = date_obj.get("Year")
            return datetime.strptime(date_deneme, '%Y')
        else:
            return None

    def parse_doi(self, doi_obj, pmid):
        doi = ""
        if type(doi_obj) == collections.abc.Mapping:
            doi = doi_obj.get("#text", "")
        elif type(doi_obj) == list:

            for obj in doi_obj:
                if obj.get("@EIdType") == "doi":
                    doi = obj.get("#text", "")
                    break
        else:
            self.error_log.write("Could not parse DOI. DOI type unknown. PMID: " + pmid)
            doi = ""
        return doi

    def parse_articles(self):
        for paper in self.article_list:
            # Retrieves Journal name
            journal_title = paper["MedlineCitation"]["Article"]["Journal"].get("Title", "")
            # print("Journal title: ", journal_title)

            # Retrieves PMID number from key #text like in example: {'@Version': '1', '#text': '33988931'}
            pm_id_dict = paper["MedlineCitation"]["PMID"]
            pm_id = pm_id_dict.get("#text", "")
            # print("PMID", pm_id)

            # Retrieves article title of the papers
            article_title = paper["MedlineCitation"]["Article"].get("ArticleTitle", "")
            # print("Article Title: ", article_title)

            abstract = paper["MedlineCitation"]["Article"].get("Abstract", "")
            abstract_text = self.parse_article_abstract(abstract, pm_id)

            doi = paper.get("MedlineCitation").get("Article").get("ELocationID")
            doi = self.parse_doi(doi, pm_id)

            keyword_list = paper.get("MedlineCitation").get("KeywordList", {}).get("Keyword", [])
            keywords = [keyword.get("#text") for keyword in keyword_list] if type(keyword_list) == list \
                else [keyword_list]

            authors = paper["MedlineCitation"]["Article"].get("AuthorList", {})
            author_obj = authors.get("Author", [])
            author_list = self.parse_authors(author_obj, pm_id)
            # print(author_list, 24174890)

            date_obj = paper["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]
            date_published = self.parse_date(date_obj, pm_id)
            if date_published is not None:
                date_published = date_published.strftime("%d-%m-%Y")
            # print(date_obj)
            # print(type(date_published))

            self.articles[pm_id] = {"PMID": pm_id,
                                    "Journal Title": journal_title,
                                    "Article Title": article_title,
                                    "Authors": author_list,
                                    "Abstract": abstract_text,
                                    "Publication Date": date_published,
                                    "DOI": doi,
                                    "Keyword": self.keyword,
                                    "Related Keywords": keywords
                                    }

    def pipeline(self, begin=0):
        self.get_article_ids()
        self.get_articles(begin)
        self.parse_articles()


# pubmed_request = EntrezSearchRequest(keyword, article_limit=200)
# pubmed_request.pipeline()
# pubmed_request.print()
