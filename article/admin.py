from django.contrib import admin
from article.models import Article, Category


class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'category', 'content']}),
    ]
    list_display = ('title', 'category')
    list_filter = ['category']
    search_fields = ['title']

admin.site.register(Article, BlogAdmin)
admin.site.register(Category)
