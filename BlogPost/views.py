from django.shortcuts import render, redirect
from .models import BlogPost


def blogs(request):
    articles = BlogPost.objects.all()

    for article in articles:
        if len(article.title) > 40:
            article.title = f"{article.title[:40].strip()}..."

        article.tags = article.tags.split(', ')[:3]

    context = {
        'articles': articles
    }
    return render(request, 'BlogPost/blogs.html', context)


def search_tag(request, tag):
    articles = BlogPost.objects.all()

    results = [article for article in articles if tag in article.tags]

    for article in results:
        article.tags = article.tags.split(', ')[:3]

    context = {
        'articles': results,
        'title': f'Search Results for: {tag}',
        'tag': tag
    }
    return render(request, 'BlogPost/blogs.html', context)


def search_query(request):
    query = request.GET.get('search', '')
    articles = BlogPost.objects.all()

    results = []

    if query:
        for article in articles:
            if query in article.tags:
                results.append(article)
            elif query in article.title:
                results.append(article)

        for article in results:
            article.tags = article.tags.split(', ')[:3]

    context = {
        'articles': results,
        'title': f'Search Results for: {query}',
        'tag': query
    }

    return render(request, 'BlogPost/blogs.html', context)


def blog_page(request, id):
    article = BlogPost.objects.get(id=id)

    article.tags = article.tags.split(', ')

    return render(request, 'BlogPost/blog_page.html', {"article": article})


def redirect_to_blogpost(request):
    return redirect('home')
