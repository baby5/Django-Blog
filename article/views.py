#coding:utf-8
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article
from datetime import datetime


def home(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 2)
    page = request.GET.get('page')
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'article_list' : article_list})


class RSSFeed(Feed) :
    title = "RSS feed - article"
    link = "/feeds/articles/"
    description = "RSS feed - blog articles"

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.get_absolute_url()


def detail(request, id):
    article = get_object_or_404(Article, pk=id)
    return render(request, 'detail.html', {'article': article})


def archives(request):
    article_list = Article.objects.all()
    return render(request, 'list.html', {
        'article_list': article_list,
    })


def about_me(request):
    return render(request, 'aboutme.html')


def search_tag(request, tag):
    article_list = get_list_or_404(Article, category__iexact=tag)#忽略大小写, __contains:包含
    return render(request, 'list.html', {'article_list': article_list}) 


def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if s:
            article_list = Article.objects.filter(title__icontains=s)
            return render(request, 'list.html', {
                'article_list': article_list,
                'error_message': '' if article_list else '没结果',
            })
    return redirect('/')
            
