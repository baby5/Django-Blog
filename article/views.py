#coding:utf-8
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.syndication.views import Feed
from django.views import generic
from django.http import HttpResponseRedirect

from .models import Article, Tags
from .forms import ArticleCommentForm

def home(request):
    article_list = Article.objects.all()
    tag_list = Tags.objects.all()
    date_archives = Article.objects.archive()#custom
    return render(request, 'article/list.html', {
        'article_list' : article_list,
        'tag_list': tag_list,
        'date_archives': date_archives,
    })


class CommentView(generic.edit.FormView):
    form_class = ArticleCommentForm
    template_name = "article/detail.html"

    def form_valid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.article = target_article
        comment.save()
        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['pk'])
        return redirect(target_article.get_absolute_url()) 


class DetailView(generic.DetailView):
    model = Article
    template_name = 'article/detail.html'
    
    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tags.objects.all()
        kwargs['date_archives'] = Article.objects.archive()
        kwargs['form'] = ArticleCommentForm()
        kwargs['comment_list'] = self.object.articlecomment_set.all()
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
