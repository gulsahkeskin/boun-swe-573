from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .forms import TagForm

from .models import Article, Tag, Author, RelatedKeywords
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery
from django.core.paginator import Paginator

from .forms import CreateUserForm


def home(request):
    return render(request, 'tagapp/home.html')


def signup_user(request):
    form = CreateUserForm()

    if request.method == 'GET':
        return render(request, 'tagapp/signupuser.html', {'form': form})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('search')
            except IntegrityError:
                return render(request, 'tagapp/signupuser.html',
                              {'form': form, 'error': "This username is already taken! Please choose a new username."})
        else:
            # Tell the user that password didn't match
            return render(request, 'tagapp/signupuser.html',
                          {'form': form, 'error': "Passwords do not match!"})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'tagapp/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'tagapp/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('search')


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def search(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        if searched:
            articles = Article.objects.filter(Q(article_title__icontains=searched)).distinct()
        # print(len(articles))

            return render(request, 'tagapp/search_results.html', context={'articles': articles})
    else:
        return render(request, 'tagapp/search.html', {})

    # search = request.GET.get('search')
    # articles = Article.objects.order_by('-publication_date')
    # if search:
    #     articles = articles.filter(Q(journal_title__icontains=search) |
    #                                Q(article_title__icontains=search) |
    #                                Q(abstract__icontains=search)).distinct()
    #     page = request.GET.get('page')
    #     paginator = Paginator(articles, 25)
    #
    #     return render(request, 'tagapp/search.html', context={'articles': paginator.get_page(page)})
    #
    # else:
    #     return render(request, 'tagapp/search.html')


def search_results(request):
    return render(request, 'tagapp/search_results.html')


def article_details(request, pk):
    article = Article.objects.get(pk=pk)
    authors = Author.objects.filter(article=article)
    keywords = RelatedKeywords.objects.filter(article=article)
    tags = Tag.objects.filter(article=article)
    article_dict = {
        "journal_title": article.journal_title,
        "article_title": article.article_title,
        "authors": authors,
        "date": article.publication_date,
        "abstract": article.abstract,
        "keywords": keywords,
        "doi": article.doi,
        "tags": tags
    }
    return render(request, 'tagapp/article_details.html', context=article_dict)


@login_required
# def create_tag(request, pk):
#     article = Article.objects.get(pk=pk)
#     tags = Tag.objects.filter(article=article)
#     if request.method == 'POST':
#         form = TagForm(data=request.POST)
#         query = request.POST.get('query')
#         if query:
#             suggestions = WikiData.wiki_suggest(query)
#             print(suggestions)
#             article.Tag.add(tags)
#
#     return render(request, 'tagapp/create_tag.html', {'form': TagForm})

@login_required
def create_tag(request):
    form = TagForm()
    if request.method == 'POST':
        form = TagForm(request.POST)
    # if request.method == 'POST':
    #     query = request.POST.get('query')
    #     form = TagForm(data=request.POST)
    #     if form.data['suggestions']:
    #         choices = form.data['suggestions']

    return render(request, 'tagapp/create_tag.html', {'form': form})
    # if request.method == 'GET':
    #     return render(request, 'tagapp/create_tag.html', {'form': TagForm()})
    # else:
    #     try:
    #         form = TagForm(data=request.POST)
    #         newtag = form.save(commit=False)
    #         newtag.user = request.user
    #         newtag.save()
    #     except ValueError:
    #         return render(request, 'tagapp/create_tag.html', {'form': TagForm(), 'error': "bad data passed in"})

    # return redirect('article_details')


@login_required
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk, user=request.user)
    if request.method == 'POST':
        tag.delete()
        return redirect('article_details')


def tag_list(request):
    return render(request, 'tag_list.html')
