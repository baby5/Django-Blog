from django.contrib import admin
from article.models import Article


class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'category', 'content']}),
    ]
    list_display = ('title', 'category', 'date_time')
    list_filter = ['category', 'date_time']
    search_fields = ['title']

admin.site.register(Article, BlogAdmin)
