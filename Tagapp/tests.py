from django.test import TestCase, Client

from .models import Article, Author, Tag, User


# View tests
class UrlResponse(TestCase):
    client = Client()

    def test_home_url_response_ok(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_login_url_response_ok(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_search_url_response_ok(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 302)


# Form tests
class FormResponse(TestCase):
    def test_signup_form_ok(self):
        client = Client()
        url = '/signup/'
        fields = {'username': 'gulcaa',
                  'first_name': 'gulsah',
                  'last_name': 'keskin',
                  'email': 'gulsah@gg.com',
                  'password1': '123',
                  'password2': '123'}
        response = client.post(url, fields)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/search/')


# Model test
class ModelTest(TestCase):

    def setUp(self):
        Article.objects.create(article_title='bipolar disorder',
                               pm_id='31202087',
                               journal_title='Asian journal of psychiatry',
                               keyword='catatonia',
                               abstract='AIM: To compare the symptom profile of catatonia among patients with '
                                        'affective, psychotic and organic disorders...',
                               doi='10.1016/j.ajp.2019.05.024')

    def test_article_created_ok(self):
        article = Article.objects.get()
        self.assertEqual(article.article_title, 'bipolar disorder')
        self.assertEqual(article.pm_id, '31202087')
        self.assertEqual(article.journal_title, 'Asian journal of psychiatry')
        self.assertEqual(article.keyword, 'catatonia')
        self.assertEqual(article.abstract, 'AIM: To compare the symptom profile of catatonia among patients with '
                                           'affective, psychotic and organic disorders...')
        self.assertEqual(article.doi, '10.1016/j.ajp.2019.05.024')

    def createAuthor(self, full_name='Sandeep Grover'):
        return Author.objects.create(full_name=full_name)

    def test_author_created_ok(self):
        author = self.createAuthor()
        self.assertTrue(isinstance(author, Author))

    def wikidataTags(self,
                     wiki_id='Q131755',
                     description='human mental illness characterized by mood changes',
                     aliases='BP, depressione maniacale, depressione bipolare, fase maniacale del disturbo bipolare, '
                             'disturbo maniacale, disturbo bipolare misto, disturbo maniaco-depressivo, '
                             'disturbo bipolare maniacale I., mania ipomania, ipomania mania, disturbo affettivo '
                             'bipolare maniacale, psicopatico depressivo-maniacale., disturbo affettivo bipolare, '
                             'malattia bipolare, malattia maniaco-depressiva, psicosi maniaco-depressiva, '
                             'follia circolare, mood disorders, bipolar spectrum, mood swing, anhedonia, insomnia, '
                             'hypersomnia, delusion, aphasia, hallucination, hypersexuality, mania, hypomania, '
                             'mental depression, fatigue, psychomotor agitation, mood swing, topiramate, olanzapine, '
                             'gabapentin, lithium compounds, risperidone, quetiapine, valproic acid, lamotrigine, '
                             'clozapine, tiagabine, clonazepam, carbamazepin, lamotrigine, transclopenthixol'):
        tags = Tag.objects.create(wiki_id=wiki_id, description=description, aliases=aliases)

        return tags

    def test_tags_created_ok(self):
        tags = self.wikidataTags()
        self.assertTrue(isinstance(tags, Tag))
        check_tag = Tag.objects.filter(wiki_id='Q131755').values()
        self.assertEqual(check_tag[0].get('description'), tags.description)
