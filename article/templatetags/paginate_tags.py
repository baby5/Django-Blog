from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

register = template.Library()

@register.simple_tag(takes_context=True)
def paginate(context, object_list, page_count):
    paginator = Paginator(object_list, page_count)
    page = int(context['request'].GET.get('page', 1))

    try:
        object_list = paginator.page(page)
        context['current_page'] = page
        pages = get_page_range(page, paginator.num_pages)
    except PageNotAnInteger:
        object_list = paginator.page(1)
        context['current_page'] = 1
        pages = get_page_range(1, paginator.num_pages)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
        context['current_page'] = paginator.num_pages
        pages = get_page_range(paginator.num_pages, paginator.num_pages)

    context['article_list'] = object_list
    context['pages'] = pages
    context['last_page'] = paginator.num_pages
    context['first_page'] = 1
    try:
        context['pages_first'] = pages[0]
        context['pages_last'] = pages[-1] + 1
    except:
        context['pages_first'] = 1
        context['pages_last'] = 2

    return ''


def get_page_range(page, num_pages):
    left = page-2 if page-2 > 1 else 2
    right = page+2 if page+2 < num_pages else num_pages

    return range(left, right)
