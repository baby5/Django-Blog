#coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from article.models import Article
from datetime import datetime
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  #添加包

def home(request):
    posts = Article.objects.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try :
        post_list = paginator.page(page)
    except PageNotAnInteger :
        post_list = paginator.page(1)
    except EmptyPage :
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list' : post_list})


class RSSFeed(Feed) :
    title = "RSS feed - article"
    link = "/feeds/posts/"
    description = "RSS feed - blog posts"

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
    try:
        post = Article.objects.get(pk=id)
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post': post})


def archives(request):
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'archives.html', {
        'post_list': post_list,
        'error': False
    })


def about_me(request):
    return render(request, 'aboutme.html')


def search_tag(request, tag):
    try:
        post_list = Article.objects.filter(category__iexact=tag)#忽略大小写, __contains:包含
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'tag.html', {'post_list': post_list}) 


def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if s:
            post_list = Article.objects.filter(title__icontains=s)
            return render(request, 'archives.html', {
                'post_list': post_list,
                'error': False if post_list else True,
            })
    return redirect('/')
            
