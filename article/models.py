from django.db import models
from django.urls import reverse

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )

    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    abstract = models.CharField(max_length=54, blank=True, null=True, help_text='arbitrary')
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    topped = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

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
