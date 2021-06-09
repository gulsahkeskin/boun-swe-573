from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import Article
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
    # if request.method == 'POST':
    #     article_as_dict = {}
    #     articles = Article.objects.filter(article_title__icontains='searched')
    #     for index, article in enumerate(articles):
    #         article_as_dict[index] = {'title': article.article_title}
    #     # print(article_as_dict)
    #     return render(request, 'Tagapp/search_results.html', {'articles': article_as_dict})
    # else:
    #     return render(request, 'Tagapp/search.html', {})

    if request.method == "POST":
        searched = request.POST.get('searched')
        # articles = Article.objects.filter(SearchQuery('article_title'))
        # if searched:
        # print(searched)
        articles = Article.objects.filter(Q(article_title__icontains='searched')).distinct()
        # print(len(articles))

        return render(request, 'tagapp/search_results.html', context={'articles': articles})

        # return render(request, 'tagapp/search_results.html', {'searched': searched})
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




    # if request.method == 'GET':
    #     query = request.GET.get('q')
    #     searchbutton = request.GET.get('submit')
    #     if query is not None:
    #         lookups = Q(journal_title__icontains=query) | Q(article_title__icontains=query)
    #
    #         results = Article.objects.filter(lookups).distinct()
    #
    #         context = {'results': results,
    #                    'searchbutton': searchbutton}
    #
    #         return render(request, 'tagapp/search.html', context)
    #
    #     else:
    #         return render(request, 'tagapp/search.html')
