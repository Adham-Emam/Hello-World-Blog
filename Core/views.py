from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views 
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from BlogPost.models import BlogPost
from BlogPost.article_fetcher import fetch_and_save_articles


def home(request):
    fetch_and_save_articles()

    # Query BlogPost objects to display in the template
    articles = BlogPost.objects.all()

    latest_articles = []

    for article in articles:
        if article.cover_img:
            latest_articles.append(article)
            if len(latest_articles) == 5:
                break

    for article in articles:
        if len(article.title) > 40:
            article.title = f"{article.title[:40].strip()}..."

        article.tags = article.tags.split(', ')[:3]

    context = {
        'articles': latest_articles
    }
    return render(request, 'Core/home.html', context)


def regiester(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful.')
            return redirect('login')
        else:
            messages.error(
                request, 'Registration failed. Please correct the error below.')
    else:
        form = UserCreationForm()

    return render(request, 'Core/regiester.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'Core/login.html')


@login_required
def logout_view(request):
    # Capture the referring URL
    next_url = request.META.get('HTTP_REFERER', 'home')

    logout(request)

    return redirect(next_url)
