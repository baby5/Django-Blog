#coding:utf-8
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic

from .models import Article, Category, Tags
from datetime import datetime


def home(request):
    articles = Article.objects.filter(status='p')
    paginator = Paginator(articles, 2)
    page = request.GET.get('page')
    try:
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)
    
    tag_list = Tags.objects.all()
    date_archives = Article.objects.archive()#custom
    return render(request, 'article/list.html', {
        'article_list' : article_list,
        'tag_list': tag_list,
        'date_archives': date_archives,
    })


class DetailView(generic.DetailView):
    model = Article
    template_name = 'article/detail.html'
    
    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tags.objects.all()
        kwargs['date_archives'] = Article.objects.archive()
        return super(DetailView, self).get_context_data(**kwargs)


class BaseListView(generic.ListView):
    
    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tags.objects.all()
        kwargs['date_archives'] = Article.objects.archive()
        return super(BaseListView, self).get_context_data(**kwargs)
    

class ArchivesView(BaseListView):
    template_name = 'article/list.html'

    def get_queryset(self):
        if 'year' in self.kwargs and 'month' in self.kwargs:
            return Article.objects.filter(created_time__year=self.kwargs['year'], created_time__month=self.kwargs['month'])
        else:
            return Article.objects.all()


class CategoryView(BaseListView):
    template_name = 'article/list.html'

    def get_queryset(self):
        return Article.objects.filter(category=self.kwargs['cate_id'])


class TagView(BaseListView):
    template_name = 'article/list.html'

    def get_queryset(self):
        return Article.objects.filter(tags=self.kwargs['tag_id'])


def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if s:
            article_list = Article.objects.filter(title__icontains=s)
            tag_list = Tags.objects.all()
            date_archives = Article.objects.archive()#custom
            return render(request, 'article/list.html', {
                'article_list': article_list,
                'tag_list' : tag_list,
                'date_archives': date_archives,
                'error_message': '' if article_list else 'No Results',
            })
    return redirect('/')


def about_me(request):
    tag_list = Tags.objects.all()
    date_archives = Article.objects.archive()#custom
    return render(request, 'article/aboutme.html', {
        'tag_list' : tag_list,
        'date_archives': date_archives,
    })


class RSSFeed(Feed) :
    title = "RSS feed - article"
    link = "/feeds/articles/"
    description = "RSS feed - blog articles"

    def items(self):
        return Article.objects.order_by('-last_modified_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.last_modified_time

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.get_absolute_url()
