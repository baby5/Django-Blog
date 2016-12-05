from django.contrib import admin
from article.models import Article, Category, Tags


class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'tags', 'category', 'abstract', 'content', 'status', 'topped']}),
    ]
    list_display = ('title', 'created_time', 'last_modified_time', 'category')
    list_filter = ['last_modified_time', 'category']
    search_fields = ['title']

admin.site.register(Article, BlogAdmin)
admin.site.register(Category)
admin.site.register(Tags)
