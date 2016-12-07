from django.db import models
from django.urls import reverse

class ArticleManager(models.Manager):
    """
    return [(2016, [12, 09]), (2015, [11, 10])]
    """
    def archive(self):
        date_list = Article.objects.datetimes('created_time', 'month', order='DESC')
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict(d.year).append(d.month)
        return sorted(date_dict.items, reverse=True)


class Article(models.Model):
    objects = ArticleManager()
    
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )

    title = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tags', blank=True)
    abstract = models.CharField(max_length=54, blank=True, null=True, help_text='arbitrary')
    content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    topped = models.BooleanField(default=False)

    created_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-last_modified_time']


class Category(models.Model):
    name = models.CharField(max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
